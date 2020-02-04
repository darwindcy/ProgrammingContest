from django.db import models

from django.urls import reverse

# Create your models here.

user_choices  = (
    ('administrator', 'ADMINISTRATOR'),
    ('participant', 'PARTICIPANT'),
    ('grader', 'GRADER'),
)

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
