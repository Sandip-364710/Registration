# jobs/admin.py
from django.contrib import admin
from .models import UserInfo, BusinessRegistration, IndividualRegistration,JobPosting, Recommendation


class UserInfoAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('user', 'email', 'skills', 'experience')

    # Fields to filter the list view by
    list_filter = ('user', 'skills', 'experience')

    # Fields to search by in the search box
    search_fields = ('user','skills', 'experience','email')

# Register the UserInfo model with the UserInfoAdmin configuration
admin.site.register(UserInfo, UserInfoAdmin)

class BusinessRegistrationAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('org_name', 'name', 'email', 'experience', 'country','skills')

    # Fields to filter the list view by
    list_filter = ('country', 'state', 'city', 'industry')

    # Fields to search by in the search box
    search_fields = ('org_name', 'name', 'email', 'state', 'city','email','skills' )

admin.site.register(BusinessRegistration, BusinessRegistrationAdmin)
class IndividualRegistrationAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('name', 'email', 'skills', 'experience', 'country',)

    # Fields to filter the list view by
    list_filter = ('name','country', 'skills', 'experience')

    # Fields to search by in the search box
    search_fields = ('name','country', 'skills', 'experience' )

admin.site.register(IndividualRegistration, IndividualRegistrationAdmin )

class Jobpostingadmin(admin.ModelAdmin):
    list_display=('company','title','experience','skills')
    list_filter = ('company','title', 'skills', 'experience')
    search_fields = ('company','title', 'skills', 'experience' )
admin.site.register(JobPosting, Jobpostingadmin)

class Recommendationadmin(admin.ModelAdmin):
    list_display=('user','job')
    list_filter=('user','job')
    search_fields=('user','job')

admin.site.register(Recommendation, Recommendationadmin)
