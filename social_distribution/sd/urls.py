from django.urls import path, re_path

from . import views
from . import api
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Paths to UI pages  ----  All GETs
    path('', views.feed, name='ui_feed'),
    path('search',views.search, name='ui_search'),
    path('explore', views.explore, name='ui_explore'),
    path('account', views.account, name='ui_account'),
    path('newpost', views.new_post, name='ui_newpost'),
    path('register', views.register, name='ui_register'),
    path('notifications', views.notifications, name='ui_notifications'),
    path('login',  auth_views.LoginView .as_view(template_name='sd/login.html' ), name='ui_login'),
    path('logout', auth_views.LogoutView.as_view(template_name='sd/logout.html'), name='ui_logout'),


    # Paths to API   ----  None of these will be 'views'
    path('posts', api.posts),                                             # GET, POST (createPost)
    path('author/posts', api.author_posts),                               # GET
    path('friendrequest', api.friendrequest),                             # POST (friendRequest)
    path('posts/<uuid:post_id>', api.posts_postid),                        # GET, POST (getPost - foaf)
    path('author/<uuid:author_id>', api.author_authorid),                 # GET
    path('author/<uuid:author_id>/posts', api.author_authorid_posts),     # GET
    path('posts/<uuid:post_id>/comments', api.posts_postid_comments),     # GET, POST (addComment)
    path('author/<uuid:author_id>/friends', api.author_authorid_friends), # GET, POST (friends - intersectFriends)
    path('author/<uuid:author_id>/friends/<uuid:other_id>', api.author_authorid_friends_otherid), # GET
]
