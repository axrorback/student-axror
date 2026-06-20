import uuid
from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=120,unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="teaching_groups")
    image = models.ImageField(upload_to="groups/",blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GroupMember(models.Model):

    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="members")
    student = models.ForeignKey("accounts.StudentProfile",on_delete=models.CASCADE,related_name="groups")
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("group", "student")