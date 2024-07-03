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
        fields = '__all__'

class IndividualRegistrationForm(forms.ModelForm):
    class Meta:
        model = IndividualRegistration
        fields = '__all__'

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = '__all__'
