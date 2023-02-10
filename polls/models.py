import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # setting for admin panel
    # we can ignore this if we don't use admin panel
    # boolean=True will show the boolean values as "v" and "x" button with nice css,
    # normally, it's just show "True", "False".
    # ordering='pub_date' will set order by
    # description='Published recently?' will set the name of the column was_published_recently
    # (i still don't understand why it select the last column, which is was_published_recently)
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
