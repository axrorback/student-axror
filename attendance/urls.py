from django.urls import path
from .views import teacher_lessons_view, teacher_attendance_view

urlpatterns = [
    path("teacher/lessons/", teacher_lessons_view, name="teacher_lessons"),
    path("teacher/lessons/<uuid:lesson_id>/attendance/", teacher_attendance_view, name="teacher_attendance"),
]
