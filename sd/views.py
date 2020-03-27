import os
import json
import uuid
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
import social_distribution.settings
import requests


def explore(request):
    if valid_method(request):
        print_state(request)
        posts = Post.objects.filter(Q(visibility='PUBLIC') & (
            Q(unlisted=1) | Q(unlisted='False')))
        results = paginated_result(request, posts, GetPostSerializer, "feed", query="feed")
        is_authenticated = authenticated(request)
        user = get_current_user(request) if is_authenticated else None
        return render(request, 'sd/main.html', {'current_user': user, 'authenticated': is_authenticated, 'results': results})
    else:
        return HttpResponse(status_code=405)


def feed(request):
    if valid_method(request):
        user = get_current_user(request)
        if authenticated(request) and user:
            load_github_feed(get_current_user(request)) 
            all_posts = Post.objects.none()
            own_posts = Post.objects.filter(Q(author_id=user.uuid))
            if own_posts:
                all_posts  = (all_posts | own_posts).distinct()
            following_temp = Follow.objects.filter(Q(follower_id=user.uuid)).values('following') #### NOTE: following is a set of uuid's
            following = []
            for i in following_temp:
                following.append(i['following'])
            f1 = Friend.objects.filter(Q(author=user.uuid)).values('friend')
            f2 = Friend.objects.filter(Q(friend=user.uuid)).values('author')
            friend_ids = []
            for i in f1:
                friend_ids.append(i['friend'])
            for j in f2:
                friend_ids.append(j['author']) 
            #### NOTE:Friends is a subset of following and are author objects

            for f in following: 
                f_user = Author.objects.get(uuid=f)
                their_pub_posts = Post.objects.filter(Q(author=f_user.uuid) & Q(visibility=1) & (Q(unlisted=1) | Q(unlisted='False')))
                if their_pub_posts:
                    all_posts = (all_posts | their_pub_posts).distinct()
                if f_user.host == user.host:
                    server_spec_posts = Post.objects.filter(Q(author=f_user.uuid) & Q(visibility=5) & (Q(unlisted=1) | Q(unlisted='False')))
                    if server_spec_posts:
                        all_posts = (all_posts | server_spec_posts).distinct()
                
                spec_posts= Post.objects.filter(Q(author=f_user.uuid) & Q(visibility=4) & (Q(unlisted=1) | Q(unlisted='False')))
                for post in spec_posts:
                    if user.username in post.visibleTo:
                        all_post = (all_post | post).distinct()
                
                if f_user.uuid in friend_ids:
                    friend_posts = Post.objects.filter(Q(author=f_user.uuid) & Q(visibility=3) & (Q(unlisted=1) | Q(unlisted='False')))
                    if friend_posts:
                        all_post = (all_post | friend_posts).distinct()
                
                for friend in friend_ids:
                    tf1 = Friend.objects.filter(Q(author=friend)).values('friend_id')
                    tf2 = Friend.objects.filter(Q(friend=friend)).values('author_id')
                    their_friends = tf1 | tf2                    #### NOTE:their_friends is a set of uuid's
                    for foaf in their_friends:
                        posts = Post.objects.filter(Q(author=foaf) & Q(visibility=2)& (Q(unlisted=1) | Q(unlisted='False')))
                        if posts:
                            all_post = (all_posts | posts).distinct()
                
                temp = Author.objects.get(fs)

            results = paginated_result(request, all_posts, GetPostSerializer, "feed", query="feed")
            return render(request, 'sd/main.html', {'current_user': user, 'authenticated': True, 'results': results})
        else:
            print("CONSOLE: Redirecting from Feed because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def account(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if authenticated(request) and user:
            page = 'sd/account.html'
            return render(request, page, {'current_user': user, 'authenticated': True})
        else:
            print("CONSOLE: Redirecting from Account to because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def search(request):
    if not valid_method(request):
        return HttpResponse(status_code=405)
    print_state(request)
    user = get_current_user(request)
    if not (authenticated(request) and user):
        print("CONSOLE: Redirecting from Search because no one is logged in")
        return redirect('login')

    # Get all authors
    all_authors = Author.objects.exclude(username=user)
    context = paginated_result(request, all_authors, AuthorSerializer, "authors", query="authors")
    context['authors'] = [author['username'] for author in context['authors']]

    # Get all follows
    my_follows = Follow.objects.filter(Q(follower=user))
    follows_me = Follow.objects.filter(Q(following=user))
    all_follows = my_follows | follows_me

    # The follow object doesn't return names, it returns more objects
    # So I need to put it in a form that JS will understand
    ret_follows = []
    for f in all_follows:
        entry = {}
        entry["follower"] = f.follower.username
        entry["following"] = f.following.username
        entry["follower_uuid"] = f.follower.uuid
        entry["following_uuid"] = f.following.uuid

        ret_follows.append(entry)

    # Get all friends
    all_friends = Friend.objects.filter(
        Q(author=user)) | Friend.objects.filter(Q(friend=user))
    ret_friends = []
    for f in all_friends:
        entry = {}
        if f.friend == user:
            entry["uuid"] = f.author.uuid
            entry["name"] = f.author.username
        else:
            entry["uuid"] = f.friend.uuid
            entry["name"] = f.friend.username
        ret_friends.append(entry)

    context["current_user"] = user
    context["follows"] = ret_follows
    context["friends"] = ret_friends
    return render(request, 'sd/search.html', context)


def notifications(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if authenticated(request) and user:
            fr_requests = FriendRequest.objects.filter(Q(to_author=user))
            all_requests = []
            for a in fr_requests:
                print(a.from_author)
                all_requests.append(a.from_author)

            return render(request, 'sd/notifications.html', {"requests": all_requests})
        else:
            print("CONSOLE: Redirecting from Notifications because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def post_comment(request, post_id):
    if valid_method(request):
        print_state(request)
        comments = Comment.objects.filter(post=post_id)
        result = paginated_result(request, comments, CommentSerializer, "comments", query="comments")
        return HttpResponse("Post Comments Page")
    else:
        return HttpResponse(status_code=405)


def login(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if authenticated(request) and user:
            print("CONSOLE: Logging out " + user.username)
            try:
                request.session['authenticated'] = False
                request.session.pop('auth-user')
                request.session.flush()
            except KeyError as k:
                pass

        if request.method == "GET":
            return render(request, 'sd/login.html', {'current_user': None, 'authenticated': False})
        info = request._post
        user_name = info['username']
        pass_word = info['password']
        try:
            user = Author.objects.get(username=user_name)
        except:
            request.session['authenticated'] = False
            print("CONSOLE: "+user_name+" not found, please try again")
            return redirect('login')

        if (pass_word != user.password) and not (check_password(pass_word, user.password)):
            print("CONSOLE: Incorrect password for " +
                  user_name+", please try again")
            return redirect('login')

        request.session['authenticated'] = True
        user = Author.objects.get(username=user_name)
        key = user.uuid
        request.session['auth-user'] = str(key)
        request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
        print("CONSOLE: "+user.username +
              " successfully logged in, redirecting to feed")
        load_foreign_databases()
        return redirect('my_feed')
    else:
        return HttpResponse(status_code=405)


def register(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if authenticated(request) and user:
            print("CONSOLE: Logging out " + user.username)
            try:
                request.session['authenticated'] = False
                request.session.pop('auth-user')
                request.session.flush()
            except KeyError as k:
                pass

        if request.method == "GET":
            return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False})
        info = request._post
        friend_serializer = CreateAuthorSerializer(data=info)
        if friend_serializer.is_valid():
            friend_serializer.save()
            request.session['authenticated'] = True
            user = Author.objects.get(
                username=friend_serializer.data['username'])
            key = user.uuid
            request.session['auth-user'] = str(key)
            request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
            print("CONSOLE: "+user.username +
                  " successfully registered! Redirecting to your feed")
            return redirect('my_feed')
        else:
            return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False})
    else:
        return HttpResponse(status_code=405)


def logout(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if authenticated(request) and user:
            print("CONSOLE: Logging out " + user.username)
            try:
                request.session['authenticated'] = False
                request.session.pop('auth-user')
                request.session.flush()
            except:
                pass
            return redirect('login')
        else:
            print("CONSOLE: Redirecting from logout because no one is logged in.")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


@csrf_exempt
def friendrequest(request):
    if valid_method(request):
        print_state(request)
        if request.method == "GET":
            return HttpResponse(status_code=405)

        user = get_current_user(request)
        if not authenticated(request) or not user:
            print("CONSOLE: Redirecting from friendrequest because no one is logged in.")
            return redirect('login')
        data = json.loads(request.body)
        target = Author.objects.filter(username=data['target_author'])[0]
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
            print("CONSOLE: "+user.username+" and " +
                  target.username+" are already friends!")
            follows1 = Follow.objects.filter(
                Q(follower=target.uuid) & Q(following=user.uuid))
            if not follows1.count():
                s = FollowSerializer(
                    data={'follower': target.uuid, 'following': user.uuid})
                if s.is_valid():
                    print("CONSOLE: Created a Follow from target to user")
                    s.save()
            follows2 = Follow.objects.filter(
                Q(follower=user.uuid) & Q(following=target.uuid))
            if not follows2.count():
                s = FollowSerializer(
                    data={'follower': user.uuid, 'following': target.uuid})
                if s.is_valid():
                    print("CONSOLE: Created a Follow from user to target")
                    s.save()
            # creates Follow objects in case they don't already exist
            return HttpResponse(json.dumps({'status': 'friends'}), content_type='application/json')

        elif relationship == 2:
            info = {'author': user.uuid, 'friend': target.uuid}
            friend = Friend.objects.create(author=user.uuid, friend=target.uuid)
            if friend.is_valid():
                friend.save()
                obj.delete()
                print("CONSOLE: "+user.username+" and " +
                      target.username+" are now friends!")
            follows1 = Follow.objects.filter(
                Q(follower=target.uuid) & Q(following=user.uuid))
            if not follows1.count():
                s = FollowSerializer(
                    data={'follower': target.uuid, 'following': user.uuid})
                if s.is_valid():
                    print("CONSOLE: Created a Follow from target to user")
                    s.save()
            follows2 = Follow.objects.filter(
                Q(follower=user.uuid) & Q(following=target.uuid))
            if not follows2.count():
                s = FollowSerializer(
                    data={'follower': user.uuid, 'following': target.uuid})
                if s.is_valid():
                    print("CONSOLE: Created a Follow from user to target")
                    s.save()
            return HttpResponse(json.dumps({'status': 'friends'}), content_type='application/json')

        elif relationship == 3:
            print("CONSOLE: "+user.username+" is already following " +
                  target.username+". Returning")
            follows1 = Follow.objects.filter(
                Q(follower=target.uuid) & Q(following=user.uuid))
            if not follows1.count():
                s = FollowSerializer(
                    data={'follower': user.uuid, 'following': target.uuid})
                if s.is_valid():
                    print("CONSOLE: Created a Follow from user to target")
                    s.save()

            return HttpResponse(json.dumps({'status': 'following'}), content_type='application/json')

        elif relationship == 4:
            info = {'to_author': target.uuid, 'from_author': user.uuid}
            friendreq_serializer = FriendRequestSerializer(data=info)
            if friendreq_serializer.is_valid():
                friendreq_serializer.save()
                print("CONSOLE: "+user.username +
                      " sent a friend request to "+target.username)
            follows1 = Follow.objects.filter(
                Q(follower=target.uuid) & Q(following=user.uuid))
            if not follows1.count():
                s = FollowSerializer(
                    data={'follower': user.uuid, 'following': target.uuid})
                if s.is_valid():
                    print("CONSOLE: Created a Follow from user to target")
                    s.save()

            return HttpResponse(json.dumps({'status': 'following'}), content_type='application/json')
    else:
        return HttpResponse(status_code=405)


def new_post(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if not authenticated(request) or not user:
            print("CONSOLE: Redirecting from new_post because no one is logged in.")
            return redirect('login')

        if request.method == "GET":
            form = NewPostForm()
            return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})

        else:
            if request.FILES:
                myfile = request.FILES['image']
                info = dict(request._post)
                for i in info:
                    if isinstance(info[i], list):
                        info[i] = info[i][0]
                info['author'] = user.uuid
                form = NewPostForm(info, request.FILES)
                if form.is_valid():
                    post = form.save()
                    post.link_to_image = 'media/'+post.image.name
                    post.save()
                    print('CONSOLE: Post successful! Redirecting to your feed.')
                    return redirect('my_feed')
                else:
                    print('CONSOLE: Post failed, please try again.')
                    return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})
            else:
                info = dict(request._post)
                for i in info:
                    if isinstance(info[i], list):
                        info[i] = info[i][0]
                info['author'] = user.uuid
                form = NewPostForm(info)
                if form.is_valid():
                    post = form.save()
                    post.save()
                    print('CONSOLE: Post successful! Redirecting to your feed.')
                    return redirect('my_feed')
                else:
                    print('CONSOLE: Post failed, please try again.')
                    return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})
    else:
        return HttpResponse(status_code=405)


