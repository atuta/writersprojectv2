import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, country, password=None):
        if not email:
            raise ValueError('Email is required')
        if not first_name:
            raise ValueError('First Name is required')
        if not last_name:
            raise ValueError('Last Name is required')
        if not phone:
            raise ValueError('Phone is required')
        if not country:
            raise ValueError('Country is required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            country=country
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, country, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            country=country,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    last_login = models.DateTimeField(verbose_name="Last Login", blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=120, null=True)
    rating_stars = models.IntegerField(default=0, null=True)
    userrole = models.CharField(max_length=20, default="3", null=True)
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.CharField(max_length=10, default="no", null=True)
    writer_article = models.CharField(max_length=10, default="no", null=True)
    is_archived = models.CharField(max_length=10, default="no", null=True)
    otp_string = models.CharField(max_length=120, null=True)
    c_wallet_balance = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    preferred_language = models.CharField(max_length=100, default='EN-US', blank=True)
    email = models.EmailField(verbose_name="Email address", max_length=100, unique=True)
    phone = models.CharField(verbose_name="Phone", max_length=20)
    country = models.CharField(verbose_name="Country code without the plus sign", max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'country']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class WritersApplications(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_email = models.CharField(max_length=100, blank=True)
    a_first_name = models.CharField(max_length=100, blank=True)
    a_last_name = models.CharField(max_length=100, blank=True)
    a_country = models.CharField(max_length=100, blank=True)
    a_article = models.TextField(blank=True)
    a_word_count = models.CharField(max_length=10, blank=True)
    a_language = models.CharField(max_length=100, blank=True)
    a_status = models.CharField(max_length=20, default='pending')
    a_datetime = models.DateTimeField(auto_now=True, null=True)


class Configs(models.Model):
    c_id = models.AutoField(primary_key=True)
    words_per_hour = models.CharField(max_length=50, blank=True)
    buffer_in_hours = models.CharField(max_length=50, blank=True)
    signup_article_title = models.TextField(blank=True)
    c_datetime = models.DateTimeField(auto_now=True, null=True)


class Languages(models.Model):
    l_id = models.AutoField(primary_key=True)
    l_code = models.CharField(max_length=70, blank=True)
    l_isotwo = models.CharField(max_length=5, blank=True)
    l_name = models.CharField(max_length=100, blank=True)
    l_datetime = models.DateTimeField(auto_now=True, null=True)


class Countries(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_pcode = models.CharField(max_length=70, blank=True)
    c_isotwo = models.CharField(max_length=5, blank=True)
    c_name = models.CharField(max_length=70, blank=True)
    t_datetime = models.DateTimeField(auto_now=True, null=True)


class AppraisalActiveTasks(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_code = models.CharField(max_length=70, blank=True)
    t_article = models.TextField(blank=True)
    t_article_word_count = models.TextField(max_length=20, blank=True)
    t_writer_reward = models.DecimalField(max_digits=10, decimal_places=5, default=0, blank=True)
    t_author = models.CharField(max_length=100, blank=True)
    t_status = models.CharField(max_length=50, blank=True, default='writerdraft')
    t_datetime = models.DateTimeField(auto_now=True, null=True)

    # statuses: draft,submitted, inreview, approved, returned, disapproved
    class Meta:
        ordering = ['t_id']


class ActiveTasks(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_code = models.CharField(max_length=70, blank=True)
    t_article = models.TextField(blank=True)
    t_article_word_count = models.TextField(max_length=20, blank=True)
    t_writer_reward = models.DecimalField(max_digits=10, decimal_places=5, default=0, blank=True)
    t_author = models.CharField(max_length=100, blank=True)
    t_status = models.CharField(max_length=50, blank=True, default='writerdraft')
    t_datetime = models.DateTimeField(auto_now=True, null=True)

    # statuses: draft,submitted, inreview, approved, returned, disapproved
    class Meta:
        ordering = ['t_id']


class ApprisalTasks(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_task_code = models.CharField(max_length=70, blank=True)
    t_title = models.CharField(max_length=500, blank=True)
    t_task_category = models.CharField(max_length=100, blank=True)
    t_word_count = models.CharField(max_length=100, blank=True)
    t_wc_description = models.CharField(max_length=100, blank=True)
    t_keywords = models.CharField(max_length=500, blank=True)
    t_keyword_repetition = models.CharField(max_length=20, blank=True)
    t_instructions = models.TextField(blank=True)
    t_doc = models.CharField(max_length=100, blank=True)
    t_status = models.CharField(max_length=50, blank=True, default='clientdraft')
    t_remarks = models.TextField(blank=True)
    t_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['t_id']


class Tasks(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_p_code = models.CharField(max_length=70, blank=True)
    t_task_code = models.CharField(max_length=70, blank=True)
    t_title = models.CharField(max_length=500, blank=True)
    t_project_category = models.CharField(max_length=100, blank=True)
    t_word_count = models.CharField(max_length=100, blank=True)
    t_wc_description = models.CharField(max_length=100, blank=True)
    t_keywords = models.CharField(max_length=500, blank=True)
    t_keyword_repetition = models.CharField(max_length=20, blank=True)
    t_instructions = models.TextField(blank=True)
    t_usd_cost = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    t_usd_payout = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    t_paid = models.CharField(max_length=10, default='no', blank=True)
    t_doc = models.CharField(max_length=100, blank=True)
    p_writer_level = models.CharField(max_length=100, blank=True, default='standard')
    p_extra_proofreading = models.CharField(max_length=20, blank=True, default='no')
    p_priority_order = models.CharField(max_length=20, blank=True, default='no')
    p_favourite_writers = models.CharField(max_length=20, blank=True, default='no')
    t_status = models.CharField(max_length=50, blank=True, default='clientdraft')
    t_remarks = models.TextField(blank=True)
    t_stars = models.CharField(max_length=10, blank=True)
    t_owner = models.CharField(max_length=100, blank=True)
    t_owner_names = models.CharField(max_length=150, blank=True)
    t_allocated_to = models.CharField(max_length=100, blank=True)
    t_urgent = models.CharField(max_length=10, blank=True)
    t_deadline = models.CharField(max_length=50, blank=True)
    t_writer_deadline = models.CharField(max_length=50, blank=True)
    t_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['t_id']


class PaymentTransactions(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_taskcode = models.CharField(max_length=70, blank=True)
    p_projectcode = models.CharField(max_length=70, blank=True)
    p_email = models.CharField(max_length=100, blank=True)
    p_transid = models.CharField(max_length=100, blank=True)
    c_usd_amount = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    c_moving_balance = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    p_direction = models.CharField(max_length=20, blank=True)
    p_narration = models.CharField(max_length=200, blank=True)
    c_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['p_id']


class Costs(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=70, blank=True)
    c_usd_cost = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    c_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['c_id']


class ProjectOptions(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_p_code = models.CharField(max_length=70, blank=True)
    p_writer_level = models.CharField(max_length=100, blank=True, default='standard')
    p_extra_proofreading = models.CharField(max_length=20, blank=True, default='no')
    p_priority_order = models.CharField(max_length=20, blank=True, default='no')
    p_favourite_writers = models.CharField(max_length=20, blank=True, default='no')
    p_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['p_id']


class Projects(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_code = models.CharField(max_length=70, blank=True)
    p_title = models.CharField(max_length=200, blank=True)
    p_category = models.CharField(max_length=100, blank=True)
    p_language = models.CharField(max_length=100, blank=True)
    p_description = models.TextField(blank=True)
    p_usd_cost = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    p_usd_payout = models.DecimalField(max_digits=10, decimal_places=5, default=0, null=True)
    p_owner = models.CharField(max_length=20, blank=True, )
    p_status = models.CharField(max_length=50, blank=True, default='clientdraft')
    p_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['p_id']


class Categories(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=150, blank=True)
    c_description = models.CharField(max_length=250, blank=True, )
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


class EmailTemplates(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_cid = models.CharField(max_length=10, blank=True)
    e_category = models.CharField(max_length=10, blank=True)
    e_mail = models.TextField(blank=True)

    class Meta:
        ordering = ['e_id']


class Articles(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_title = models.CharField(max_length=250, blank=True)
    a_tag = models.CharField(max_length=250, blank=True)
    a_author = models.CharField(max_length=100, blank=True)
    a_body = models.TextField(blank=True)

    class Meta:
        ordering = ['a_id']


class BlacklistedEmails(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_email = models.CharField(max_length=70, blank=True)
    m_from_name = models.CharField(max_length=150, blank=True)
    m_to_email = models.CharField(max_length=70, blank=True)
    m_to_name = models.CharField(max_length=150, blank=True)
    m_subject = models.CharField(max_length=200, blank=True)
    m_body = models.TextField(blank=True)
    m_read = models.CharField(max_length=10, blank=True, default='no')
    t_datetime = models.DateTimeField(auto_now=True, null=True)

    # statuses: draft,submitted, inreview, approved, returned, disapproved
    class Meta:
        ordering = ['b_id']


class Messages(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_from_email = models.CharField(max_length=70, blank=True)
    m_from_name = models.CharField(max_length=150, blank=True)
    m_to_email = models.CharField(max_length=70, blank=True)
    m_to_name = models.CharField(max_length=150, blank=True)
    m_subject = models.CharField(max_length=200, blank=True)
    m_body = models.TextField(blank=True)
    m_read = models.CharField(max_length=10, blank=True, default='no')
    t_datetime = models.DateTimeField(auto_now=True, null=True)

    # statuses: draft,submitted, inreview, approved, returned, disapproved
    class Meta:
        ordering = ['m_id']


class Support(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_category = models.CharField(max_length=100, null=True)
    s_email = models.CharField(max_length=100, null=True)
    s_message = models.TextField(blank=True, null=True)
    s_status = models.CharField(max_length=10, null=True, default='0')
    s_datetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['s_id']
