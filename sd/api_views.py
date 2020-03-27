from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .paginations import *
from .models import *
from .serializers import *
from .helper_functions import *
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .forms import *
import os
import json
import uuid
from uuid import uuid4


def serializePost(post):
    postDict = {}
    postDict['author'] = serializeAuthor(post.author)
    postDict['title'] = post.title
    postDict['source'] = post.source
    postDict['origin'] = post.origin
    postDict['description'] = post.description
    postDict['contentType'] = post.contentType
    postDict['content'] = post.content
    postDict['categories'] = post.categories
    # postDict['count'] = 'COUNT'
    # postDict['size'] = 'SIZE'
    # postDict['next'] = 'NEXT'
    comments = Comment.objects.filter(post=post)
    postDict['comments'] = []
    for comment in comments:
        postDict['comments'].append(serializeComment(comment))
    postDict['published'] = post.published
    postDict['id'] = post.uuid
    postDict['visibility'] = post.visibility
    postDict['visibleTo'] = []
    postDict['unlisted'] = post.unlisted
    return postDict


def serializeComment(comment):
    commentDict = {}
    commentDict['author'] = serializeAuthor(comment.author)
    commentDict['comment'] = comment.comment
    commentDict['contentType'] = comment.contentType
    commentDict['published'] = comment.published
    commentDict['id'] = comment.uuid
    return commentDict


def serializeAuthor(author):
    authorDict = {}
    authorDict['id'] = str(author.host.hostname) + \
        'author/' + str(author.uuid)
    authorDict['host'] = author.host.hostname
    authorDict['displayName'] = author.displayName
    authorDict['github'] = author.github
    authorDict['url'] = str(author.host.hostname) + \
        'author/' + str(author.uuid)
    authorDict['bio'] = author.bio
    authorDict['firstName'] = author.first_name
    authorDict['lastName'] = author.last_name
    authorDict['email'] = author.email
    return authorDict


class CreateAuthorAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CreateAuthorSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        print("VALID")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(request.user)
        print(request.auth)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetAllAuthorsAPIView(APIView):
    def get(self, request):
        authors = Author.objects.filter(host=settings.HOSTNAME)
        authors = list(map(serializeAuthor, authors))
        return Response(authors, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class EditUserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer = AuthorSerializer

    def put(self, request, pk, format=None):
        if request.user.uuid != pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(
            instance=author, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetAuthorAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer

    def get(self, request, pk, format=None):
        author = Author.objects.get(uuid=pk)
        authorDict = serializeAuthor(author)

        friendList = []

        asAuthor = Friend.objects.filter(author=author)
        asFriend = Friend.objects.filter(friend=author)
        friendList += list(map(lambda x: serializeAuthor(x.friend), asAuthor))
        friendList += list(map(lambda x: serializeAuthor(x.author), asFriend))

        authorDict['friends'] = friendList

        return Response(authorDict, status=status.HTTP_200_OK)


class CreatePostAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer

    def create(self, request, pk):
        data = request.data.copy()
        data['author'] = pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetPostAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = GetPostSerializer

    # Returns Post by sending UUID of Post
    def get(self, request, pk, format=None):
        post = Post.objects.get(uuid=pk)
        postDict = serializePost(post)

        return Response(postDict, status=status.HTTP_200_OK)


class GetAllAuthorPostAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = GetPostSerializer

    # Returns All Author's Posts by sending UUID of Author
    def get(self, request, pk, format=None):
        posts = Post.objects.filter(author=pk)
        posts = posts.filter(visibility='PUBLIC')
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllAuthorFriendsAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = FriendSerializer

    # Returns All Author's friends
    def get(self, request, pk, format=None):
        friendList = []

        asAuthor = Friend.objects.filter(author=pk)
        asFriend = Friend.objects.filter(friend=pk)
        friendList += list(map(lambda x: serializeAuthor(x.friend), asAuthor))
        friendList += list(map(lambda x: serializeAuthor(x.author), asFriend))

        return Response(friendList, status=status.HTTP_200_OK)


class GetAllPublicPostsAPIView(APIView):
    serializer_class = GetPostSerializer

    def get(self, request, format=None):
        posts = Post.objects.filter(visibility='PUBLIC')
        data = paginated_result(
            request, posts, GetPostSerializer, 'posts', query='posts')
        return Response(data, status=status.HTTP_200_OK)


class GetAllVisiblePostsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = GetPostSerializer

    def get(self, request, format=None):
        user = request.user
        if str(user) == "AnonymousUser":
            print("Anonymous user")
            posts = Post.objects.filter(visibility='PUBLIC')
            serializer = GetPostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            userUUID = user.uuid
            print(userUUID)
            # -------------
            # public posts
            # -------------

            filteredPosts = Post.objects.filter(visibility='PUBLIC')

            # -------------
            # foaf posts
            # -------------

            foafPosts = Post.objects.filter(visibility='FOAF')

            friends = Friend.objects.filter(author=userUUID).union(
                Friend.objects.filter(friend=userUUID))

            foafUUIDs = []
            friendUUIDs = []
            # for each friend
            for friend in friends:
                # append friend's uuid to foaf
                if friend.friend not in foafUUIDs:
                    foafUUIDs.append(friend.friend)
                    friendUUIDs.append(friend.friend)

                # innerFriends is friend's friends
                innerFriend = Friend.objects.filter(author=friend.friend)
                for f2 in innerFriend:
                    if f2.friend not in foafUUIDs:
                        foafUUIDs.append(f2.friend)

            for uuid in foafUUIDs:
                filteredPosts.union(foafPosts.filter(author=uuid))

            # -------------
            # friend posts
            # -------------

            friendPosts = Post.objects.filter(visibility='FRIENDS')

            for uuid in friendUUIDs:
                filteredPosts.union(friendPosts.filter(author=uuid))

            # -------------
            # private posts
            # -------------

            privatePosts = Post.objects.filter(visibility='PRIVATE')

            filteredPosts.union(privatePosts.filter(author=userUUID))

            # -------------
            # server posts
            # -------------

            author = Author.objects.get(uuid=userUUID)

            serverAuthors = Author.objects.filter(host=author.host)
            print(serverAuthors)

            for author in serverAuthors:
                temp = Post.objects.filter(
                    author=author.uuid, visibility='SERVERONLY')
                # print('temp ok')
                filteredPosts = filteredPosts.union(temp)

            postList = []
            for post in filteredPosts:
                postList.append(serializePost(post))

            return PostPagination().get_paginated_response(postList, author.host)

            # serializer = GetPostSerializer(filteredPosts, many=True)


class DeletePostAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # serializer_class = DeletePostSerializer

    def delete(self, request, pk):
        try:
            post = Post.objects.get(uuid=pk).delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("Post Not Found!", e)
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateCommentAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer

    def create(self, request, pk):
        print(pk)
        data = request.data.copy()
        data['post'] = pk
        data['author'] = request.user.uuid
        print(data)
        serializer = self.get_serializer(data=data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        # print("VALID")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetPostCommentsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, pk):
        comments = Comment.objects.filter(post=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateFriendRequestAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = FriendRequestSerializer

    def create(self, request):
        data = request.data
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetAllAuthorFriendRequest(APIView):
    serializer_class = FriendRequestSerializer

    def get(self, request, pk):
        friend_requests = FriendRequest.objects.filter(to_author=pk)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class GetAllFOAFAPIView(APIView):
    serializer_class = AuthorSerializer

    def get(self, request, pk):
        friends = Friend.objects.filter(author=pk)
        foaf = []
        # for each friend
        for friend in friends:
            # append friend's uuid to foaf
            if friend.friend not in foaf:
                foaf.append(friend.friend)

            # innerFriends is friend's friends
            innerFriend = Friend.objects.filter(author=friend.friend)
            for f2 in innerFriend:
                if f2.friend not in foaf:
                    foaf.append(f2.friend)

        authors = []
        for author in foaf:
            if author.uuid != pk:
                authors.append(Author.objects.get(uuid=author.uuid))

        serializer = AuthorSerializer(authors, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CreateFriendAPIView(CreateAPIView):
    serializer_class = FriendSerializer

    # pk = uuid of friend request
    def create(self, request, pk):
        friendRequest = FriendRequest.objects.get(uuid=pk)

        data = {}
        data['friend'] = friendRequest.to_author
        data['author'] = friendRequest.from_author

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CheckFriendAPIView(APIView):

    def get(self, request, pk1, pk2):
        # checking for friendship
        author1 = Author.objects.get(uuid=pk1)
        author1dict = serializeAuthor(author1)
        author2 = Author.objects.get(uuid=pk2)
        author2dict = serializeAuthor(author2)
        friends = Friend.objects.filter(author=author1, friend=author2).union(
            Friend.objects.filter(author=author2, friend=author1))

        return Response(
            {"query": "friends",
             "authors": [author1dict['id'], author2dict['id']],
             "friends": len(list(friends.all())) != 0
             }
        )


class DeleteFriendAPIView(APIView):

    def delete(self, request, pk, format=None):
        currentUser = request.user
        # determine if user is Friend object's "author" or "friend"
        try:
            friend = Friend.objects.get(author=pk, friend=currentUser)
        except Exception:
            try:
                friend = Friend.objects.get(author=currentUser, friend=pk)
            except Exception:
                print("Friendship doesn't exist!")
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )
        friend.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
