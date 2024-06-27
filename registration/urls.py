# placement/urls.py
from django.contrib import admin
from django.urls import path
from  . import views

urlpatterns = [
    
    path('', views.welcome, name='welcome'),
    path('choice/', views.choice, name='choice'),
    path('registration/', views.registration, name='registration'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('view_profile/<str:username>/', views.view_profile, name='view_profile'),
    path('recommend_jobs/', views.recommend_jobs_route, name='recommend_jobs'),
    path('recruiter_login/', views.recruiter_login, name='recruiter_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job_postings/', views.job_postings, name='job_postings'),
    path('candidates/', views.candidates, name='candidates'),
    path('create_job_posting/', views.create_job_posting, name='create_job_posting'),
]
