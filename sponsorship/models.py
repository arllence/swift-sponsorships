from django.db import models
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your models here. hmm :)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.IntegerField(default=0)
    sponsored = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user,self.status)

class Sponsor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user,self.status)

class Bio_Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    birth_certificate = models.FileField(upload_to='birth_certificate')
    national_id = models.FileField(upload_to='national_id')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user,self.status)


class School_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    academic_level = models.CharField(max_length=200)
    completion_year = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user,self.name)


class Reasons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    reason = models.TextField()
    rec_letter = models.FileField(upload_to='rec_letter')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user,self.reason)


class Sponsored(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user_sponsored')
    by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user_sponsoring')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user,self.status)