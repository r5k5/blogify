from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Post 
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType


def post_create(request):
	if not request.user.is_authenticated():
		return redirect("accounts:login")
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("posts:detail", instance.id)
	context = {
		"form": form,
	}
	return render(request, "posts/post_form.html", context)


def post_detail(request, id=None):
	if not request.user.is_authenticated():
		return redirect("accounts:login")
	instance = get_object_or_404(Post, id=id)
	initial_data = {
		"content_type": ContentType.objects.get_for_model(instance.__class__),
		"object_id": instance.id,
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		object_id = form.cleaned_data.get("object_id")
		content = form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(
									user = request.user,
									content_type = content_type,
									object_id = object_id,
									content = content
								) #creates a new comment for the instance
		form = CommentForm() #clears the form after a new comment is added

	comments = Comment.objects.filter_by_instance(instance) #holds all the comments for the instance

	paginator = Paginator(comments, 3) # show 3 comments per page
	page_no = request.GET.get('page') # gets value if in url page=value
	try:
		queryset = paginator.page(page_no)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		"post": instance,
		"comments": queryset,
		"comment_form": form,
	}
	return render(request, "posts/post_detail.html", context)


def post_list(request):
	if not request.user.is_authenticated():
		return redirect("accounts:login")
	queryset_list = Post.objects.all()

	query = request.GET.get("q") # used for searching; gets value if in url q=value
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 5) # Show 5 posts per page
	page_no = request.GET.get('page') # gets value if in url page=value
	try:
	    queryset = paginator.page(page_no)
	except PageNotAnInteger: # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset,
	}
	return render(request, "posts/post_list.html", context)


def post_update(request, id=None):
	if not request.user.is_authenticated():
		return redirect("accounts:login")
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	
	if instance.user != request.user:
		return render(request, "posts/permission.html", {})

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("posts:detail", instance.id)
	context = {
		"post": instance,
		"form": form
	}
	return render(request, "posts/post_form.html", context)


def post_delete(request, id=None):
	if not request.user.is_authenticated():
		return redirect("accounts:login")
	instance = get_object_or_404(Post, id=id)
	
	if instance.user != request.user:
		return render(request, "posts/permission.html", {})
	
	instance.delete()
	return redirect("posts:list")