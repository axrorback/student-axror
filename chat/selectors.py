from django.shortcuts import get_object_or_404
from group.models import Group, GroupMember
from .models import ChatRoom


def get_room(group_id):
    group = get_object_or_404(Group, id=group_id)
    room, _ = ChatRoom.objects.get_or_create(group=group)

    return room


def get_messages(room):

    return room.messages.filter(is_deleted=False).select_related("sender", "reply_to").order_by("created_at")


def is_member(student, room):
    
    return GroupMember.objects.filter(group=room.group,student=student).exists()