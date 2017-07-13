from .models import Question, Answer
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class IndexView(generic.ListView) :
  template_name = 'forum/index.html'
  context_object_name = 'all_ques'

  def get_queryset(self) :
    return Question.objects.all()
    
@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DetailView(generic.DetailView) :
  model = Question
  template_name = 'forum/detail.html'

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class QuestionCreate(CreateView) :
  form_class = QuestionForm
  template_name = 'forum/question_form.html'

  def form_valid(self, form) :
    self.object = form.save(commit = False)
    try:
      obj = Question.objects.get(question__icontains = self.object.question)
    except:
      obj = None

    if obj :
      return render(self.request, 'forum/dup_error.html', {'question': obj})
    self.object.userID = self.request.user
    self.object.date = datetime.now()
    self.object.save()
    return super(QuestionCreate, self).form_valid(form)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class AnswerCreate(CreateView) :
  form_class = AnswerForm
  template_name = 'forum/answer_form.html'
  #passing data to template
  def get_context_data(self, **kwargs):
      return dict(
          super(AnswerCreate, self).get_context_data(**kwargs),
          question=Question.objects.get(pk = self.kwargs['pk'])
      )

  # setting the rest of data
  def form_valid(self, form) :
    self.object = form.save(commit = False)
    self.object.userID = self.request.user
    self.object.date = datetime.now()
    self.object.quesID = Question.objects.get(pk = self.kwargs['pk'])
    self.object.save()
    return super(AnswerCreate, self).form_valid(form)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
def upvote(request, pk) :
  answer = Answer.objects.get(pk = pk)
  answer.upvotes = answer.upvotes + 1
  answer.save()
  return render(request, 'forum/detail.html', {'question': answer.quesID})
