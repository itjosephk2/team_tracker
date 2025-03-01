from django.contrib.auth.models import User
from django.db import models
from datetime import date

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    active = models.BooleanField(default=False)  # Keep active stored in the DB
    manager = models.ForeignKey(
        'self',  # Self-referential ForeignKey
        on_delete=models.SET_NULL,  # Keep employee if manager is removed
        null=True,
        blank=True,
        related_name="team_members"
    )
    # The user field is optional, so employee can exist without being linked to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id})"

    def update_active_status(self):
        """Updates the active status based on contracts."""
        today = date.today()
        self.active = self.contracts.filter(contract_start__lte=today, contract_end__gte=today).exists()
        self.save()



class Contract(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='contracts')
    job_title = models.CharField(max_length=255)  # Using job_title instead of a Job model
    contract_start = models.DateField()
    contract_end = models.DateField(null=True, blank=True)
    hourly_rate = models.FloatField(default=12.45)
    contracted_hours = models.FloatField(default=40)

    def __str__(self):
        return f"{self.person} - {self.job_title}"
