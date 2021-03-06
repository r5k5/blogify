from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Question(models.Model):
  question = models.TextField()
  userID = models.ForeignKey(User)
  date = models.DateTimeField('date published')

  def __str__(self) :
    return self.question

  def get_absolute_url(self) :
    return reverse('forum:detail', kwargs = {'pk': self.pk})

  class Meta:
    ordering = ["-date"]


class Answer(models.Model) :
  userID = models.ForeignKey(User)
  quesID = models.ForeignKey(Question)
  answer = models.TextField()
  date = models.DateTimeField('date published')
  upvotes = models.IntegerField(default=0)

  def __str__(self) :
    return self.answer

  def get_absolute_url(self) :
    return reverse('forum:detail', kwargs = {'pk': self.quesID.pk})

  class Meta:
    ordering = ["-date"]
