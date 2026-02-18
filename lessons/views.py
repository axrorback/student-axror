# lessons/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from accounts.decorators import student_required
from .models import Lesson, LessonStatus


@student_required
def dashboard_view(request):
    """
    Student dashboard:
    - Bugungi dars (agar bo'lsa)
    - Yaqqin kelayotgan dars (agar bugun yo'q bo'lsa)
    """
    now = timezone.localtime(timezone.now())
    today = now.date()

    today_lesson = (
        Lesson.objects
        .filter(starts_at__date=today)
        .exclude(status=LessonStatus.CANCELED)
        .order_by("starts_at")
        .first()
    )

    upcoming_lesson = None
    if not today_lesson:
        upcoming_lesson = (
            Lesson.objects
            .filter(starts_at__gt=now)
            .exclude(status=LessonStatus.CANCELED)
            .order_by("starts_at")
            .first()
        )

    return render(request, "lessons/dashboard.html", {
        "today_lesson": today_lesson,
        "upcoming_lesson": upcoming_lesson,
        "now": now,
    })


@student_required
def lessons_list_view(request):
    """
    Student lessons page:
    - Upcoming (starts_at >= now)
    - Past (ends_at < now) yoki status DONE
    """
    now = timezone.localtime(timezone.now())

    upcoming = (
        Lesson.objects
        .filter(starts_at__gte=now)
        .exclude(status=LessonStatus.CANCELED)
        .order_by("starts_at")
    )

    past = (
        Lesson.objects
        .filter(Q(ends_at__lt=now) | Q(status=LessonStatus.DONE))
        .exclude(status=LessonStatus.CANCELED)
        .order_by("-starts_at")
    )

    return render(request, "lessons/lessons_list.html", {
        "upcoming": upcoming,
        "past": past,
    })


@student_required
def lesson_detail_view(request, pk: int):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, "lessons/lesson_detail.html", {"lesson": lesson})
