import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Projects(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_title = models.CharField(max_length=200, blank=True)
    p_category = models.CharField(max_length=100, blank=True,)
    p_language = models.CharField(max_length=100, blank=True, )
    p_description = models.TextField(blank=True, )
    p_owner = models.CharField(max_length=20, blank=True, )
    p_status = models.CharField(max_length=50, blank=True, default='pending')
    p_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['p_id']


class SystemUsers(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_firstname = models.CharField(max_length=100, blank=True)
    s_lastname = models.CharField(max_length=100, blank=True,)
    s_phone = models.CharField(max_length=20, blank=True, )
    s_email = models.CharField(max_length=100, blank=True, )
    s_passwd = models.CharField(max_length=100, blank=True, )
    s_country = models.CharField(max_length=100, blank=True, )
    s_role = models.CharField(max_length=50, blank=True, )
    s_status = models.CharField(max_length=50, blank=True, default='inactive')
    c_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['s_id']


class Categories(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=150, blank=True)
    c_description = models.CharField(max_length=250, blank=True,)
    c_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['c_id']


class Posts(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_title = models.CharField(max_length=250, blank=True)
    p_title_tag = models.CharField(max_length=250, blank=True)
    p_author = models.CharField(max_length=100, blank=True)
    p_body = models.TextField(blank=True)
    p_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['p_id']


class Articles(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_title = models.CharField(max_length=250, blank=True)
    a_tag = models.CharField(max_length=250, blank=True)
    a_author = models.CharField(max_length=100, blank=True)
    a_body = models.TextField(blank=True)

    class Meta:
        ordering = ['a_id']


class Support(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_category = models.CharField(max_length=100, null=True)
    s_email = models.CharField(max_length=100, null=True)
    s_message = models.TextField(blank=True, null=True)
    s_status = models.CharField(max_length=10, null=True, default='0')
    s_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['s_id']
