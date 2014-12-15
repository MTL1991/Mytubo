from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class Tuber(models.Model):
    user = models.OneToOneField(User, editable=False)

    def __unicode__(self):
        return  self.user.username

class Tubo(models.Model):
    tuber = models.ForeignKey('Tuber')

    title = models.CharField(max_length=60)
    description = models.TextField()
    docfile = models.FileField(upload_to='')
    last_editing_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title