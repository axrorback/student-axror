from django.db import models
import uuid
from django.contrib.auth.models import User
from accounts.models import StudentProfile



class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"
        CANCELLED = "cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    student = models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name="orders")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=Status,default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}-{self.status}-{self.student.auid}"