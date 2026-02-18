# accounts/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import AllowedStudents, StudentProfile , Feedback


@admin.register(AllowedStudents)
class AllowedStudentAdmin(admin.ModelAdmin):
    list_display = ("auid", "is_active", "deny_message_short", "updated_at_display")
    list_filter = ("is_active",)
    search_fields = ("auid", "notes", "deny_message")
    ordering = ("auid",)
    list_per_page = 50

    fields = ("auid", "is_active", "deny_message", "notes","created_by")
    actions = ("activate_students", "deactivate_students", "set_default_deny_message")

    def deny_message_short(self, obj):
        msg = (obj.deny_message or "").strip()
        return (msg[:60] + "…") if len(msg) > 60 else msg
    deny_message_short.short_description = "Deny message"

    def updated_at_display(self, obj):
        if hasattr(obj, "updated_at") and obj.updated_at:
            return timezone.localtime(obj.updated_at).strftime("%Y-%m-%d %H:%M")
        return "—"
    updated_at_display.short_description = "Updated"

    @admin.action(description="✅ Activate selected students")
    def activate_students(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} ta student activate qilindi.")

    @admin.action(description="⛔ Deactivate selected students")
    def deactivate_students(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} ta student deactivate qilindi.")

    @admin.action(description="📝 Set default deny message for selected")
    def set_default_deny_message(self, request, queryset):
        default_msg = "Siz ushbu tizimga kira olmaysiz. Admin bilan bog‘laning."
        updated = queryset.update(deny_message=default_msg)
        self.message_user(request, f"{updated} ta student uchun deny message default qilindi.")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "auid",
        "full_name",
        "acharya_email",
        "mobile",
        "program_name",
        "specialization",
        "ac_year",
        "current_city",
        "student_id",
        "user_id",
        "last_synced_at",
    )
    search_fields = (
        "auid",
        "full_name",
        "acharya_email",
        "mobile",
        "program_name",
        "specialization",
        "ac_year",
        "current_city",
    )
    list_filter = ("ac_year", "program_name", "specialization", "current_city")
    ordering = ("auid",)
    list_per_page = 50

    # Profil datalarini admin panelda "faqat ko‘rish" qilish (xohlasangiz)
    readonly_fields = (
        "auid",
        "user_id",
        "student_id",
        "full_name",
        "acharya_email",
        "mobile",
        "program_name",
        "specialization",
        "ac_year",
        "current_city",
        "last_synced_at",
    )

    fieldsets = (
        ("Identity", {"fields": ("auid", "user_id", "student_id")}),
        ("Main", {"fields": ("full_name", "acharya_email", "mobile")}),
        ("Academic", {"fields": ("program_name", "specialization", "ac_year", "current_city")}),
        ("System", {"fields": ("last_synced_at",)}),
    )

    actions = ("force_resync_hint",)

    @admin.action(description="ℹ️ Resync: (eslatma) login qilganda avtomatik yangilanadi")
    def force_resync_hint(self, request, queryset):
        self.message_user(
            request,
            "Resync hozircha action bilan emas. Student qayta login qilsa profil data avtomatik yangilanadi."
        )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "short_id",
        "auid",
        "short_feedback",
        "created_at_local",
    )

    search_fields = ("auid", "feedback")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("id", "auid", "feedback", "created_at")
    date_hierarchy = "created_at"
    list_per_page = 50

    fieldsets = (
        ("Feedback Info", {
            "fields": ("id", "auid", "feedback"),
        }),
        ("Meta", {
            "fields": ("created_at",),
        }),
    )

    # ---- Pretty display helpers ----

    def short_id(self, obj):
        return str(obj.id)[:8]
    short_id.short_description = "ID"

    def short_feedback(self, obj):
        if len(obj.feedback) > 60:
            return obj.feedback[:60] + "..."
        return obj.feedback
    short_feedback.short_description = "Feedback"

    def created_at_local(self, obj):
        return timezone.localtime(obj.created_at).strftime("%Y-%m-%d %H:%M")
    created_at_local.short_description = "Created"
    created_at_local.admin_order_field = "created_at"