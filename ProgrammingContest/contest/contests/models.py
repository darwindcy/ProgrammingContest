from django.db import models

# Create your models here.

class Contest(models.Model):
    contestName             = models.CharField(max_length = 20)
    contestDate             = models.DateTimeField()
    contestParticipants     = models.CharField(max_length = 20)