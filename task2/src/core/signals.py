from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils import timezone

from .models import PlayerLevel


@receiver(pre_save, sender=PlayerLevel)
def assign_date(sender, instance, **kwargs):
    if instance.completed is None and instance.is_completed:
        instance.completed = timezone.now().date()


@receiver(post_save, sender=PlayerLevel)
def assign_prize(sender, instance, **kwargs):
    if instance.is_completed:
        instance.assign_prize()
