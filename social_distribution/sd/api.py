from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
import json
from .models import *
from .serializers import *
from uuid import UUID

class squawkJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)

def api_response(jsonContent):
    return HttpResponse(json.dumps(jsonContent, cls=squawkJSONEncoder), content_type="application/json", status=200)

def posts(request, **kwargs):# GET, POST (createPost)
    if request.method == 'GET':
        posts = Post.objects.all()
        posts = CreatePostSerializer(posts, many=True).data
        response ={}
        response['query'] = 'posts'
        response['posts'] = list(posts)
        return api_response(response)
    elif request.method == 'POST':
        return api_response({"query":"createPost"})

def author_posts(request, **kwargs):# GET
    if request.method == 'GET':
        return posts(request) #################################################### currently authenticated API user??

def friendrequest(request, **kwargs):# POST (friendRequest)
    if request.method == 'POST':
        return api_response({"query":"friendRequest"})

def posts_postid(request, **kwargs):# GET, POST (getPost - foaf)
    if request.method == 'GET':
        try:
            post = Post.objects.get(uuid=kwargs['post_id'])
        except:
            return HttpResponseNotFound("This post does not exist.")
        response = CreatePostSerializer(post).data
        response['query'] = 'getPost'
        return api_response(response)
    elif request.method == 'POST':
        return api_response({"query":"getPost"})

def author_authorid(request, **kwargs):# GET
    if request.method == 'GET':
        try:
            author = Author.objects.get(uuid=kwargs['author_id'])
        except:
            return HttpResponseNotFound("This author does not exist.")
        response = AuthorSerializer(author).data
        return api_response(response)

def author_authorid_posts(request, **kwargs):# GET
    if request.method == 'GET':
        posts = Post.objects.filter(author=kwargs['author_id'])
        posts = CreatePostSerializer(posts, many=True).data
        response ={}
        response['query'] = 'posts'
        response['posts'] = list(posts)
        return api_response(response)

def posts_postid_comments(request, **kwargs):# GET, POST (addComment)
    if request.method == 'GET':
        response = {"query":"comments"}
        return api_response(response)
    elif request.method == 'POST':
        return api_response({"query":"addComment"})

def author_authorid_friends(request, **kwargs):# GET, POST (friends - intersectFriends)
    if request.method == 'GET':
        response = {"query":"friends"}
        friends = FriendList.objects.filter(author=kwargs['author_id'])
        response['authors'] = FriendListSerializer(friends, many=True).data
        return api_response(response)
    elif request.method == 'POST':
        return api_response({"query":"friends"})

def author_authorid_friends_otherid(request, **kwargs):# GET
    if request.method == 'GET':
        response = {"query":"friends"}
        response['authors'] = kwargs['other_id'].hex
        response['friends'] = FriendList.objects.filter(author=kwargs['author_id'], friend=kwargs['other_id']).exists()
        return api_response(response)
