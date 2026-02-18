from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import ForeignKey

class AllowedStudents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auid = models.CharField(max_length=13)
    creted_at = models.DateTimeField(auto_now_add=True)
    created_by = ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    deny_message = models.TextField(blank=True,default='You are not allowed to access this page please contact Akhrojon')

    def __str__(self):
        return self.auid

class StudentProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    auid = models.CharField(max_length=32, unique=True)  # ABT24CCS008
    user_id = models.IntegerField(null=True, blank=True) # 745 (authenticate'dan)
    student_id = models.IntegerField(null=True, blank=True) # 689 (details'dan)

    full_name = models.CharField(max_length=255, blank=True)
    acharya_email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=32, blank=True)

    program_name = models.CharField(max_length=255, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    ac_year = models.CharField(max_length=50, blank=True)
    current_city = models.CharField(max_length=100, blank=True)

    last_synced_at = models.DateTimeField(auto_now=True)

    present_count = models.PositiveIntegerField(default=0)
    absent_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.auid} — {self.full_name}"