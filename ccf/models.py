from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# each class in the model corresponds to a database table
class Post(models.Model):
    # each attribute corresponds to a field in the table
    #
    # CharField: single-line text
    title = models.CharField(max_length=100)
    # TextField: multi-line text
    content = models.TextField()
    # timezone.now: time when post is created
    date_posted = models.DateTimeField(default=timezone.now)
    # CASCADE: if user is deleted, then all posts will be deleted as well
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
