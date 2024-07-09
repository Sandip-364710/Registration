from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    experience = models.IntegerField()
    designation = models.CharField(max_length=255)
    skills = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username

class BusinessRegistration(models.Model):
    org_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    headcount = models.IntegerField()
    industry = models.CharField(max_length=255)
    

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
    company = models.ForeignKey(BusinessRegistration, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Recommendation(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.job}"
