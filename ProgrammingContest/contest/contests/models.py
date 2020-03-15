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
    #contestProblems         = models.ForeignKey(Problem, default = None, on_delete = models.SET_NULL, null = True)


    def get_absolute_url(self):
        return reverse("contests:contest-detail", kwargs = {"id": self.id})

    def __str__(self):
        return self.contestName + ", " + str(self.contestDate)
        

class Problem(models.Model):
    contest                = models.ForeignKey(Contest, null = True, on_delete = models.CASCADE, related_name = "contestproblems")
    problemName            = models.CharField(max_length = 100, unique = True, default = "Another Problem", null = False)
    problemInformation     = models.TextField(null = True)
    problemTests           = models.TextField(null = True)

    def __str__(self):
        return self.problemName
    
    def problem_data(self):
        return self.contest + "\n\n" + self.problemName + "\n\n" + self.problemInformation + "\n\n" + self.problemTests 