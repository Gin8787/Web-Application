# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login

from django.db import transaction

from django.http import HttpResponse, Http404

from mimetypes import guess_type

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from grumblr.models import *
from grumblr.forms import *


@login_required
def index(request):
	print("In index")
	print("current user is " + request.user.username)
	context = {}
	posts = Posts.objects.all().order_by("-time")

	context['posts'] = posts
	context['curUser'] = request.user.username
	context['form'] = PostForm()

	return render(request, 'grumblr/index.html', context)

def register(request):
	print("Register a new user")
	context = {}

	if request.method != "POST":
		context['form'] = RegistrationForm()
		return render(request, 'grumblr/sign_up.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		print("Form is not valid, should return global error message")
		return render(request, 'grumblr/sign_up.html', context)

	print("username is")
	print(form.cleaned_data['username'])
	print(form.cleaned_data['email'])
	print(form.cleaned_data['first_name'])
	print(form.cleaned_data['last_name'])
	print(form.cleaned_data['password'])

	new_user = User.objects.create_user(email=form.cleaned_data['email'], \
		first_name=form.cleaned_data['first_name'], \
		last_name=form.cleaned_data['last_name'], \
		username=form.cleaned_data['username'], \
		password=form.cleaned_data['password'], \
		is_active=False)



	new_user.save()

	# send confirmation email
	token = default_token_generator.make_token(new_user)

	email_body="""
	Welcome to Grumblr. Please click the link below to 
	verify your email address and complete the registration of your account.

	http://%s%s
	"""% (request.get_host(),
		reverse('confirmation', args=(new_user.username, token)))

	send_mail(subject="Grumblr: Verify your email address of your Grumblr account",
			message=email_body,
			from_email="account_verify@grumblr.com",
			recipient_list=[new_user.email])

	context['email'] = form.cleaned_data['email']
	#context['token'] = token

	return render(request, 'grumblr/verify_account.html', context)

	# create prfile for the new user
	# new_profile = Profiles.objects.create(user=new_user)
	# print("Create profile successfully")

	# print("Register authenticate new_user")

	# new_user = authenticate(username=form.cleaned_data['username'], \
	#	password=form.cleaned_data['password'])

	# print("New user created successfully")

	#login(request, new_user)

	#print("Login new user and return index.html")

	#return redirect('index.html')

@login_required
def profile(request, username):
	print("This is profile function")
	if request.method != "GET":
		return redirect('index.html')

	#print("user name is " + username)

	#print(User.objects.all())

	
	if not (len(User.objects.filter(username = username)) > 0):
		print("Cannot find the user")
		#return redirect('index.html')
		return render(request, 'grumblr/login.html')

	context = {}

	visted_user = User.objects.get(username=username)

	postsOfUser = Posts.objects.filter(user=visted_user).order_by("-time")

	#profile_visted_user = Profiles.objects.filter(user=visted_user)

	friends = visted_user.friends.all()

	context["profile"] = Profiles.objects.get(user=visted_user)

	context['curUser'] = request.user.username

	context["postsOfUser"] = postsOfUser

	context["friends"] = friends

	context["requestUser"] = Profiles(user=request.user)
	
	for friend in friends:
		print("friend is:")
		print(friend.user.username)

	if visted_user == request.user:
		context["follow_btn"] = 0
		print("follow btn is 0")
	else:
		context["follow_btn"] = 1

	context['visted_user'] = visted_user
	print("Going to render profile")
	#print reverse('edit')

	#context['form'] = PostForm()

	return render(request, 'grumblr/profile.html', context)
	
"""@login_required
def postMsg(request):
	print("This is postMsg function")
	context = {}
	errors = []
	if request.method != 'POST' :
		print("postMsg GET")
		posts = Posts.objects.all().order_by('-time')
		context['posts'] = posts
		context['form'] = PostForm()
		return render(request, 'grumblr/index.html', context)

	form = PostForm(request.POST)


	if not form.is_valid():
		return render(request, 'grumblr/index.html', context)

	print("postMsg request is POST")

	new_post = Posts(post=form.cleaned_data['post'], user=request.user)
	new_post.save()

	print("postMsg saved new_post")

	posts = Posts.objects.all().order_by("-time")

	context['form'] = PostForm()
	context['posts'] = posts
	context['curUser'] = request.user.username

	print("Before return")
	return render(request, 'grumblr/index.html', context)
"""

@login_required
def postMsg(request):
	print("In postMsg")
	if request.method != "POST":
		print("The method is not POST")
	if not 'post' in request.POST:
		print("No post key in the POST Content")
	if not 'post' in request.POST or not request.POST['post']:
		raise Http404
	else:
		new_post = Posts(post=request.POST['post'], user=request.user)
		new_post.save()

	return HttpResponse("")

@login_required
def edit_profile(request):
	print("In edit_profile")
	context = {}
	user = request.user

	profile_to_edit = get_object_or_404(Profiles, user=user)

	if request.method != "POST":
		print("In edit_profile get")
		context['form'] = EditProfileForm()
		context['profile'] = profile_to_edit
		return render(request, 'grumblr/edit_profile.html', context)

	print("This is edit_profile POST part")

	form_profile = EditProfileForm(request.POST, request.FILES)

	context['form'] = form_profile

	if not form_profile.is_valid():
		print("form_profile is not valid")
		context['profile'] = profile_to_edit
		return render(request, 'grumblr/edit_profile.html', context)

	print("form_profile is valid, the values are:")
	print(form_profile.cleaned_data['age'])
	print(form_profile.cleaned_data['bio'])
	print(form_profile.cleaned_data['first_name'])
	print(form_profile.cleaned_data['last_name'])
	print(form_profile.cleaned_data['picture'])

	profile_to_edit.age = form_profile.cleaned_data['age']
	profile_to_edit.bio = form_profile.cleaned_data['bio']
	profile_to_edit.picture = form_profile.cleaned_data['picture']
	user.first_name = form_profile.cleaned_data['first_name']
	user.last_name = form_profile.cleaned_data['last_name']

	print(form_profile.cleaned_data['picture'])

	profile_to_edit.save()
	user.save()
	

	profile_to_edit = get_object_or_404(Profiles, user=user)
	profile = profile_to_edit.user

	context['visted_user'] = profile_to_edit.user


	postsOfUser = Posts.objects.filter(user=user).order_by("-time")

	context["postsOfUser"] = postsOfUser	
	context['curUser'] = request.user.username
	context["follow_btn"] = 0

	return redirect('home')
	#return render(request, 'grumblr/profile.html', context)

def get_picture(request, username):
	print("This is get_picture")
	profile = get_object_or_404(Profiles, user=User.objects.filter(username=username))
	if not profile.picture:
		raise Http404

	print(profile.picture.name)

	content_type = guess_type(profile.picture.name)
	#print profile.picture, dir(profile.picture)
	return HttpResponse(profile.picture, content_type=content_type)

@login_required
def follow(request, username):

	if not (len(User.objects.filter(username = username)) > 0):
		print("Cannot find the user")
		#return redirect('index.html')
		return render(request, 'grumblr/login.html')

	print("In follow")
	print("parameter username is ")
	print(username)
	visted_user = User.objects.get(username=username)
	visting_user = User.objects.get(username=request.user)
	prfile_visting_user = Profiles.objects.get(user=visting_user)
	print(visted_user)
	print(visted_user.username)
	prfile_visting_user.friends.add(visted_user)

	return redirect('home')

@login_required
def unfollow(request, username):
	if not (len(User.objects.filter(username = username)) > 0):
		print("Cannot find the user")
		#return redirect('index.html')
		return render(request, 'grumblr/login.html')

	visted_user = User.objects.get(username=username)
	visting_user = User.objects.get(username=request.user)
	profile_visting_user = Profiles.objects.get(user=visting_user)
	print(visted_user)
	profile_visting_user.friends.remove(visted_user)

	return redirect('home')

@login_required
def friends_stream(request):
	print("In friends_stream")
	context = {}
	profile = Profiles.objects.get(user=request.user)

	friends_all = profile.friends.all()

	print(friends_all)

	posts = Posts.objects.filter(user__in=friends_all).order_by("-time")

	print(posts)

	context['profile'] = profile
	#context['posts'] = posts

	print("********Before render friends stream******")
	return render(request, 'grumblr/friends_stream.html', context)

def activate_account(request, username, token):
	try:
		user = User.objects.get(username=username)
	except ObjectDoesNotExist:
		raise Http404

	if not default_token_generator.check_token(user, token):
		raise Http404

	user.is_active = True
	user.save()

	#create prfile for the new user
	new_profile = Profiles.objects.create(user=user)
	new_profile.picture = "profile_picture/default.jpeg"
	new_profile.save()
	print("Create profile successfully")

	return redirect('login')

# First let users give their email address
def get_reset_email(request):
	context = {}
	if request.method == 'GET':
		context['form'] = ResetPwdEmailForm()
		return render(request, 'grumblr/get_reset_email.html', context)

	form = ResetPwdEmailForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'grumblr/get_reset_email.html', context)

	user = User.objects.get(email=form.cleaned_data['email'])

	token = default_token_generator.make_token(user)

	email_body = """
	Hi, this email is from Grumblr.

	Please click the link below to reset the password of your Grumblr account.

	http://%s%s
	"""%(request.get_host(), reverse('reset_password_email_confirmation', args=(user.username, token)))

	send_mail(subject="Grumblr: Reset the password of your Grumblr account",
				message=email_body,
				from_email="reset_password@grumblr.com",
				recipient_list=[user.email])

	context['email'] = form.cleaned_data['email']

	return render(request, 'grumblr/reset_email_notification.html', context)

