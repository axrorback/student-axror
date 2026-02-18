# lessons/admin.py
from django.contrib import admin
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import Lesson, LessonStatus


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status_badge",
        "starts_at_local",
        "ends_at_local",
        "duration_min",
        "location",
        "updated_at_local",
    )
    list_filter = ("status", "starts_at")
    search_fields = ("title", "location", "content")
    ordering = ("-starts_at",)
    date_hierarchy = "starts_at"
    list_per_page = 50

    fieldsets = (
        ("Asosiy", {"fields": ("title", "status")}),
        ("Vaqt", {"fields": ("starts_at", "ends_at")}),
        ("Qo‘shimcha", {"fields": ("location", "content")}),
        ("O'qituvchi",{"fields": ("teacher",)}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")

    actions = ("mark_scheduled", "mark_done", "mark_canceled")

    def status_badge(self, obj: Lesson):
        if obj.status == LessonStatus.SCHEDULED:
            return mark_safe('<span class="badge text-bg-primary">SCHEDULED</span>')
        if obj.status == LessonStatus.DONE:
            return mark_safe('<span class="badge text-bg-success">DONE</span>')
        if obj.status == LessonStatus.CANCELED:
            return mark_safe('<span class="badge text-bg-danger">CANCELED</span>')
        return obj.status
    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"

    def starts_at_local(self, obj: Lesson):
        return timezone.localtime(obj.starts_at).strftime("%Y-%m-%d %H:%M")
    starts_at_local.short_description = "Starts"
    starts_at_local.admin_order_field = "starts_at"

    def ends_at_local(self, obj: Lesson):
        return timezone.localtime(obj.ends_at).strftime("%Y-%m-%d %H:%M")
    ends_at_local.short_description = "Ends"
    ends_at_local.admin_order_field = "ends_at"

    def updated_at_local(self, obj: Lesson):
        return timezone.localtime(obj.updated_at).strftime("%Y-%m-%d %H:%M")
    updated_at_local.short_description = "Updated"
    updated_at_local.admin_order_field = "updated_at"

    def duration_min(self, obj: Lesson):
        try:
            mins = int((obj.ends_at - obj.starts_at).total_seconds() // 60)
            return f"{mins} min"
        except Exception:
            return "—"
    duration_min.short_description = "Duration"

    @admin.action(description="Mark as SCHEDULED")
    def mark_scheduled(self, request, queryset):
        updated = queryset.update(status=LessonStatus.SCHEDULED)
        self.message_user(request, f"{updated} ta dars SCHEDULED qilindi.")

    @admin.action(description="Mark as DONE")
    def mark_done(self, request, queryset):
        updated = queryset.update(status=LessonStatus.DONE)
        self.message_user(request, f"{updated} ta dars DONE qilindi.")

    @admin.action(description="Mark as CANCELED")
    def mark_canceled(self, request, queryset):
        updated = queryset.update(status=LessonStatus.CANCELED)
        self.message_user(request, f"{updated} ta dars CANCELED qilindi.")
