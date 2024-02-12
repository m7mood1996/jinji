
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers for authentication instead of usernames.
    """
    def create_user(self, email, username, first_name, last_name, password=None, **other_fields):
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        elif not first_name:
            raise ValueError(_('Users must have a first name'))
        elif not username:
            raise ValueError(_('Users must have a username'))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **other_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **other_fields
        )

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        user.save(using=self._db)

        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    # basic information
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    car_number = models.CharField(max_length=10, unique=False, blank=False, default='000000')
    # Registration Date
    date_joined = models.DateTimeField(default=timezone.now)  ## todo: unterschied zu 'auto_now_add=True'

    # Permissions
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'car_number']  # Note: USERNAME_FIELD not to be included in this list!

    def __str__(self):
        return self.username


class Entry(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


    