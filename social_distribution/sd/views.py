import os, pdb, json, uuid
from .models import *
from .serializers import *
from .forms import *
from .helper_functions import *
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponse

def explore(request):
    if valid_method(request):
        print_state(request)
        posts = Post.objects.filter(Q(visibility=1 ) & Q(unlisted=0))
        results = paginated_result(posts, request, "feed", query="feed")
        if authenticated(request):
            return render(request, 'sd/main.html', {'current_user': get_current_user(request), 'authenticated': True, 'results': results})
        else:
            return render(request, 'sd/main.html', {'current_user': None, 'authenticated': False, 'results': results})
    else:
        return HttpResponse(status_code=405)


def feed(request):
    if valid_method(request):
        print_state(request)
        if authenticated(request):
            user = get_current_user(request)
            own_posts = Post.objects.filter(Q(author_id=user.uuid))
            pub_posts = Post.objects.filter(Q(visibility=1) & Q(unlisted=0))
            all_posts = own_posts | pub_posts
            results = paginated_result(all_posts, request, "feed", query="feed")
            return render(request, 'sd/main.html', {'current_user': user, 'authenticated': True, 'results': results})
        else:
            print("CONSOLE: Redirecting from Feed because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)

def account(request):
    if valid_method(request):
        print_state(request)
        if authenticated(request):
            user = get_current_user(request)
            page = 'sd/account.html'
            return render(request, page, {'current_user': user, 'authenticated': True})
        else:
            print("CONSOLE: Redirecting from Account to because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def search(request):
    if valid_method(request):
        print_state(request)
        if authenticated(request):
            user = get_current_user(request)

            # Get all authors
            all_authors = Author.objects.exclude(username=user)
            authors = paginated_result(all_authors, request, "feed", query="feed")

            # Get all follows
            my_follows = Follow.objects.filter(follower.username==user)
            follows_me = Follow.objects.filter(following.username==user)
            all_follows = my_follows | follows_me
            follows = paginated_result(all_follows, request, "feed", query="feed")

            # Get all friends
            all_friends = Friend.objects.filter(author.username==user)
            friends = paginated_result(all_friends, request, "feed", query="feed")

            return render(request, 'sd/search.html', {'authors': authors, 'current_user': user}) # , 'follows': follows, 'friends': friends})
        else:
            print("CONSOLE: Redirecting from Search because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def notifications(request):
    if valid_method(request):
        print_state(request)
        if authenticated(request):
            return render(request, 'sd/notifications.html')
        else:            
            print("CONSOLE: Redirecting from Notifications because no one is logged in")
            return redirect('login')
    else:
        return HttpResponse(status_code=405)

def post_comment(request, post_id):
    if valid_method(request):
        print_state(request)
        comments = Comment.objects.filter(post=post_id)
        result = paginated_result(comments, request, "comments", query="comments")
        return HttpResponse("Post Comments Page")
    else:
        return HttpResponse(status_code=405)

def login(request):
    if valid_method(request):
        print_state(request)
        if authenticated(request):
            print("CONSOLE: Logging out "+ get_current_user(request).username)
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
            print("CONSOLE: Incorrect password for "+user_name+", please try again")
            return redirect('login')

        request.session['authenticated'] = True
        user = Author.objects.get(username=user_name) 
        key = user.uuid
        request.session['auth-user'] = str(key)
        request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
        print("CONSOLE: "+user.username+" successfully logged in, redirecting to feed")
        return redirect('my_feed')
    else:
        return HttpResponse(status_code=405)

def register(request):
    if valid_method(request):
        print_state(request)  
        if authenticated(request):
            print("CONSOLE: Logging out "+ get_current_user(request).username)
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
            user = Author.objects.get(username=friend_serializer.data['username'])
            key = user.uuid
            request.session['auth-user'] = str(key)
            request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
            print("CONSOLE: "+user.username+" successfully registered! Redirecting to your feed")
            return redirect('my_feed')
        else:
            return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False} )
    else:
        return HttpResponse(status_code=405)

def logout(request):
    if valid_method(request):
        print_state(request)
        if authenticated(request):
            print("CONSOLE: Logging out "+get_current_user(request).username)
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
        if not authenticated(request):
            print("CONSOLE: Redirecting from friendrequest because no one is logged in.")
            return redirect('login')
        user = get_current_user(request)
        if request.method == "GET":
            return HttpResponse(status_code=405)
        else:
            data = json.loads(request.body)
            target = Author.objects.get(username=data['target_author']) 
            check = FriendRequest.objects.filter(Q(to_author=user.uuid) & Q(from_author=target.uuid))
            # pdb.set_trace()
            info = {'to_author': target.uuid, 'from_author':user.uuid}
            friendreq_serializer = FriendRequestSerializer(data=info)
            if friendreq_serializer.is_valid():
                friendreq_serializer.save()
                info = {'follower': user.uuid, 'following':target.uuid}
                follow_serializer = FollowSerializer(data=info)
                if follow_serializer.is_valid():
                    print("CONSOLE: Following "+target.username)
                else:
                    print("CONSOLE: Couldn't follow "+target.username+" :" +follow_serializer.errors)
                
                resp = HttpResponse(json.dumps({"created":"true"}), content_type='application/json')
                return resp
            else:
                resp = HttpResponse(json.dumps({"created":"false"}), content_type='application/json')
                return resp
    else:
        return HttpResponse(status_code=405)

def new_post(request):
    if valid_method(request):
        print_state(request)
        if not authenticated(request):
            print("CONSOLE: Redirecting from new_post because no one is logged in.")
            return redirect('login')

        user = get_current_user(request)
        if request.method == "GET":
            form = NewPostForm()
            return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})

        else:
            info = dict(request._post)
            for i in info:
                if isinstance(info[i],list):
                    info[i] = info[i][0]
            info['author'] = user.uuid
            friend_serializer = CreatePostSerializer(data=info)
            if friend_serializer.is_valid():
                friend_serializer.save()
                page = 'sd/feed.html'
                print('CONSOLE: Post successful! Redirecting to your feed.')
                return redirect('my_feed')
            else:
                form = NewPostForm()
                print('CONSOLE: Post failed, please try again.')
                return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})
    else:
        return HttpResponse(status_code=405)