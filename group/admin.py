from django.contrib import admin
from .models import Group , GroupMember


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','teacher',)

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('group',)
