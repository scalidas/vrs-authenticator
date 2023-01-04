from django.contrib import admin
from .models import GoogleUser, CustomSession

# Register your models here.
admin.site.register(GoogleUser)
admin.site.register(CustomSession)