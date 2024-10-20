from django.db import models

# Create your models here.
class person(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 255)
    phone_number = models.IntegerField()
    date_of_birth = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class contract(models.Model):
    person_id = models.ForeignKey(person, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    contract_start = models.DateField()
    contract_end = models.DateField()
    hourly_rate = models.FloatField(default=12.45)
    contracted_hours = models.FloatField(default=40)

    def __str__(self):
        return self.name