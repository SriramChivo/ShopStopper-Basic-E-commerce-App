from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

# Create a manager to return a queryset of our customModel


class UserManager(BaseUserManager):
    def create_user(self, Email, UserName, password=None, commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not Email:
            raise ValueError('Users must have an email address')
        if not UserName:
            raise ValueError('Users must have an UserName')

        User = self.model(
            Email=self.normalize_email(Email),
            UserName=UserName,
        )

        User.set_password(password)

        if commit:
            User.save(using=self._db)
        return User

    def create_superuser(self, Email, UserName, password):
        User = self.create_user(
            Email,
            password=password,
            UserName=UserName,
            commit=False,
        )

        User.is_staff = True
        User.is_superuser = True
        User.save(using=self._db)
        return User

        # Creation of Custom UserModel using the Class BaseUSerManager and premissionsmixins for permission fields in models


class Accounts(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "Accounts"

    Email = models.EmailField(verbose_name='email address',
                              max_length=60, unique=True, help_text="Email Should be Valid and Unique")
    UserName = models.CharField(
        max_length=60, null=False, unique=True, help_text="Username should be Valid and Unique")

    Updated_Time = models.DateTimeField(auto_now=True)

    # password1 and password2 those fields will be taken care by AbstractBaseUser
    # lastLogin Field will be added by abstractbaseuser

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    # Define the usermanager to call from the objects,name model which use BaseUserManager
    objects = UserManager()

    USERNAME_FIELD = "Email"
    REQUIRED_FIELDS = ["UserName"]

    def __str__(self):
        return self.UserName + " With Email " + self.Email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

