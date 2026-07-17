from django.db.models.signals import post_save
from django.dispatch import receiver

from lessons.models import Lesson

from .services import notify_new_lesson


@receiver(post_save, sender=Lesson)
def lesson_created(sender, instance, created, **kwargs):

    if created:
        notify_new_lesson(instance)