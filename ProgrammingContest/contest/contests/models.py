from django.db import models

from django.urls import reverse
import datetime

# Create your models here.

class Contest(models.Model):
    # Basic Detail
    contestName             = models.CharField(max_length = 20, unique = True)
    contestDate             = models.DateField()
    contestants             = models.ManyToManyField('users.CustomUser', blank = True)

    contestHours            = models.PositiveSmallIntegerField(default = 2)
    contestMinutes          = models.PositiveSmallIntegerField(default = 0)
    contestDuration         = models.DurationField(default = datetime.timedelta(days = 0, seconds=7200))

    isRunning               = models.BooleanField(default = False)


    def get_absolute_url(self):
        return reverse("contests:contest-detail", kwargs = {"id": self.id})

    def __str__(self):
        return self.contestName + ", " + str(self.contestDate)