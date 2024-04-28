import os
from django.db import models
from django.contrib.auth.models import User

profile_pics_dir = 'profile_pics'
default_profile_pic = os.path.join(profile_pics_dir, 'default.png')


class Profile(models.Model):
    # connect out user model to django's user model
    # on delete, delete everything i.e. cascade
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend the model with a profile picture
    image = models.ImageField(
        default=default_profile_pic,
        upload_to=profile_pics_dir,
    )

    def __str__(self):
        return f'{self.user.username} Profile'
