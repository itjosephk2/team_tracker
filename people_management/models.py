from django.db import models

# Create your models here.
class person(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 250)

    job_link_description = models.URLField(max_length = 200)
    application_posted = models.DateField()
    date_applied = models.DateField(default=datetime.date.today)
    cv = models.FileField(blank=True, null=True)
    cover_letter = models.FileField(blank=True, null=True)
    date_last_followup = models.DateField()
    recruiter_name = models.CharField(max_length= 80)
    recruiter_email = models.EmailField(max_length = 250)
    manager_name = models.CharField(max_length= 80)
    
    company_name = models.CharField(max_length= 60)
    company_website = models.URLField(max_length = 200)

    def __str__(self):
        return self.name