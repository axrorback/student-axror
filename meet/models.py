import uuid
from django.db import models
from lessons.models import Lesson

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    lesson = models.OneToOneField(Lesson,on_delete=models.CASCADE,related_name="meeting")
    room_name = models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name