from django.db import models

from django.urls import reverse
import datetime

# Create your models here.

class Contest(models.Model):
    # Basic Detail
    contestName             = models.CharField(max_length = 50, unique = True)
    contestDate             = models.DateField()
    contestants             = models.ManyToManyField('users.CustomUser', blank = True)

    contestHours            = models.PositiveSmallIntegerField(default = 2)
    contestMinutes          = models.PositiveSmallIntegerField(default = 0)
    contestDuration         = models.DurationField(default = datetime.timedelta(days = 0, seconds=7200))

    isRunning               = models.BooleanField(default = False)
    isPaused                = models.BooleanField(default = False)
    pauseTime               = models.DateTimeField(null = True)
    startTime               = models.DateTimeField(null = True)
    stopTime                = models.DateTimeField(null = True)

    # returns the remaining time
    def get_remaining_time(self):
        remainingTime = 0
        if not self.isRunning:
            return remainingTime
        else:
            
            startTime           = self.startTime
            tz_info             = startTime.tzinfo

            currentTime         = datetime.datetime.now(tz_info)
            contestDuration     = self.contestDuration
            durationSeconds     = contestDuration.seconds
            remainingTime            = startTime - currentTime

            time_in_seconds = (remainingTime.total_seconds() + durationSeconds)

            if (time_in_seconds <= 0):
                self.isRunning = False
                self.save()
            return time_in_seconds 
    
    # returns remaining time in formatted string
    def get_remaining_time_string(self):
        if not self.isRunning:
            return "Contest Not Running"
        else:
            timeLeft            = self.get_remaining_time()
            hour                = int(timeLeft // 3600)
            minutes             = int((timeLeft // 60) % 60)
            seconds             = int(timeLeft - hour * 3600 - minutes * 60)
            
            hour = str(hour) if hour >= 10 else ("0" + str(hour))
            minutes = str(minutes) if minutes >= 10 else ("0" + str(minutes))
            seconds = str(seconds) if seconds >= 10 else ("0" + str(seconds))

            time = hour + ":" + minutes +":"+ seconds
            return time

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