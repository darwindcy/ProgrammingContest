from django.db import models

from django.conf import settings

from django.urls import reverse

# Create your models here.

import datetime

def get_upload_path(instance, filename):
    return 'submissions/{0}/{1}/{2}'.format(instance.submissionProblem.contest.contestName, instance.submissionTeam.userName, filename)

class CustomManager(models.Manager):
    def delete(self):
        for obj in self.get_queryset():
            obj.delete()

class Submission(models.Model):
    grade_choices = [
        ('pass', 'PASS'),
        ('fail', 'FAIL'),
        ('ungraded', 'UNGRADED'),
        ('inprocess', 'INPROCESS')
    ]

    submissionFile      = models.FileField(upload_to=get_upload_path, null = True, blank = True)
    submissionName      = models.CharField(max_length = 25, null = True)
    submissionTime      = models.TimeField(auto_now_add=True)
    submissionTeam      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'submittedBy', on_delete = models.SET_NULL, null = True, blank = True)
    from contests.models import Problem
    submissionProblem   = models.ForeignKey(Problem, related_name = 'associatedProblem',on_delete = models.SET_NULL, null = True, blank = True)
    submissionGrade     = models.CharField(max_length = 9, choices = grade_choices, default = grade_choices[2][0])
    totalSubmissionCount = models.IntegerField(default = 0)

    objects = CustomManager()

    def delete(self, using = None, keep_parents = False):
        if self.submissionFile.storage.exists(self.submissionFile.name):
            self.submissionFile.storage.delete(self.submissionFile.name)    

        super().delete()

    def get_submission_list_url(self):
        return reverse("submission:submission-list", kwargs = {"id": self.id})
    
    def get_submission_list(self):
        return reverse("submission:submission-list")

    def confirm_download_url(self):
        return reverse("submission:submission-download", kwargs = {"id":self.id})

    def get_grading_url(self):
        return reverse("submission:submission-grade", kwargs = {"id": self.id})

    def get_submission_score(self):
        submission_timedelta       = datetime.timedelta(hours = self.submissionTime.hour, 
                                                        minutes = self.submissionTime.minute, 
                                                        seconds = self.submissionTime.second)
        contest_timedelta          = datetime.timedelta(hours = self.submissionProblem.contest.startTime.hour, 
                                                        minutes = self.submissionProblem.contest.startTime.minute, 
                                                        seconds = self.submissionProblem.contest.startTime.second)
        timediff = submission_timedelta - contest_timedelta
        time_minutes = timediff.total_seconds()/60

        time_minutes = int(time_minutes)

        if(self.submissionGrade.lower() != "pass"):
            return 0
        
        count = self.totalSubmissionCount

        score = (count - 1) * 20 + time_minutes
        
        return score


    # def delete(self, *args, **kwargs):
    #     if os.path.isfile(self.submissionFile.path):
    #         os.remove(self.submissionFile.path)
        
    #     super().delete()