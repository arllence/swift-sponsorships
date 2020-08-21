from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Codes(models.Model):
    code = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.code,self.date_created)

class Sent_Codes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=500)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.code,self.status)