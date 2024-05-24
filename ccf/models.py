from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import (
    get_object_or_404,
)
import datetime


def get_default_date():
    return datetime.date(1974, 12, 6)


# each class in the model corresponds to a database table
class Client(models.Model):
    # each attribute corresponds to a field in the table
    #
    # CharField: single-line text
    friendly_name = models.CharField(max_length=24)
    # timezone.now: time when client is added
    date_added = models.DateTimeField(default=timezone.now)
    # CASCADE: if user is deleted, then all clients will be deleted as well
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=12, default='')
    mobile = models.CharField(max_length=12, default='')
    email = models.EmailField(max_length=50, default='')
    profession = models.CharField(max_length=50, default='')
    dob = models.DateField(default=get_default_date)

    def __str__(self):
        return self.friendly_name

    def get_detail_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse('ccf:client-detail', kwargs={'pk': self.pk})


class Note(models.Model):
    # CharField: single-line text
    title = models.CharField(max_length=100)
    # TextField: multi-line text
    content = models.TextField()
    # this will be updated when the note is edited
    date_updated = models.DateTimeField(default=timezone.now)
    # CASCADE: if client is deleted, then all notes will be deleted as well
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_queryset(self):
        client = get_object_or_404(client=self.kwargs.get('client'))
        return Note.objects.filter(client=client).order_by('-date_updated')

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse('ccf:note-detail', kwargs={'pk': self.pk})


class Treatment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # this will not be updated when the treatment is edited
    date_treated = models.DateTimeField(default=timezone.now)
    # CASCADE: if client is deleted, then all treatments will be deleted as well
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_queryset(self):
        client = get_object_or_404(client=self.kwargs.get('client'))
        return Note.objects.filter(client=client).order_by('-date_treated')

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse('ccf:note-detail', kwargs={'pk': self.pk})
