from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Client, Medical, Consultation,
)


@receiver(post_save, sender=Client)
def create_medical(sender, instance, created, **kwarg):
    if created:
        Medical.objects.create(client=instance)


def save_medical(sender, instance, **kwarg):
    instance.medical.save()


@receiver(post_save, sender=Client)
def create_consultation(sender, instance, created, **kwarg):
    if created:
        Consultation.objects.create(client=instance)


def save_consultation(sender, instance, **kwarg):
    instance.consultation.save()
