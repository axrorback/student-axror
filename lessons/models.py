# lessons/models.py
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User
class LessonStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    DONE = "DONE", "Done"
    CANCELED = "CANCELED", "Canceled"

class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)               # Bugungi mavzu
    starts_at = models.DateTimeField()                     # boshlanish vaqti
    ends_at = models.DateTimeField()                       # tugash vaqti
    location = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)                 # mavzu detail / notes
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teachers")
    status = models.CharField(
        max_length=12,
        choices=LessonStatus,
        default=LessonStatus.SCHEDULED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-starts_at",)

    def __str__(self):
        return f"{self.title} ({self.starts_at:%Y-%m-%d})"

    @property
    def is_today(self):
        local_now = timezone.localtime(timezone.now())
        return timezone.localtime(self.starts_at).date() == local_now.date()
