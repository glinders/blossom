from django.db import models
from django.utils.text import capfirst
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import (
    get_object_or_404,
)
import datetime
import ccf.symbols


def get_default_date():
    return datetime.date(1970, 1, 1)


# each class in the model corresponds to a database table
class Client(models.Model):
    # each attribute corresponds to a field in the table
    #
    # CharField: single-line text
    display_name = models.CharField(max_length=24)
    # timezone.now: time when client is added
    date_added = models.DateTimeField(default=timezone.now)
    # CASCADE: if user is deleted, then all clients will be deleted as well
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=18, default='')
    mobile = models.CharField(max_length=18, default='')
    email = models.EmailField(max_length=50, default='')
    profession = models.CharField(max_length=50, default='')
    dob = models.DateField(default=get_default_date)

    def __str__(self):
        return self.display_name

    def get_detail_fields(self):
        return [
            (capfirst(field.verbose_name), field.value_from_object(self))
            for field in self._meta.fields
            if field.name not in (
                'id', 'display_name', 'therapist', 'date_added'
            )
        ]

    # return the canonical URL for an object
    def get_absolute_url(self):
        return reverse(
            'ccf:client-detail',
            kwargs={
                'client_id': self.pk,
                'tab': ccf.symbols.CLIENT_TAB_DETAILS
            },
        )


class Medical(models.Model):
    # connect our user model to django's user model
    # on delete, delete everything i.e. cascade
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    # TextField: multi-line text, use kwarg 'verbose_name' to set name
    # displayed in forms (done here as an example)
    allergies = models.TextField(
        verbose_name='Allergies',
        default='',
    )
    chronic_skin_conditions = models.TextField(default='')
    illnesses_and_disorders = models.TextField(default='')
    cosmetic_procedures = models.TextField(default='')
    medications = models.TextField(default='')
    pregnancy = models.TextField(default='')
    # this will be updated when the note is edited
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.client.display_name} Medical'

    def get_detail_fields(self):
        return [
            (capfirst(field.verbose_name), field.value_from_object(self))
            for field in self._meta.fields
            if field.name not in (
                'id', 'client', 'date_updated'
            )
        ]

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse(
            'ccf:client-detail',
            kwargs={
                'client_id': self.pk,
                'tab': ccf.symbols.CLIENT_TAB_MEDICAL
            },
        )


class Consultation(models.Model):
    # connect our user model to django's user model
    # on delete, delete everything i.e. cascade
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    # TextField: multi-line text
    skin_type = models.TextField(default='')
    skin_conditions = models.TextField(default='')
    concerns = models.TextField(default='')
    lash_colour = models.TextField(default='')
    eyebrow_colour = models.TextField(default='')
    # this will be updated when the note is edited
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.client.display_name} Consultation'

    def get_detail_fields(self):
        data = [
            (capfirst(field.verbose_name), field.value_from_object(self))
            for field in self._meta.fields
            if field.name not in (
                'id', 'client', 'date_updated'
            )
        ]
        return data

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse(
            'ccf:client-detail',
            kwargs={
                'client_id': self.pk,
                'tab': ccf.symbols.CLIENT_TAB_CONSULTATION
            },
        )


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

    # our generic templates use 'generic_object.display_name'
    # to refer to the instance name
    @property
    def display_name(self):
        return self.title

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse(
            'ccf:note-detail',
            kwargs={
                'client_id': self.client_id,
                'pk': self.pk,
            }
        )


class Treatment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # this will not be updated when the treatment is edited
    date_treated = models.DateTimeField(default=timezone.now)
    # CASCADE: if client is deleted, then all treatments will be deleted as well
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # our generic templates use 'generic_object.display_name'
    # to refer to the instance name
    @property
    def display_name(self):
        return self.title

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse(
            'ccf:treatment-detail',
            kwargs={
                'client_id': self.client_id,
                'pk': self.pk,
            }
        )
