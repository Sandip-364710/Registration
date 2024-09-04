# jobs/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserInfo, BusinessRegistration, IndividualRegistration, JobPosting

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['experience', 'designation', 'skills','email']

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = BusinessRegistration
        fields = [
            'org_name',
            'name',
            'email',
            'phone',
            'address',
            'country',
            'state',
            'city',
            'website',
            'headcount',
            'industry',
            'salary',
            'experience',
            'skills',
            'id',
            'password'
        ]
        

class IndividualRegistrationForm(forms.ModelForm):
    class Meta:
        model = IndividualRegistration
        fields = '__all__'

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'experience', 'skills', 'description'] 


class RecruiterLoginForm(forms.Form):
    companyid = forms.CharField(label='Company ID', max_length=50)
    companypassword = forms.CharField(label='Password', widget=forms.PasswordInput)