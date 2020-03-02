from django.db import models

from django.urls import reverse

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from contests.models import Contest

user_choices  = (
    ('administrator', 'ADMINISTRATOR'),
    ('team', 'Team'),
    ('grader', 'GRADER'),
)


class MyAccountManager(BaseUserManager):
    def create_user(self, userName, userType, password=None, participatingIn = None):
        if not userName:
            raise ValueError("Users must have a username")

        if not userType:
            raise ValueError("Users must have a user type")

        if not password:
            raise ValueError("Users must have a password")
        
        user = self.model(
            userName = userName,
            userType = userType,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_staffuser(self, userName, userType, password):
        user = self.create_user(
            userName = userName,
            userType = userType,
            password = password
        )
        user.staff = True
        user.save(using = self._db)
        return user

    def create_superuser(self, userName, userType, password):
        user = self.create_user(
            userName = userName,
            userType = userType,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class CustomUser(AbstractBaseUser):
    userName        = models.CharField(max_length = 30, unique = True)
    userType        = models.CharField(max_length=20, 
                                    choices = user_choices, 
                                    default = user_choices[1])
    participatingIn  = models.ManyToManyField(Contest, blank = True)

    date_joined     = models.DateTimeField(blank = True, null = True)
    last_login      = models.DateTimeField(blank = True, null = True)
    admin        = models.BooleanField(default = False)
    active       = models.BooleanField(default = True)
    staff        = models.BooleanField(default = False)
    is_superuser    = models.BooleanField(default = False)


    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = ['userType', 'password']

    objects = MyAccountManager()

    def get_full_name(self):
        return self.userName

    def __str__(self):
        return self.userName + ", " + self.userType

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs = {"id": self.id})
