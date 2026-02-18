# attendance/admin.py
from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("lesson", "student", "status", "marked_at")
    list_filter = ("status", "lesson")
    search_fields = ("student__auid", "student__full_name", "lesson__title")
    ordering = ("-marked_at",)
    autocomplete_fields = ("lesson", "student")
