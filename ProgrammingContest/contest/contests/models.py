from django.db import models

from django.urls import reverse

# Create your models here.

class Contest(models.Model):
    contestName             = models.CharField(max_length = 20)
    contestDate             = models.DateField()
    contestParticipants     = models.CharField(max_length = 20)

    def get_absolute_url(self):
        return reverse("contests:contest-detail", kwargs = {"id": self.id})