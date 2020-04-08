import os
import json
import uuid
import base64
from .models import *
from .serializers import *
from .forms import *
from .helper_functions import *
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
import social_distribution.settings
import requests
import commonmark

"""AJAX Requests"""

@csrf_exempt
def verifyuser(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            target = Author.objects.get(uuid=data['target_author'])
            target.verified = True
            target.save()
            return HttpResponse()
        except:
            return HttpResponse(status_code=500)
    else:
        return HttpResponse(status_code=405)

@csrf_exempt
def deleteuser(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            target = Author.objects.get(uuid=data['target_author'])
            target.delete()
            return HttpResponse()
        except:
            return HttpResponse(status_code=500)
    else:
        return HttpResponse(status_code=405)

@csrf_exempt
def rejectrequest(request):
    if request.method == "POST":
        try:
            user = get_current_user(request)
            data = json.loads(request.body)
            target = Author.objects.get(username=data['target_author'])
            fr = FriendRequest.objects.get(Q(to_author=user.uuid) & Q(from_author=target.uuid))
            fr.rejected=True
            fr.save()
            return HttpResponse()
        except:
            return HttpResponse(status_code=500)
    return HttpResponse(status_code=405)


@csrf_exempt
def friendrequest(request):
    if valid_method(request):
        if request.method == "GET":
            return HttpResponse(status_code=405)

        try:
            user = get_current_user(request)
            if not authenticated(request) or not user:
                return redirect('login')
            data = json.loads(request.body)

            target = Author.objects.get(username=data['target_author'])
            relationship, obj = get_relationship(user, target)
            """
            relationship values:
            1 --> user and target are already friends; no work required
            2 --> there exists a friend request from target to user; complete friends and delete friend request
            3 --> there exists a friend request from user to target; don't create another
            4 --> no relationship exists yet; create one
            obj is returned in case 2 friend request to be deleted
            """
            if relationship == 1:
                follows1 = Follow.objects.filter(
                    Q(follower=target.uuid) & Q(following=user.uuid))
                if not follows1:
                    info = {'follower': targetuuid, 'following': user.uuid}
                    s = FollowSerializer(data=info)
                    if s.is_valid():
                        s.save()
                follows2 = Follow.objects.filter(
                    Q(follower=user.uuid) & Q(following=target.uuid))
                if not follows2:
                    info = {'follower': user.uuid, 'following': target.uuid}
                    s = FollowSerializer(data=info)
                    if s.is_valid():
                        s.save()
                # creates Follow objects in case they don't already exist
                return HttpResponse(json.dumps({'status': 'friends'}), content_type='application/json')

            elif relationship == 2:
                info = {'author': user.uuid, 'friend': target.uuid}
                friend = FriendSerializer(data=info)
                if friend.is_valid():
                    friend.save()
                    obj.delete()
                else:
                    return HttpResponse(status_code=500)
                follows1 = Follow.objects.filter(
                    Q(follower=target.uuid) & Q(following=user.uuid))
                if not follows1:
                    info = {'follower': target.uuid, 'following': user.uuid}
                    s = FollowSerializer(data=info)
                    if s.is_valid():
                        s.save()
                    else:
                        return HttpResponse(status_code=500)
                follows2 = Follow.objects.filter(
                    Q(follower=user.uuid) & Q(following=target.uuid))
                if not follows2:
                    info = {'follower': user.uuid, 'following': target.uuid}
                    s = FollowSerializer(data=info)
                    if s.is_valid():
                        s.save()
                    else:
                        return HttpResponse(status_code=500)
                return HttpResponse(json.dumps({'status': 'friends'}), content_type='application/json')

            elif relationship == 3:
                follows1 = Follow.objects.filter(
                    Q(follower=user.uuid) & Q(following=target.uuid))
                if not follows1:
                    info = {'follower': user.uuid, 'following': target.uuid}
                    s = FollowSerializer(data=info)
                    if s.is_valid():
                        s.save()

                return HttpResponse(json.dumps({'status': 'following'}), content_type='application/json')

            elif relationship == 4:
                info = {'to_author': target.uuid, 'from_author': user.uuid}
                friendreq_serializer = FriendRequestSerializer(data=info)
                if friendreq_serializer.is_valid():
                    friendreq_serializer.save()
                else:
                    return HttpResponse(status_code=500)
                follows1 = Follow.objects.filter(
                    Q(follower=target.uuid) & Q(following=user.uuid))
                if not follows1:
                    info = {'follower': user.uuid, 'following': target.uuid}
                    s = FollowSerializer(data=info)
                    if s.is_valid():
                        s.save()
                    else:
                        return HttpResponse(status_code=500)

                return HttpResponse(json.dumps({'status': 'following'}), content_type='application/json')
        except:
            return HttpResponse(status_code=500)
    else:
        return HttpResponse(status_code=405)

@csrf_exempt
def unfollow(request):
    if request.method=="POST":
        if authenticated(request):
            try:
                user = get_current_user(request)
                data = json.loads(request.body)
                target = Author.objects.get(uuid=data['target_author'])

                follow = Follow.objects.filter(follower=user.uuid, following=target.uuid)
                if follow:
                    follow.delete()

                fr = FriendRequest.objects.filter(Q(to_author=target.uuid) & Q(from_author=user.uuid))
                if fr:
                    fr.delete()

                friends = Friend.objects.filter((Q(author=user.uuid) & Q(friend=target.uuid)) | Q(author=target.uuid) & Q(friend=user.uuid))
                if friends:
                    friends.delete()
                    fr = FriendRequest.objects.create(to_author=user, from_author=target)

                return HttpResponse()
            except:
                return HttpResponse(status_code=500)
        else:
            return HttpResponse(status_code=401)
    else:
        return HttpResponse(status_code=405)

@csrf_exempt
def deletepost(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user = get_current_user(request)
            post = Post.objects.get(uuid=data['target_post'])
            if authenticated(request) and user:
                if post.author == user:
                    post.delete()
                else:
                    return HttpResponse(status_code=403) #logged in but not correct user
                return HttpResponse() #OK
            else:
                return HttpResponse(status_code=401) #not logged in
        except:
            return HttpResponse(status_code=500) #server errror
    else:
        return HttpResponse(status_code=405) #invalid method