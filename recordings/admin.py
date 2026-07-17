from django.contrib import admin

from .models import LessonRecording


@admin.register(LessonRecording)
class LessonRecordingAdmin(admin.ModelAdmin):
    list_display = ('lesson','created_at','uploaded_by')