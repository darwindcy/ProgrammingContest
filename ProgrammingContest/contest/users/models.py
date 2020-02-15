from django.db import models

from django.urls import reverse

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

user_choices  = (
    ('administrator', 'ADMINISTRATOR'),
    ('participant', 'PARTICIPANT'),
    ('grader', 'GRADER'),
)


class MyAccountManager(BaseUserManager):
    def create_user(self, userName, userType, password=None):
        if not userName:
            raise ValueError("Users must have a username")

        if not userType:
            raise ValueError("Users must have a user type")
        
        user = self.model(
            userName = userName,
            userType = userType
        )

        user.set_password(password)
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

class customUser(AbstractBaseUser):
    userName        = models.CharField(max_length = 30, unique = True)
    userType        = models.CharField(max_length=20, 
                                    choices = user_choices , 
                                    default = 'participant')
    password         = models.CharField(max_length=30)
    participatingIn  = models.ManyToManyField('contests.Contest', blank = True)
    contestIn   = models.BooleanField

    email           = models.EmailField()
    date_joined     = models.DateTimeField(blank = True, null = True)
    last_login      = models.DateTimeField(blank = True, null = True)
    is_admin        = models.BooleanField(default = False)
    is_active       = models.BooleanField(default = True)
    is_staff        = models.BooleanField(default = False)
    is_superuser    = models.BooleanField(default = False)


    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = ['userType', 'password']

    objects = MyAccountManager()

    def __str__(self):
        return self.userName + ", " + self.userType

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    

    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs = {"id": self.id})

class User(models.Model):
    userName    = models.CharField(max_length=20) #max_length = 20
    userType    = models.CharField(max_length=20, 
                                    choices = user_choices , 
                                    default = 'participant')
    password    = models.CharField(max_length=30)
    participatingIn  = models.ManyToManyField('contests.Contest', blank = True)
    contestIn   = models.BooleanField

    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs = {"id": self.id})