# Then confirm the reset link that sent to the users, and render the html
# which can let users enter their new password
def reset_password_email_confirmation(request, username, token):
	print("In reset_password_email_confirmation function")
	context = {}
	try:
		user = User.objects.get(username=username)
	except ObjectDoesNotExist:
		raise Http404

	if not default_token_generator.check_token(user, token):
		raise Http404


	context['user'] = user
	context['form'] = ResetPasswordForm()
	print(user)
	print("before reset_password.html")
	return render(request, 'grumblr/reset_password.html', context)

# Then reset the password of the user
def reset_password(request, username):
	print("In reset_password function")
	context = {}

	if request.method == 'GET':
		user = User.objects.get(username=username)
		context['user'] = user
		context['form'] = ResetPasswordForm()
		return render(request, 'grumblr/reset_password.html', context)

	form = ResetPasswordForm(request.POST)

	if not form.is_valid():
		user = User.objects.get(username=username)
		context['user'] = user
		context['form'] = form
		return render(request, 'grumblr/reset_password.html', context)

	try:
		user = User.objects.get(username=username)
	except ObjectDoesNotExist:
		raise Http404

	user.set_password(form.cleaned_data['new_password'])
	user.save()

	return redirect('login')


@login_required
def change_password(request):
	context = {}
	user = request.user
	if request.method == 'GET':
		
		context['user'] = user
		context['form'] = ResetPasswordForm()
		return render(request, 'grumblr/change_password.html', context)

	form = ResetPasswordForm(request.POST)

	if not form.is_valid():
		context['user'] = user
		context['form'] = form
		return render(request, 'grumblr/change_password.html', context)
	

	user.set_password(form.cleaned_data['new_password'])
	user.save()

	user = authenticate(username=user.username, password=form.cleaned_data['new_password'])

	login(request, user)

	return redirect('home')