def get_image(request, url):
    path = 'media/'+url
    try:
        with open(path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except:
        return HttpResponse(open('media/404.jpg', 'rb').read(), content_type="image/jpeg")


def edit_post(request, post_id):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if not authenticated(request) or not user:
            print("CONSOLE: Redirecting from edit_post because no one is logged in.")
            return redirect('login')

        post = Post.objects.get(uuid=post_id)
        if(user.uuid != post.author_id):
            print(
                "CONSOLE: Redirecting from edit_post because the post does not belong to logged in user.")
            return redirect('my_feed')

        if request.method == "GET":
            form = EditPostForm(instance=post)
            return render(request, 'sd/edit_post.html', {'form': form, 'current_user': user, 'authenticated': True})
        else:
            data = request.POST
            post.title = data['title']
            post.description = data['description']
            post.content = data['content']
            post.source = data['source']
            post.contentType = data['contentType']
            post.categories = data['categories']
            post.visibility = data['visibility']
            post.unlisted = data['unlisted']
            post.save()
            return redirect('my_feed')
    else:
        return HttpResponse(status_code=405)


@csrf_exempt
def delete_post(request, post_id):
    if request.method == "DELETE":
        user = get_current_user(request)
        if authenticated(request) and user:
            post = Post.objects.get(uuid=post_id)
            if post.author.uuid == user.uuid:
                post.delete()
                print("CONSOLE: Post deleted successfully.")
            else:
                print("CONSOLE: Unable to delete post.")
                return HttpResponse(status_code=403)
            return HttpResponse()
        else:
            print(
                "CONSOLE: Redirecting from Delete post function because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def edit_account(request):
    if valid_method(request):
        print_state(request)
        user = get_current_user(request)
        if not authenticated(request) or not user:
            print("CONSOLE: Redirecting from edit_post because no one is logged in.")
            return redirect('login')

        details = Author.objects.get(uuid=user.uuid)
        if request.method == "GET":
            form = EditAccountForm(instance=user)
            return render(request, 'sd/edit_account.html', {'form': form, 'current_user': user, 'authenticated': True})
        else:
            data = request.POST
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.username = data['username']
            user.email = data['email']
            user.bio = data['bio']
            user.github = data['github']
            user.save()
            return redirect('account')
    else:
        return HttpResponse(status_code=405)
