# attendance/views.py
from uuid import UUID

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from accounts.models import StudentProfile
from lessons.models import Lesson, LessonStatus
from .models import Attendance, AttendanceStatus

@staff_member_required
def teacher_lessons_view(request):
    """Teacher: darslar ro'yxati (attendance belgilash uchun)"""
    now = timezone.localtime(timezone.now())

    lessons = (
        Lesson.objects
        .exclude(status=LessonStatus.CANCELED)
        .order_by("-starts_at")[:80]
    )

    return render(request, "attendance/teacher_lessons.html", {"lessons": lessons, "now": now})

@staff_member_required
def teacher_attendance_view(request, lesson_id: UUID):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    students = StudentProfile.objects.order_by("auid")

    existing = Attendance.objects.filter(lesson=lesson, student__in=students)
    existing_map = {a.student_id: a for a in existing}  # key = StudentProfile.pk

    if request.method == "POST":
        updated_count = 0

        with transaction.atomic():
            for s in students:
                key = f"status_{s.id}"
                status = request.POST.get(key)

                if status not in AttendanceStatus.values:
                    continue

                obj = existing_map.get(s.id)
                if obj:
                    if obj.status != status:
                        obj.status = status
                        obj.save(update_fields=["status", "marked_at"])
                        updated_count += 1
                else:
                    Attendance.objects.create(lesson=lesson, student=s, status=status)
                    updated_count += 1

            # ✅ 1 ta query bilan hamma student uchun present/absent countni olish
            stats = (
                Attendance.objects
                .filter(student__in=students)
                .values("student_id")
                .annotate(
                    present=Count("id", filter=Q(status=AttendanceStatus.PRESENT)),
                    absent=Count("id", filter=Q(status=AttendanceStatus.ABSENT)),
                )
            )

            stats_map = {row["student_id"]: row for row in stats}

            # ✅ StudentProfile fieldlarni yangilash
            for s in students:
                row = stats_map.get(s.id, None)
                present = row["present"] if row else 0
                absent = row["absent"] if row else 0

                # faqat o'zgargan bo'lsa update qilsin
                if s.present_count != present or s.absent_count != absent:
                    s.present_count = present
                    s.absent_count = absent
                    s.save(update_fields=["present_count", "absent_count"])

        messages.success(request, f"Attendance saqlandi. O'zgargan/yangi: {updated_count} ta.")
        return redirect("teacher_attendance", lesson_id=lesson.id)

    # GET
    rows = []
    for s in students:
        a = existing_map.get(s.id)
        rows.append({
            "student": s,
            "status": a.status if a else AttendanceStatus.ABSENT,
        })

    return render(request, "attendance/teacher_attendance.html", {
        "lesson": lesson,
        "rows": rows,
        "statuses": AttendanceStatus,
    })