@login_required
def get_posts(request, time="1970-01-01T00:00+00:00"):
	#print("In get posts")
	#print(time)
	#print(Posts.objects.all())
	max_time = Posts.get_max_time()
	posts = Posts.get_posts(time)
	context = {"max_time":max_time, "posts":posts}
	print("In get posts before render")
	return render(request, 'posts.json', context, content_type='application/json')

@login_required
def get_posts_profile(request, username, time="1970-01-01T00:00+00:00"):
	#print("In get posts profile")
	max_time = Posts.get_max_time()
	visted_user = User.objects.get(username=username)
	posts = Posts.objects.filter(user=visted_user)
	context = {"max_time":max_time, "posts":posts}
	return render(request, 'posts.json', context, content_type='application/json')

@login_required
def get_posts_friend(request, time="1970-01-01T00:00+00:00"):
	max_time = Posts.get_max_time()
	profile = Profiles.objects.get(user=request.user)
	friends_all = profile.friends.all()
	print(friends_all)
	posts = Posts.objects.filter(user__in=friends_all).order_by("-time")
	context = {"max_time": max_time, "posts": posts}
	return render(request, 'posts.json', context, content_type='application/json')


@login_required
def get_changes(request, time="1970-01-01T00:00+00:00"):
	#print("In get_changes")
	#print("time is ")
	#print(time)
	max_time = Posts.get_max_time()
	posts = Posts.get_changes(time)
	context = {"max_time":max_time, "posts":posts}
	return render(request, 'posts.json', context, content_type='application/json')

@login_required
def get_changes_profile(request, username,time="1970-01-01T00:00+00:00"):
	max_time = Posts.get_max_time()
	visited_user = User.objects.get(username=username)
	posts = Posts.get_changes_profile(visited_user, time)
	context = {"max_time":max_time, "posts":posts}
	return render(request, 'posts.json', context, content_type='application/json')

@login_required
def get_comments(reqeust, post_id):
	#print("In get_comment")
	#max_time = Comments.get_max_time()
	comments = Comments.get_comments(post_id)
	context = {"comments":comments}
	#if post_id == "12":
		#print("In get_comment 12")
		#for comment in comments:
			#print(comment)
	return render(reqeust, 'comments.json', context, content_type='application/json')

@login_required
def get_changes_comments(request, post_id, time="1970-01-01T00:00+00:00"):
	max_time = Comments.get_max_time()
	comments = Comments.get_comments(post_id)
	context = {"max_time":max_time, "comments":comments}
	return render(request, 'comments.json', context, content_type='application/json')

@login_required
def add_comment(request, post_id):
	#print("In add_comment")
	context = {}
	form = CommentForm(request.POST)
	if not form.is_valid():
		return render(request, 'grumblr/mainpage.html', context)

	context['form'] = form
	new_comment = Comments(comment=form.cleaned_data['comment'],post=Posts.objects.get(id=post_id), user=request.user)
	new_comment.save()
	max_time = Comments.get_max_time()
	comments = Comments.get_comments(post_id)
	context = {"max_time": max_time, "comment": new_comment}
	return render(request, 'comment.json', context, content_type='application/json')