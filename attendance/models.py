# attendance/models.py
from django.db import models
from django.utils import timezone
import uuid
from accounts.models import StudentProfile
from lessons.models import Lesson

class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"
    LATE = "LATE", "Late"
    EXCUSED = "EXCUSED", "Excused"

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attendances")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances")

    status = models.CharField(max_length=10, choices=AttendanceStatus, default=AttendanceStatus.ABSENT)
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("lesson", "student")
        ordering = ("student__auid",)

    def __str__(self):
        return f"{self.lesson_id} - {self.student.auid} - {self.status}"
