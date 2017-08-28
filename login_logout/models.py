# coding: utf-8

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 
import datetime
from django import forms

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Пример +7(909)555-55-55.")
    phone_number = models.CharField(max_length = 11, validators=[phone_regex], verbose_name=u'Номер телефона')
    email_delivery = models.BooleanField(default = True)
    new_password = models.CharField(max_length=200 ,blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    

class ActivationUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    activation_key = models.CharField(max_length=40, blank = True)
    key_expires = models.DateTimeField(default = datetime.datetime.now())    