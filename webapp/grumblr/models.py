# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Max

class Posts(models.Model):
	post = models.CharField(max_length = 42)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add = True)
	last_changed = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.post

	@staticmethod
	def get_changes(time="1970-01-01T00:00+00:00"):
		return Posts.objects.filter(last_changed__gt=time).distinct()

	@staticmethod
	def get_posts(time="1970-01-01T00:00+00:00"):
		return Posts.objects.filter(last_changed__gt=time).distinct()

	@staticmethod
	def get_changes_profile(profile_user, time="1970-01-01T00:00+00:00"):
		return Posts.objects.filter(last_changed__gt=time, user=profile_user)

	@property
	def html(self):
		return render_to_string("post_item.html", {"user":self.user, "post":self.post,"time":self.time,"post_id":self.id}).replace("\n", "");

	@staticmethod
	def get_max_time():
		return Posts.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

class Comments(models.Model):
	comment = models.CharField(max_length = 420)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Posts, on_delete=models.CASCADE)
	last_changed = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.comment

	@staticmethod
	def get_changes(post_id):
		return Comments.objects.all().filter(post=Posts.objects.get(id=post_id))

	@staticmethod
	def get_comments(post_id):
		return Comments.objects.all().filter(post=Posts.objects.get(id=post_id))

	@property
	def html(self):
		return render_to_string("comment_item.html", {"user":self.user, "comment":self.comment, "time":self.time, "comment_id":self.id}).replace("\n", "")

	@staticmethod
	def get_max_time():
		return Comments.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

class Profiles(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	age = models.IntegerField(null=True)
	bio = models.CharField(max_length=420, default="Hello, Grumblr!", blank=True)
	picture = models.ImageField(upload_to="profile_picture", blank=True)

	friends = models.ManyToManyField(User, related_name='friends')

	def __unicode__(self):
		return user.username + " " +self.age + " " + self.bio

	def get_profile(user):
		try:
			profile = Profiles.Profiles.object.get(user=user)
		except ObjectDoesNotExist:
			print("The profile does not exist")

		return profile