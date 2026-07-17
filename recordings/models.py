import uuid
from django.db import models
from django.contrib.auth.models import User
from lessons.models import Lesson



class LessonRecording(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)

    lesson = models.OneToOneField(Lesson,on_delete=models.CASCADE,related_name="recording",)

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    video = models.FileField(upload_to="lesson_recordings/")

    uploaded_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,)

    duration = models.DurationField(null=True,blank=True,)

    size = models.BigIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title