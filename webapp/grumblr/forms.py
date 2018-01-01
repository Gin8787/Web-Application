from django import forms

from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	username = forms.CharField(max_length=50)	
	email = forms.CharField(max_length=50)
	password = forms.CharField(max_length=200, label='Password', widget = forms.PasswordInput())
	confirm_password = forms.CharField(max_length=200, label='Confirm password', widget = forms.PasswordInput())

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()

		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		email = cleaned_data.get('email')

	
		if password and confirm_password and password != confirm_password:
			print("Passwords did not match")
			raise forms.ValidationError("Passords did not match. ")

		if '@' not in email:
			raise forms.ValidationError("email address is not correct ")

		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			print("Username is already taken")
			raise forms.ValidationError("Username is already taken. ")

		return self.cleaned_data['username']

class EditProfileForm(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	age = forms.IntegerField(required=False)
	bio = forms.CharField(max_length=420)
	picture = forms.ImageField(required=False)

	def clean(self):
		cleaned_data = super(EditProfileForm, self).clean()

		age = cleaned_data.get('age')
		picture = cleaned_data.get('picture')

		if picture:
			print("get picture from form")

		print("age is ")
		print(age)

		if age < 0:
			print("age is not correct")
			raise forms.ValidationError("Age should be a number that is not less than 0!")

		return cleaned_data

class ResetPwdEmailForm(forms.Form):
	email = forms.CharField(max_length=50)

	def clean(self):
		cleaned_data = super(ResetPwdEmailForm, self).clean()

		email = cleaned_data.get('email')

		if not email:
			raise forms.ValidationError("Email is required!")

		user = User.objects.filter(email=email)

		if not user:
			raise forms.ValidationError("The email is not the email that you registered! ")

		return cleaned_data

class ResetPasswordForm(forms.Form):
	new_password = forms.CharField(max_length=200, label='Password', widget = forms.PasswordInput())
	confirm_new_password = forms.CharField(max_length=200, label='Confirm password', widget = forms.PasswordInput())

	def clean(self):
		cleaned_data = super(ResetPasswordForm, self).clean()

		new_password = cleaned_data.get("new_password")
		confirm_new_password = cleaned_data.get("confirm_new_password")

		if not new_password:
			raise forms.ValidationError("Please enter the new password! ")

		if not confirm_new_password:
			raise forms.ValidationError("Please confirm your new password! ")

		if new_password != confirm_new_password:
			raise forms.ValidationError("Password doesn't match!")

		return cleaned_data

class PostForm(forms.Form):
	post = forms.CharField(max_length=42)

	def clean(self):
		cleaned_data = super(PostForm, self).clean()
		post = cleaned_data.get("post")

		if not post:
			raise forms.ValidationError("The content of the post should not be empty")

		return cleaned_data


class CommentForm(forms.Form):
    comment = forms.CharField(max_length = 420)

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()


        comment = self.cleaned_data.get('comment')

        if not comment:
            raise forms.ValidationError("Comment cannot be empty.")
            print('invalid commentForm')

        return cleaned_data
