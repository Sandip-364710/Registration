from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    experience = models.IntegerField()
    designation = models.CharField(max_length=255)
    skills = models.CharField(max_length=300)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class BusinessRegistration(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE) 
    org_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="software developer", blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    password = models.CharField(max_length=128)
    headcount = models.IntegerField()
    industry = models.CharField(max_length=255, default="IT-Software, Software Services", blank=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    experience = models.IntegerField(blank=False, null=True)  # Allow NULL values
    skills = models.CharField(max_length=255, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(BusinessRegistration, self).__init__(*args, **kwargs)
        # Store the original password when the object is created or retrieved
        self._original_password = self.password

    def save(self, *args, **kwargs):
        # Check if the password has been modified
        if self.password != self._original_password:
            self.password = make_password(self.password)
        super(BusinessRegistration, self).save(*args, **kwargs)

    def __str__(self):
        return self.org_name

class IndividualRegistration(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    experience = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class JobPosting(models.Model):
    company = models.ForeignKey(BusinessRegistration, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    skills = models.TextField()
    description = models.TextField()
    location = models.CharField(max_length=255, default='Unknown')

    def __str__(self):
        return self.title

class Recommendation(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.job}"
