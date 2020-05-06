from django.db import models

from django.conf import settings

from django.urls import reverse

# Create your models here.

import datetime

def get_upload_path(instance, filename):
    newname = "sub_for_id_" + str(instance.submissionProblem.id) + "." + instance.submissionLanguage
    return 'submissions/{0}/{1}/{2}'.format(instance.submissionProblem.contest.contestName, instance.submissionTeam.userName, newname)

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
    language_choices = [
        ('java', 'JAVA'),
        ('c++', 'C++'),
        ('c', 'C'),
        ('python', 'PYTHON'),
    ]

    submissionFile      = models.FileField(upload_to=get_upload_path, null = False, blank = False)
    submissionName      = models.CharField(max_length = 25, null = True)
    submissionLanguage  = models.CharField(max_length = 6, choices = language_choices, default = language_choices[2][0])

    submissionTime      = models.DateTimeField(auto_now_add=True)
    subTouchTime        = models.DateTimeField(auto_now=True)
    submissionTeam      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'submittedBy', on_delete = models.SET_NULL, null = True, blank = True)
    from contests.models import Problem
    submissionProblem   = models.ForeignKey(Problem, related_name = 'associatedProblem',on_delete = models.SET_NULL, null = True, blank = True)
    submissionGrade     = models.CharField(max_length = 9, choices = grade_choices, default = grade_choices[2][0])
    totalSubmissionCount = models.IntegerField(default = 0)

    objects = CustomManager()


    def delete(self, using = None, keep_parents = False):
        try:
            if self.submissionFile.storage.exists(self.submissionFile.name):
                self.submissionFile.storage.delete(self.submissionFile.name) 
        except:
            print("Error while deleting File")

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

        if self.submissionProblem and self.submissionTime:
            #timediff = submission_timedelta - contest_timedelta
            timediff        = self.submissionTime - self.submissionProblem.contest.startTime
            duration_in_s   = timediff.total_seconds()

            time_minutes = divmod(duration_in_s, 60)[0]
            print("sub time", self.submissionTime)
            print("start time", self.submissionProblem.contest.startTime)
            print("Time seconds", duration_in_s)
            print("Time minutes", time_minutes)
            if(self.submissionGrade.lower() != "pass"):
                return 0
            
            count = self.totalSubmissionCount

            score = (count - 1) * 20 + time_minutes
        else:
            score = 0
        
        return score
