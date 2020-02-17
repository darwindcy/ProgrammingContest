from django.db import models

from django.urls import reverse

from users.models import User

from django.conf import settings
# Create your models here.

class OraclePost(models.Model):
    postQuestion        = models.TextField(max_length = 500, null = False)
    postAnswer          = models.TextField(max_length = 500, null = True)
    postTime            = models.DateTimeField(auto_now_add=True)
    postUser            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True, blank = True)   
    isAnswered          = models.BooleanField(default = False)    

    def get_absolute_url(self):
        return reverse("oracle:post-detail", kwargs = {"id": self.id})