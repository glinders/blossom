import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


profile_pics_dir = 'profile_pics'
default_profile_pic = os.path.join(profile_pics_dir, 'default.png')


class Profile(models.Model):
    # connect our user model to django's user model
    # on delete, delete everything i.e. cascade
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend the model with a profile picture
    image = models.ImageField(
        default=default_profile_pic,
        upload_to=profile_pics_dir,
    )

    def save(self):
        # first save image
        super().save()
        # get current image
        img = Image.open(self.image.path)
        # then resize image to save space & reduce load time
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'
