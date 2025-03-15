from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import date


class Person(models.Model):
    """
    Represents an employee in the system.

    Each Person can be linked to a Django `User` for authentication.
    A Person may also have a manager (who is another Person instance).
    """
    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("manager", "Manager"),
        ("hr_admin", "HR Admin"),
    ]

    first_name = models.CharField(max_length=50, help_text="The employee's first name.")
    last_name = models.CharField(max_length=50, help_text="The employee's last name.")
    email = models.EmailField(max_length=255, unique=True, help_text="The employee's email address.")
    phone_number = models.CharField(max_length=15, blank=True, help_text="Contact number of the employee.")
    date_of_birth = models.DateField(help_text="Employee's date of birth.")
    active = models.BooleanField(default=False, help_text="Indicates if the person is currently employed.")

    manager = models.ForeignKey(
        'self',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_members",
        help_text="Manager supervising this employee."
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="employee",
        help_text="The role of the person in the company."
    )

    user = models.OneToOneField(
        "auth.User",  
        on_delete=models.CASCADE,
        related_name="person",
        null=True,
        blank=True,
        help_text="The associated Django user account."
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

    def update_active_status(self):
        """
        Updates the `active` field based on active contracts.

        The person is considered active if they have at least one contract 
        where the current date falls within the contract period.
        """
        today = date.today()
        self.active = self.contracts.filter(contract_start__lte=today).exclude(contract_end__lt=today).exists()
        self.save()


class Contract(models.Model):
    """
    Represents an employment contract for a Person.
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='contracts',
        help_text="The person this contract belongs to."
    )
    job_title = models.CharField(
        max_length=255,
        help_text="Job title associated with this contract."
    )
    contract_start = models.DateField(help_text="Contract start date.")
    contract_end = models.DateField(null=True, blank=True, help_text="Contract end date (if applicable).")
    hourly_rate = models.FloatField(default=12.45, help_text="Hourly pay rate for this contract.")
    contracted_hours = models.FloatField(default=40, help_text="Number of contracted hours per week.")

    def __str__(self):
        return f"{self.person} - {self.job_title}"


@receiver(post_save, sender=Contract)
def activate_person_on_contract(sender, instance, **kwargs):
    """Activate a person only if today's date is within the contract period."""
    today = date.today()
    
    if instance.person and not instance.person.active:
        if instance.contract_start <= today and (instance.contract_end is None or today <= instance.contract_end):
            instance.person.active = True
            instance.person.save()

@receiver(post_delete, sender=Contract)
def deactivate_person_if_no_valid_contracts(sender, instance, **kwargs):
    """Deactivate the person if they have no valid (active) contracts."""
    today = date.today()

    has_valid_contract = Contract.objects.filter(
        person=instance.person,
        contract_start__lte=today,  # Started already
    ).exclude(
        contract_end__lt=today  # Not already expired
    ).exists()

    if instance.person and not has_valid_contract:
        instance.person.active = False
        instance.person.save()
