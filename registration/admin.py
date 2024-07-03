# jobs/admin.py
from django.contrib import admin
from .models import UserInfo, BusinessRegistration, IndividualRegistration,JobPosting, Recommendation


class UserInfoAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('user', 'email', 'skills', 'experience')

    # Fields to filter the list view by
    list_filter = ('user', 'skills', 'experience')

    # Fields to search by in the search box
    search_fields = ('user','skills', 'experience')

# Register the UserInfo model with the UserInfoAdmin configuration
admin.site.register(UserInfo, UserInfoAdmin)

class BusinessRegistrationAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('org_name', 'name', 'email', 'phone', 'country',)

    # Fields to filter the list view by
    list_filter = ('country', 'state', 'city', 'industry')

    # Fields to search by in the search box
    search_fields = ('org_name', 'name', 'email', 'state', 'city', )

admin.site.register(BusinessRegistration, BusinessRegistrationAdmin)
class IndividualRegistrationAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('name', 'email', 'skills', 'experience', 'country',)

    # Fields to filter the list view by
    list_filter = ('name','country', 'skills', 'experience')

    # Fields to search by in the search box
    search_fields = ('name','country', 'skills', 'experience' )

admin.site.register(IndividualRegistration, IndividualRegistrationAdmin )
admin.site.register(JobPosting)
admin.site.register(Recommendation)
