from django.db import models
import uuid
from django.utils import timezone

class AssignmentStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    CLOSED = "CLOSED", "Closed"

class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.OneToOneField(
        "lessons.Lesson",
        on_delete=models.CASCADE,
        related_name="assignment"
    )
    title = models.CharField(max_length=255)
    instructions = models.TextField(blank=True)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=12,
        choices=AssignmentStatus,
        default=AssignmentStatus.PUBLISHED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.lesson.title}"

    @property
    def is_deadline_passed(self):
        return timezone.now() > self.deadline



class SubmissionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"

class AssignmentSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        "accounts.StudentProfile",
        on_delete=models.CASCADE,
        related_name="assignment_submissions"
    )

    github_link = models.URLField(unique=True)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=12,
        choices=SubmissionStatus,
        default=SubmissionStatus.PENDING,
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_submissions"
    )

    review_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("assignment", "student")
        ordering = ("-submitted_at",)

    def __str__(self):
        return f"{self.student.auid} - {self.assignment.title}"