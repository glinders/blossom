from django.contrib import admin
from .models import Post

# Register our models here, so we can access them on the admin site
admin.site.register(Post)
