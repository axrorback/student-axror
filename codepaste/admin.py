from django.contrib import admin
from .models import CodePaste

@admin.register(CodePaste)
class CodePasteAdmin(admin.ModelAdmin):
    list_display = ['user','language','is_active','is_expired']