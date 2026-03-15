from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib import messages

from accounts.decorators import student_required
from attendance.models import Attendance, AttendanceStatus
from accounts.models import StudentProfile
from homework.models import (
    Assignment,
    AssignmentSubmission,
    SubmissionStatus,

)
from .models import Lesson , LessonStatus
from .forms import AssignmentSubmissionForm


def get_current_student(request):
    auid = request.session.get("student_auid")
    if not auid:
        return None
    return StudentProfile.objects.filter(auid=auid).first()


def get_attendance_for_student(lesson, student):
    if not student:
        return None
    return Attendance.objects.filter(
        lesson=lesson,
        student=student
    ).first()


def get_assignment_for_lesson(lesson):
    return Assignment.objects.filter(lesson=lesson).first()


def get_submission_for_student(assignment, student):
    if not assignment or not student:
        return None
    return AssignmentSubmission.objects.filter(
        assignment=assignment,
        student=student
    ).select_related("reviewed_by").first()


def can_student_submit(student, assignment):
    """
    Student submission qila olishi uchun:
    1. Assignment mavjud bo'lishi kerak
    2. Deadline o'tmagan bo'lishi kerak
    3. Student shu lesson uchun PRESENT yoki LATE bo'lishi kerak
    """
    if not assignment:
        return False, "Vazifa mavjud emas."

    if timezone.now() > assignment.deadline:
        return False, "Vazifa deadline tugagan."

    attendance_exists = Attendance.objects.filter(
        lesson=assignment.lesson,
        student=student,
        status__in=[AttendanceStatus.PRESENT, AttendanceStatus.LATE]
    ).exists()

    if not attendance_exists:
        return False, "Siz bu darsda qatnashmagansiz, shu sabab topshira olmaysiz."

    return True, None


@student_required
def dashboard_view(request):
    """
    Student dashboard:
    - Bugungi dars (agar bo'lsa)
    - Bugungi dars uchun attendance
    - Bugungi dars assignmenti
    - Bugungi dars submissioni
    - Agar bugun dars bo'lmasa yaqin upcoming lesson
    """
    now = timezone.localtime(timezone.now())
    today = now.date()

    student = get_current_student(request)
    if not student:
        return redirect("student_login")

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

    today_attendance = None
    today_assignment = None
    today_submission = None
    today_can_submit = False
    today_submit_reason = None

    if today_lesson:
        today_attendance = get_attendance_for_student(today_lesson, student)
        today_assignment = get_assignment_for_lesson(today_lesson)

        if today_assignment:
            today_submission = get_submission_for_student(today_assignment, student)
            today_can_submit, today_submit_reason = can_student_submit(student, today_assignment)

    upcoming_attendance = None
    upcoming_assignment = None
    upcoming_submission = None
    upcoming_can_submit = False
    upcoming_submit_reason = None

    if upcoming_lesson:
        upcoming_attendance = get_attendance_for_student(upcoming_lesson, student)
        upcoming_assignment = get_assignment_for_lesson(upcoming_lesson)

        if upcoming_assignment:
            upcoming_submission = get_submission_for_student(upcoming_assignment, student)
            upcoming_can_submit, upcoming_submit_reason = can_student_submit(student, upcoming_assignment)

    context = {
        "student": student,
        "now": now,

        "today_lesson": today_lesson,
        "today_attendance": today_attendance,
        "today_assignment": today_assignment,
        "today_submission": today_submission,
        "today_can_submit": today_can_submit,
        "today_submit_reason": today_submit_reason,

        "upcoming_lesson": upcoming_lesson,
        "upcoming_attendance": upcoming_attendance,
        "upcoming_assignment": upcoming_assignment,
        "upcoming_submission": upcoming_submission,
        "upcoming_can_submit": upcoming_can_submit,
        "upcoming_submit_reason": upcoming_submit_reason,
    }
    return render(request, "lessons/dashboard.html", context)


