from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserInfoForm, BusinessRegistrationForm, IndividualRegistrationForm, JobPostingForm
from .models import BusinessRegistration, JobPosting, Recommendation, UserInfo
from django.contrib.auth.hashers import check_password
from .jobs1 import recommend_jobs
from django.contrib import messages

def welcome(request):
    return render(request, 'welcome.html')

def choice(request):
    return render(request, 'choice.html')

def registration(request):
    if request.method == 'POST':
        user_type = request.POST.get('userType')
        if user_type == 'business':
            form = BusinessRegistrationForm(request.POST)
            success_message = "Business registration successful!"
        else:
            form = IndividualRegistrationForm(request.POST)
            success_message = "Individual registration successful!"
        
        if form.is_valid():
            form.save()
            messages.success(request, success_message)  # Add a success message
            return redirect('welcome')  # Redirect to the welcome page upon successful form submission
    else:
        form = BusinessRegistrationForm()  # Default to business registration form

    return render(request, 'registration.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if form.is_valid() and user_info_form.is_valid():
            user = form.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            login(request, user)
            messages.success(request, 'Successfully signed up!')
            return redirect('view_profile', username=user.username)
    else:
        form = UserRegistrationForm()
        user_info_form = UserInfoForm()
    
    return render(request, 'signup.html', {'form': form, 'user_info_form': user_info_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('view_profile', username=user.username)
        else:
        
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('welcome')

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInfo, user=user)
    return render(request, 'viewprofile.html', {'user': user, 'user_info': user_info})



# @login_required
# def recommendations(request):
#     user = request.user
#     # Assuming user has a profile with a skills attribute as a comma-separated string
#     user_skills = user.skills.split(", ")

#     # Filter businesses based on user skills
#     recommendations = BusinessRegistration.objects.filter(skills__name__in=user_skills).distinct()  # Assuming 'skills' is a ManyToMany field

#     return render(request, 'recommendations.html', {
#         'recommendations': recommendations
#     })

@login_required
def recommend_jobs_route(request):
    user_info = get_object_or_404(UserInfo, user=request.user)
    recommendations = recommend_jobs(user_info.skills, user_info.designation, user_info.experience)
    
    if not recommendations:
        recommendations = [{"message": "No recommendations found!"}]
    else:
        for job in recommendations:
            company_id = job.get('company id')
            job_id = int(job.get('job id'))
            if company_id:
                try:
                    company_info = BusinessRegistration.objects.get(id=company_id)
                    job['Company'] = company_info.org_name
                    job['Domain'] = company_info.industry
                except BusinessRegistration.DoesNotExist:
                    job['Company'] = 'Unknown'
                    job['Domain'] = 'Unknown'

            try:
                Recommendation.objects.get_or_create(
                    user=user_info,
                    job=JobPosting.objects.get(id=job_id)
                )
            except JobPosting.DoesNotExist:
                pass  # Skip if the job posting does not exist

    # Fetch all business registrations to display on the page
    businesses = BusinessRegistration.objects.all()

    return render(request, 'recommendations.html', {
        'recommendations': recommendations,
        'username': request.user.username,
        'businesses': businesses
    })

def recruiter_login(request):
    if request.method == 'POST':
        company_id = request.POST.get('companyid')
        company_password = request.POST.get('companypassword')
        try:
            company = BusinessRegistration.objects.get(id=company_id)
            if check_password(company_password, company.password):
                request.session['company_id'] = company.id
                return redirect('dashboard')
            else:
                return render(request, 'recruiter_login.html', {'error': 'Invalid credentials'})
        except BusinessRegistration.DoesNotExist:
            return render(request, 'recruiter_login.html', {'error': 'Invalid credentials'})
    return render(request, 'recruiter_login.html')

@login_required
def dashboard(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('recruiter_login')
    company = get_object_or_404(BusinessRegistration, id=company_id)
    return render(request, 'dashboard.html', {'company': company})

@login_required
def job_postings(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('recruiter_login')
    jobs = JobPosting.objects.filter(company_id=company_id)
    return render(request, 'job_postings.html', {'jobs': jobs})

@login_required
def candidates(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('recruiter_login')
    recommendations = Recommendation.objects.filter(job__company_id=company_id)
    return render(request, 'candidates.html', {'recommendations': recommendations})

@login_required
def create_job_posting(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('recruiter_login')
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.company_id = company_id
            job_posting.save()
            return redirect('job_postings')
    else:
        form = JobPostingForm()
    return render(request, 'create_job_posting.html', {'form': form})
