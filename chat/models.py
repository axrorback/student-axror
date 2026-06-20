import uuid
from django.db import models

class ChatRoom(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    group = models.OneToOneField("group.Group",on_delete=models.CASCADE,related_name="chat_room")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group.name

class ChatMessage(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey("accounts.StudentProfile",on_delete=models.CASCADE,related_name="chat_messages")
    message = models.TextField()
    reply_to = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,related_name="replies")
    attachment = models.FileField(upload_to="chat/",blank=True,null=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.auid}"