@student_required
def lessons_list_view(request):
    """
    Student lessons page:
    - Upcoming lessons
    - Past lessons
    - Har lesson uchun attendance, assignment, submission holati
    """
    now = timezone.localtime(timezone.now())

    student = get_current_student(request)
    if not student:
        return redirect("student_login")

    upcoming_qs = (
        Lesson.objects
        .filter(starts_at__gte=now)
        .exclude(status=LessonStatus.CANCELED)
        .order_by("starts_at")
    )

    past_qs = (
        Lesson.objects
        .filter(Q(ends_at__lt=now) | Q(status=LessonStatus.DONE))
        .exclude(status=LessonStatus.CANCELED)
        .order_by("-starts_at")
    )

    def build_lesson_items(lessons):
        items = []

        for lesson in lessons:
            attendance = get_attendance_for_student(lesson, student)
            assignment = get_assignment_for_lesson(lesson)
            submission = None
            can_submit = False
            submit_reason = None

            if assignment:
                submission = get_submission_for_student(assignment, student)
                can_submit, submit_reason = can_student_submit(student, assignment)

            items.append({
                "lesson": lesson,
                "attendance": attendance,
                "assignment": assignment,
                "submission": submission,
                "can_submit": can_submit,
                "submit_reason": submit_reason,
            })

        return items

    upcoming = build_lesson_items(upcoming_qs)
    past = build_lesson_items(past_qs)

    context = {
        "student": student,
        "upcoming": upcoming,
        "past": past,
        "now": now,
    }
    return render(request, "lessons/lessons_list.html", context)


@student_required
def lesson_detail_view(request, pk):
    """
    Student lesson detail:
    - lesson ma'lumotlari
    - attendance holati
    - assignment
    - student submission
    - submit qila oladimi yoki yo'q
    """
    student = get_current_student(request)
    if not student:
        return redirect("student_login")

    lesson = get_object_or_404(Lesson, pk=pk)

    attendance = get_attendance_for_student(lesson, student)
    assignment = get_assignment_for_lesson(lesson)

    submission = None
    can_submit = False
    submit_reason = None

    if assignment:
        submission = get_submission_for_student(assignment, student)
        can_submit, submit_reason = can_student_submit(student, assignment)

    context = {
        "student": student,
        "lesson": lesson,
        "attendance": attendance,
        "assignment": assignment,
        "submission": submission,
        "can_submit": can_submit,
        "submit_reason": submit_reason,
    }
    return render(request, "lessons/lesson_detail.html", context)


@student_required
def assignment_submit_view(request, assignment_id):
    """
    Student assignment submit/update view
    """
    student = get_current_student(request)
    if not student:
        return redirect("student_login")

    assignment = get_object_or_404(
        Assignment.objects.select_related("lesson"),
        id=assignment_id
    )

    allowed, reason = can_student_submit(student, assignment)
    if not allowed:
        messages.error(request, reason)
        return redirect("lesson_detail", pk=assignment.lesson.pk)

    submission = AssignmentSubmission.objects.filter(
        assignment=assignment,
        student=student
    ).first()

    if request.method == "POST":
        form = AssignmentSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.assignment = assignment
            obj.student = student
            obj.status = SubmissionStatus.PENDING
            obj.review_note = ""
            obj.reviewed_at = None
            obj.reviewed_by = None
            obj.save()

            if submission:
                messages.success(request, "Vazifa yangilandi.")
            else:
                messages.success(request, "Vazifa muvaffaqiyatli topshirildi.")

            return redirect("lesson_detail", pk=assignment.lesson.pk)
    else:
        form = AssignmentSubmissionForm(instance=submission)

    context = {
        "student": student,
        "assignment": assignment,
        "submission": submission,
        "form": form,
    }
    return render(request, "lessons/assignment_submit.html", context)

@student_required
def submission_review_detail_view(request, submission_id):
    submission = get_object_or_404(
        AssignmentSubmission.objects.select_related(
            "assignment",
            "assignment__lesson",
            "student",
            "reviewed_by",
        ),
        id=submission_id
    )

    context = {
        "submission": submission,
        "assignment": submission.assignment,
        "lesson": submission.assignment.lesson,
        "student_profile": submission.student,
    }
    return render(request, "lessons/submission_review_detail.html", context)

@student_required
def leaderboard_view(request):
    leaders = (
        StudentProfile.objects
        .annotate(
            approved_count=Count(
                "assignment_submissions",
                filter=Q(assignment_submissions__status="APPROVED")
            )
        )
        .filter(approved_count__gt=0)
        .order_by("-approved_count", "full_name")
    )

    context = {
        "leaders": leaders
    }
    return render(request, "accounts/leaderboard.html", context)