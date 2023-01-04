from django.db import models

# Create your models here.
class GoogleUser(models.Model):
    sub = models.CharField(max_length=50)
    logins = models.IntegerField()

    def __str__(self):
        return self.sub

class CustomSession(models.Model):
    sessionid = models.CharField(max_length=20)
    expiry = models.DateTimeField()

    def __str__(self):
        return self.sessionid