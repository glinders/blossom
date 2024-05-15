from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# each class in the model corresponds to a database table
class Client(models.Model):
    # each attribute corresponds to a field in the table
    #
    # CharField: single-line text
    friendly_name = models.CharField(max_length=100)
    # timezone.now: time when client is added
    date_added = models.DateTimeField(default=timezone.now)
    # CASCADE: if user is deleted, then all clients will be deleted as well
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.friendly_name

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

    def get_absolute_url(self):
        # page to redirect to after creating new object
        return reverse('ccf:note-detail', kwargs={'pk': self.pk})
