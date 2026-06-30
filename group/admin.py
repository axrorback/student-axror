from django.contrib import admin
from .models import Group, GroupMember

class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 3
    raw_id_fields = ("student",)
    autocomplete_fields = ("student",)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "total_members")
    search_fields = ("name",)
    inlines = [GroupMemberInline]

    def total_members(self, obj):
        return obj.members.count()
    total_members.short_description = "A'zolar soni"

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("group", "student", "joined_at", "is_admin", "is_muted")
    list_filter = ("group", "is_admin", "is_muted")
    search_fields = ("student__full_name", "group__name")