from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import (
    UserRegistrationForm,
    UserInfoForm,
    BusinessRegistrationForm,
    IndividualRegistrationForm,
    JobPostingForm,
)
from .models import BusinessRegistration, JobPosting, Recommendation, UserInfo
from django.contrib.auth.hashers import check_password
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .jobs1 import recommend_jobs
from .forms import RecruiterLoginForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils import translation
from .recommendation_engine import recommend_jobs

import logging

logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, "welcome.html")


def choice(request):
    return render(request, "choice.html")


def registration(request):
    if request.method == "POST":
        user_type = request.POST.get("userType")
        if user_type == "business":
            form = BusinessRegistrationForm(request.POST)
            success_message = "Business registration successful!"
        else:
            form = IndividualRegistrationForm(request.POST)
            success_message = "Individual registration successful!"

        if form.is_valid():
            form.save()
            messages.success(request, success_message)  # Add a success message
            return redirect(
                "welcome"
            )  # Redirect to the welcome page upon successful form submission
    else:
        form = BusinessRegistrationForm()  # Default to business registration form

    return render(request, "registration.html", {"form": form})


def user_signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if form.is_valid() and user_info_form.is_valid():
            user = form.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            login(request, user)
            messages.success(request, "Successfully signed up!")
            return redirect("view_profile", username=user.username)
    else:
        form = UserRegistrationForm()
        user_info_form = UserInfoForm()

    return render(
        request, "signup.html", {"form": form, "user_info_form": user_info_form}
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully logged in  User    {username}!")
            return redirect("view_profile", username=user.username)
        else:

            return render(
                request, "login.html", {"error": "Invalid username or password"}
            )
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("welcome")


@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInfo, user=user)
    return render(request, "viewprofile.html", {"user": user, "user_info": user_info})


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
    # Get the logged-in user's information
    user_info = get_object_or_404(UserInfo, user=request.user)

    # Get job recommendations based on user's skills, designation, and experience
    recommendations = recommend_jobs(
        user_info.skills, user_info.designation, user_info.experience
    )

    # If no recommendations are found, return a default message
    if not recommendations:
        recommendations = [{"message": "No recommendations found!"}]
    else:
        for job in recommendations:
            company_id = job.get("company id")
            job_id = int(job.get("job id", 0))  # Ensure job_id is an integer

            if company_id:
                try:
                    company_info = BusinessRegistration.objects.get(id=company_id)
                    job["Company"] = company_info.org_name
                    job["Domain"] = company_info.industry
                except BusinessRegistration.DoesNotExist:
                    job["Company"] = "Unknown"
                    job["Domain"] = "Unknown"

            # Add the recommendation to the database if it doesn't exist
            try:
                job_post = JobPosting.objects.get(id=job_id)
                Recommendation.objects.get_or_create(user=user_info, job=job_post)
            except JobPosting.DoesNotExist:
                pass  # Skip if the job posting does not exist

    # Filter business registrations based on user's skills only (ignoring experience)
    businesses = BusinessRegistration.objects.filter(
        Q(skills__icontains=user_info.skills)  # Only match based on skills
    ).distinct()

    # Pass the data to the template
    context = {
        "recommendations": recommendations,
        "username": request.user.username,
        "businesses": businesses,
    }

    return render(request, "recommendations.html", context)


def recruiter_login(request):
    if request.method == "POST":
        form = RecruiterLoginForm(request.POST)
        if form.is_valid():
            company_id = form.cleaned_data["companyid"]
            company_password = form.cleaned_data["companypassword"]

            try:
                company = BusinessRegistration.objects.get(id=company_id)
                if check_password(company_password, company.password):
                    request.session["company_id"] = company.id
                    messages.success(
                        request, f"Successfully logged in to  {company.org_name }!"
                    )
                    return redirect(
                        "dashboard"
                    )  # Redirect directly to dashboard after success
                else:
                    return render(
                        request,
                        "recruiter_login.html",
                        {"form": form, "error": "incorrect_password"},
                    )
            except BusinessRegistration.DoesNotExist:
                return render(
                    request,
                    "recruiter_login.html",
                    {"form": form, "error": "id_not_found"},
                )
    else:
        form = RecruiterLoginForm()

    return render(request, "recruiter_login.html", {"form": form})


@login_required
def dashboard(request):
    company_id = request.session.get("company_id")
    if not company_id:
        return redirect("recruiter_login")

    company = get_object_or_404(BusinessRegistration, id=company_id)
    return render(request, "dashboard.html", {"company": company})


@login_required
def job_postings(request):
    # Get the company ID from the logged-in user's session
    company_id = request.session.get("company_id")

    # Retrieve the specific company based on the logged-in user's company ID
    company = BusinessRegistration.objects.get(id=company_id)

    # Retrieve job postings only for the logged-in company
    job_data = JobPosting.objects.filter(company_id=company_id)

    context = {
        "jobs": job_data,  # Pass only the job postings for the logged-in company
        "company": company,  # Pass the company details to the template
    }
    return render(request, "job_postings.html", context)


@login_required
def candidates(request):
    # Get the company ID from the session
    company_id = request.session.get("company_id")
    if not company_id:
        return redirect("recruiter_login")

    # Get job postings for the logged-in company
    job_postings = JobPosting.objects.filter(company_id=company_id)

    # Collect the skills from the job postings
    job_skills = set(
        skill.strip() for job in job_postings for skill in job.skills.split(",")
    )

    # Get recommendations based on the skills from job postings
    recommendations = (
        Recommendation.objects.filter(user__skills__in=job_skills, job__in=job_postings)
        .select_related("user", "job__company")
        .distinct()
    )

    return render(request, "candidates.html", {"recommendations": recommendations})


# login_required
# def create_job_posting(request):
#     if request.method == 'POST':
#         form = JobPostingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Job posting created successfully.')
#             return redirect('dashboard')  # Redirect to the dashboard
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = JobPostingForm()

#     return render(request, 'create_job_posting.html', {'form': form})
login_required


class create_job_posting(CreateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = "create_job_posting.html"
    success_url = reverse_lazy("job_postings")

    # Override form_valid to assign the logged-in company automatically
    def form_valid(self, form):
        # Get the logged-in user's company from the session
        company_id = self.request.session.get("company_id")
        if company_id:
            # Retrieve the company and assign it to the form instance
            company = BusinessRegistration.objects.get(id=company_id)
            form.instance.company = company  # Assign the company to the job posting
            # Call the parent form_valid method
            response = super().form_valid(form)
            # Add a success message after the job posting is successfully created
            messages.success(self.request, "Job posting created successfully!")
            return response
        else:
            # Handle missing company in session, redirect to error page
            messages.error(
                self.request,
                "Unable to create job posting. Company not found in session.",
            )
            return redirect("error")

    def get_context_data(self, **kwargs):
        # Add the company to the form context so it can be displayed in the template if needed
        context = super().get_context_data(**kwargs)
        company_id = self.request.session.get("company_id")
        context["company"] = BusinessRegistration.objects.get(id=company_id)
        return context


# def set_language(request):
#     user_language = request.POST.get("language")
#     translation.activate(user_language)
#     request.session[translation.LANGUAGE_SESSION_KEY] = user_language
#     logger.debug(f"Language set to {user_language}")
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
