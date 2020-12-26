from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models, transaction


# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, email_id, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email_id:
            raise ValueError('The given email_id must be set')
        try:
            with transaction.atomic():
                user = self.model(email_id=email_id, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(UserManager, self).__init__(*args, **kwargs)

    def create_superuser(self, email_id, password, full_name):
        user = self.model(
            full_name=full_name,
            email_id=email_id,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(r'^[0-9]*$', 'Only Numeric characters are allowed.')

    email_id = models.EmailField(max_length=100, null=False, blank=False,unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=10, unique=True, null=True, validators=[phone_regex])
    address = models.CharField(max_length=255, default=None, null=True, blank=True)
    city = models.CharField(max_length=255, default=None, null=True, blank=True)
    state = models.CharField(max_length=255, default=None, null=True, blank=True)
    country = models.CharField(max_length=255, default=None, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=False, blank=False, validators=[phone_regex])
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'email_id'
    objects = UserManager()

    class Meta:
        db_table = 'users'  # define your custom name

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.full_name
