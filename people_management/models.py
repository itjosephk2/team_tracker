from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Person(models.Model):
    """
    Represents an employee in the system.

    Each Person can be linked to a Django `User` for authentication.
    A Person may also have a manager (who is another Person instance).
    """

    first_name = models.CharField(max_length=50, help_text="The employee's first name.")
    last_name = models.CharField(max_length=50, help_text="The employee's last name.")
    email = models.EmailField(max_length=255, unique=True, help_text="The employee's email address.")
    phone_number = models.CharField(max_length=15, blank=True, help_text="Contact number of the employee.")
    date_of_birth = models.DateField(help_text="Employee's date of birth.")
    active = models.BooleanField(default=False, help_text="Indicates if the person is currently employed.")

    manager = models.ForeignKey(
        'self',  # Self-referential foreign key to link a manager
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_members",
        help_text="Manager supervising this employee."
    )

    user = models.OneToOneField(
        User,  # Links this Person to a Django `User` instance for authentication
        on_delete=models.CASCADE,
        related_name="person",
        null=True,
        blank=True,
        help_text="The associated Django user account."
    )

    def __str__(self):
        """
        Returns a string representation of the Person object.
        """
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

    def update_active_status(self):
        """
        Updates the `active` field based on active contracts.
        
        The person is considered active if they have at least one contract 
        where the current date falls within the contract period.
        """
        today = date.today()
        self.active = self.contracts.filter(contract_start__lte=today, contract_end__gte=today).exists()
        self.save()


class Contract(models.Model):
    """
    Represents an employment contract for a Person.

    Stores job title, contract dates, hourly rate, and contracted hours.
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
        """
        Returns a string representation of the Contract object.
        """
        return f"{self.person} - {self.job_title}"