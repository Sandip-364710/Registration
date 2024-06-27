# jobs/admin.py
from django.contrib import admin
from .models import UserInfo, BusinessRegistration, IndividualRegistration,JobPosting, Recommendation

admin.site.register(UserInfo)
admin.site.register(BusinessRegistration)
admin.site.register(IndividualRegistration)
admin.site.register(JobPosting)
admin.site.register(Recommendation)
