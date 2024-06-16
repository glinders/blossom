from django.contrib import admin
from .models import (
    Client, Note, Treatment, Medical, Consultation,
)

# Register our models here, so we can access them on the admin site
admin.site.register((Client, Note, Treatment, Medical, Consultation))

