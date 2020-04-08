from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url
from .views import *
from .api_views import *
from .ajax import *
from django.contrib.auth import views as auth_views

urlpatterns = [
     # API Calls
    url(r'^auth/register/$', CreateAuthorAPIView.as_view(), name='auth_user_create'),
    url(r'^auth/logout/$', LogoutView.as_view(), name='auth_user_logout'),
    url(r'^auth/getuser/$', GetAuthorAPIView.as_view(), name='auth_user_get'),
    path('auth/edituser/<uuid:pk>', EditUserView.as_view(), name='auth_user_update'),
    url(r'^auth/createpost/$', CreatePostAPIView.as_view(), name='auth_post_create'),
    url(r'^auth/getpost/$', GetPostAPIView.as_view(), name='auth_post_get'),
    path('deletepost/<uuid:pk>', DeletePostAPIView.as_view(), name='post_delete'),
    path('posts/<uuid:pk>', GetPostAPIView.as_view(), name='get_post'),
    path('posts/<uuid:pk>/comments', CommentsAPIView.as_view(), name='get_post_comments'),
    path('author/<uuid:pk>/post', CreatePostAPIView.as_view(), name='create_post'),
    path('friendrequest/', CreateFriendRequestAPIView.as_view(), name='create_friend_request/'),
    path('author/<uuid:pk>/friendrequest', GetAllAuthorFriendRequest.as_view(), name='all_author_friend_request'),
    path('author/<uuid:pk>/posts/', GetAllAuthorPostAPIView.as_view(), name='all_author_posts'),
    path('posts', GetAllPublicPostsAPIView.as_view(), name='get_all_posts'),
    path('author/posts', GetAllVisiblePostsAPIView.as_view(), name='get_visible_posts'),
    path('author/<uuid:pk>', GetAuthorAPIView.as_view(), name='get_author'),
    path('author/<uuid:pk>/friends', GetAllAuthorFriendsAPIView.as_view(), name='all_author_friends'),
    path('friend/<uuid:pk>/foaf', GetAllFOAFAPIView.as_view(), name='get_author_foaf'),
    path('author/', GetAllAuthorsAPIView.as_view(), name='all_authors'),
    path('friend/<uuid:pk>', CreateFriendAPIView.as_view(), name='create_friend'),
    path('author/<uuid:pk1>/friends/<uuid:pk2>', CheckFriendAPIView.as_view(), name='check_friend'),
    path('friend/<uuid:pk>/delete', DeleteFriendAPIView.as_view(), name='delete_friend'),


     #Django views
    path('', explore, name='explore'),
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('newpost', new_post, name='new_post'),
    path('feed', feed, name="my_feed"),
    path('notifications', notifications, name='notifications'),
    path('edit_post/<uuid:post_id>', edit_post, name='edit_post'),
    path('image/<uuid:pk>', get_image, name='get_image'),
    path('search', search, name='search'),
    path('account', account, name='account'),
    path('edit_account', edit_account, name='edit_account'),
    path('verify', verify, name='verify'),

    #AJAX Calls
    path('verifyuser', verifyuser, name='verifyuser'),
    path('deleteuser', deleteuser, name='deleteuser'),
    path('rejectrequest', rejectrequest, name='reject_request'),
    path('friendrequest', friendrequest, name='friend_request'),
    path('unfollow', unfollow, name='unfollow'),
    path('deletepost', deletepost, name='delete_post'),
]
