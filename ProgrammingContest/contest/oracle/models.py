from django.db import models

from django.urls import reverse

from users.models import CustomUser

from django.conf import settings
# Create your models here.

class OraclePost(models.Model):
    postQuestion        = models.TextField(max_length = 500, null = False)
    postAnswer          = models.TextField(max_length = 500, null = True)
    postTime            = models.DateTimeField(auto_now_add=True)
    postUser            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'postedBy', on_delete = models.SET_NULL, null = True, blank = True)
    postAnswerer        = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'answeredBy', on_delete = models.SET_NULL, null = True, blank = True)
    isAnswered          = models.BooleanField(default = False)    

    def get_absolute_url(self):
        return reverse("oracle:post-detail", kwargs = {"id": self.id})