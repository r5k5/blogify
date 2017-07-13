from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from posts.models import Post
from forum.models import Question

def home_page(request):
	return render(request, "accounts/home.html", {'user': request.user})

def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect("accounts:dashboard")
	
	return render(request, "accounts/form.html", {"form": form, "title": "Sign In",})

def register_view(request):
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		return redirect("accounts:dashboard")

	return render(request, "accounts/form.html", {"form": form, "title": "Register",})

def logout_view(request):
	logout(request)
	return redirect("accounts:home_page")

def dashboard(request):
	if not request.user.is_authenticated():
		return redirect("accounts:login")
	return render(request, "accounts/dashboard.html", {"Post": Post.objects.all(), "Question": Question.objects.all(), "curr_user": request.user})