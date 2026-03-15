from django.db import models
from django.utils import timezone


class CodePaste(models.Model):

    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("html", "HTML"),
        ("shell", "Shell"),
    ]

    user = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return timezone.now() >= self.expire_at