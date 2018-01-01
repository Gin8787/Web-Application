from django.conf.urls import url

import django.contrib.auth.views

import grumblr.views

urlpatterns = [
    url(r'^index.html', grumblr.views.index, name="home"),
    url(r'^login.html$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name="login.html"),
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^sign_up$', grumblr.views.register, name='sign_up.html'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^profile/(?P<username>\w+)$', grumblr.views.profile, name="profile"),
    url(r'^postMsg$', grumblr.views.postMsg, name="postMsg"),
    url(r'^edit/', grumblr.views.edit_profile, name="edit"),
    url(r'^profile_picture/(?P<username>\w+)$', grumblr.views.get_picture, name='picture'),
    url(r'^follow/(?P<username>\w+)$', grumblr.views.follow, name='follow'),
    url(r'^unfollow/(?P<username>\w+)$', grumblr.views.unfollow, name='unfollow'),
    url(r'^friends_stream', grumblr.views.friends_stream, name="friends_stream"),
    url(r'^registration_confirmation/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', grumblr.views.activate_account, name="confirmation"),
    url(r'^reset_password_email_confirmation/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', grumblr.views.reset_password_email_confirmation, name="reset_password_email_confirmation"),
    url(r'^get_reset_email', grumblr.views.get_reset_email, name="get_reset_email"),
    url(r'^reset_password/(?P<username>\w+)$', grumblr.views.reset_password, name="reset_password"),
    url(r'^change_password', grumblr.views.change_password, name="change_password"),
    url(r'^get_changes/(?P<time>.+)$', grumblr.views.get_changes, name="get_changes"),
    url(r'^get_changes/?$', grumblr.views.get_changes),
    url(r'^get_posts$', grumblr.views.get_posts, name="get_posts"),
    url(r'^get_comments/(?P<post_id>\d+)$', grumblr.views.get_comments, name="get_comments"),
    url(r'^get_changes_comments/(?P<time>.+)/(?P<post_id>\d+)$', grumblr.views.get_changes_comments, name="get_changes_comments"),
    url(r'^add_comment/(?P<post_id>\d+)$', grumblr.views.add_comment, name="add_comment"),
    url(r'^get_posts_profile/(?P<username>\w+)$', grumblr.views.get_posts_profile, name="get_posts_profile"),
    url(r'^get_changes_profile/(?P<time>.+)/(?P<post_id>\d+)$', grumblr.views.get_changes_profile, name="get_changes_profile"),
    url(r'^get_posts_friend', grumblr.views.get_posts_friend, name="get_posts_friend"),
]