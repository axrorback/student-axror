# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .decorators import student_required
from .forms import LoginForm, FeedbackForm
from .models import AllowedStudents, StudentProfile
from .services.acharya_api import acharya_authenticate, acharya_get_student_details, AcharyaAuthError


def student_login_view(request):
    if request.session.get("student_auid"):
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"].strip()
        password = form.cleaned_data["password"]

        try:
            auth = acharya_authenticate(username, password)
        except AcharyaAuthError as e:
            messages.error(request, str(e))
            return render(request, "accounts/login.html", {"form": form})

        auid = auth["auid"]

        allowed = AllowedStudents.objects.filter(auid=auid).first()
        if not allowed:
            messages.error(request, "Siz talaba emassiz bu tizimda, uzr.")
            return render(request, "accounts/login.html", {"form": form})

        if not allowed.is_active:
            messages.error(request, allowed.deny_message)
            return render(request, "accounts/login.html", {"form": form})

        try:
            details = acharya_get_student_details(auid=auid, token=auth["token"])
        except AcharyaAuthError as e:
            messages.error(request, str(e))
            return render(request, "accounts/login.html", {"form": form})

        with transaction.atomic():
            profile, _ = StudentProfile.objects.get_or_create(
                auid=auid,
                defaults={
                    "user_id": auth.get("user_id"),
                }
            )
            profile.user_id = auth.get("user_id")
            profile.student_id = details.get("student_id")
            profile.full_name = details.get("full_name", "")
            profile.acharya_email = details.get("acharya_email")
            profile.mobile = details.get("mobile", "")
            profile.program_name = details.get("program_name", "")
            profile.specialization = details.get("specialization", "")
            profile.ac_year = details.get("ac_year", "")
            profile.current_city = details.get("current_city", "")
            profile.last_synced_at = timezone.now()
            profile.save()

        request.session["student_auid"] = auid
        request.session["acharya_token"] = auth["token"]
        request.session["student_profile_id"] = str(profile.id)

        return redirect("profile")

    return render(request, "accounts/login.html", {"form": form})


def student_logout_view(request):
    request.session.flush()
    return redirect("student_login")

@student_required
def profile_view(request):
    auid = request.session["student_auid"]
    profile = StudentProfile.objects.filter(auid=auid).first()

    if not profile:
        return redirect("student_login")

    return render(request, "accounts/profile.html", {"profile": profile})


@student_required
def feedback_create_view(request):
    auid = request.session["student_auid"]

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.auid = auid
            obj.save()
            messages.success(request, "Feedback qabul qilindi. Rahmat!")
            return redirect("feedback")
    else:
        form = FeedbackForm()

    return render(request, "accounts/feedback.html", {"form": form})