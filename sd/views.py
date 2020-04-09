import json, uuid, base64, requests, commonmark
from .forms import *
from .models import *
from .serializers import *
from .helper_functions import *
from django.db.models import Q
import social_distribution.settings
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponse

def explore(request):
    if valid_method(request):
        if request.method == "GET":
            user = get_current_user(request)
            if user:
                posts = Post.objects.filter(Q(visibility='PUBLIC') & Q(
                    unlisted=False)).exclude(author_id=user.uuid).order_by('-published')
            else:
                posts = Post.objects.filter(
                    Q(visibility='PUBLIC') & Q(unlisted=False)).order_by('-published')

            for p in posts:
                if p.contentType == 'text/markdown':
                    temp_content = commonmark.commonmark(p.content)
                    p.content = temp_content.replace('<img', '<img class=\"content-image\"')
            results = paginated_result(
                request, posts, GetPostSerializer, "feed", query="feed")
            is_authenticated = authenticated(request)
            user = get_current_user(request) if is_authenticated else None
            all_comments = Comment.objects.all().order_by('published')
            comments = []
            for c in all_comments:
                comments.append({
                    'post': str(c.post.uuid),
                    'author': c.author,
                    'comment': c.comment,
                    'published': c.published
                })

            # Get all authors
            ret_authors = []
            all_authors = Author.objects.all()
            for a in all_authors:
                entry = {}
                entry['name'] = a.username
                entry['uuid'] = a.uuid
                ret_authors.append(entry)

            return render(request, 'sd/main.html', {'current_user': user, 'authenticated': is_authenticated, 'results': results, 'comments':comments,'all_authors':ret_authors})
        elif request.method=="POST":
            data = request.POST
            author = Author.objects.get(uuid=data['user'])
            post = Post.objects.get(uuid=data['post'])
            comment = Comment.objects.create(author=author, comment=
            data['comment'], contentType= 'text/plain', post=post)
            comment.save()
            return redirect('explore')
    else:
        return HttpResponse(status_code=405)

def feed(request):
    if valid_method(request):
        if request.method == 'GET':
            user = get_current_user(request)
            if authenticated(request) and user:
                load_github_feed(get_current_user(request))
                all_posts = Post.objects.none()
                own_posts = Post.objects.filter(Q(author_id=user.uuid))
                if own_posts:
                    all_posts = all_posts.union(own_posts)
                following_temp = Follow.objects.filter(Q(follower_id=user.uuid)).values(
                    'following')  # NOTE: following is a set of uuid's
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
                # NOTE:Friends is a subset of following and are author objects

                for f in following:
                    f_user = Author.objects.get(uuid=f)
                    their_pub_posts = Post.objects.filter(
                        Q(author=f_user.uuid) & Q(visibility='PUBLIC') & Q(unlisted=False))
                    if their_pub_posts:
                        all_posts = all_posts.union(their_pub_posts)

                    spec_posts = Post.objects.filter(Q(author=f_user.uuid) & Q(
                        visibility='PRIVATE') & Q(unlisted=False) & Q(visibleTo__contains=user.username))
                    if spec_posts:
                        all_posts = all_posts.union(spec_posts)

                    if f_user.uuid in friend_ids:
                        friend_posts = Post.objects.filter(Q(author=f_user.uuid) & (Q(
                            visibility='FRIENDS') | Q(visibility='FOAF')) & Q(unlisted=False))
                        if f_user.host == user.host:
                            server_spec_posts = Post.objects.filter(
                                Q(author=f_user.uuid) & Q(visibility='SERVERONLY') & Q(unlisted=False))
                            if server_spec_posts:
                                all_posts = all_posts.union(server_spec_posts)
                        if friend_posts:
                            all_posts = all_posts.union(friend_posts)

                for friend in friend_ids:
                    tf1 = Friend.objects.filter(
                        Q(author=friend)).values('friend_id')
                    tf2 = Friend.objects.filter(
                        Q(friend=friend)).values('author_id')
                    # NOTE:their_friends is a list of dictionaries of 'friend_id':<id> or 'author_id':<id>
                    their_friends = tf1.union(tf2)

                    for foaf in their_friends:
                        posts = []
                        if 'friend_id' in foaf and foaf['friend_id'] in following:
                            posts = Post.objects.filter(Q(author=foaf['friend_id']) & Q(
                                visibility='FOAF') & Q(unlisted=False))
                        elif 'author_id' in foaf and foaf['author_id'] in following:
                            posts = Post.objects.filter(Q(author=foaf['author_id']) & Q(
                                visibility='FOAF') & Q(unlisted=False))
                        if posts:
                            all_posts = all_posts.union(posts)

                all_posts = all_posts.distinct().order_by('-published')
                for p in all_posts:
                    if p.contentType == 'text/markdown':
                        temp_content = commonmark.commonmark(p.content)
                        p.content = temp_content.replace('<img', '<img class=\"content-image\"')
                results = paginated_result(
                    request, all_posts, GetPostSerializer, "feed", query="feed")
                all_comments = Comment.objects.all().order_by('published')
                comments = []
                for c in all_comments:
                    comments.append({
                        'post': str(c.post.uuid),
                        'author': c.author,
                        'comment': c.comment,
                        'published': c.published
                    })

                # Get all authors
                ret_authors = []
                all_authors = Author.objects.all()
                for a in all_authors:
                    entry = {}
                    entry['name'] = a.username
                    entry['uuid'] = a.uuid
                    ret_authors.append(entry)

                return render(request, 'sd/main.html', {'current_user': user, 'authenticated': True, 'results': results, 'comments':comments, 'all_authors':ret_authors})
            else:
                return redirect('login')
        elif request.method=="POST":
            data = request.POST
            author = Author.objects.get(uuid=data['user'])
            post = Post.objects.get(uuid=data['post'])
            comment = Comment.objects.create(author=author, comment=
            data['comment'], contentType= 'text/plain', post=post)
            comment.save()
            return redirect('my_feed')

    else:
        return HttpResponse(status_code=405)


def account(request):
    if valid_method(request):
        user = get_current_user(request)
        if authenticated(request) and user:
            page = 'sd/account.html'
            return render(request, page, {'current_user': user, 'authenticated': True})
        else:
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def search(request):
    if not valid_method(request):
        return HttpResponse(status_code=405)
    user = get_current_user(request)
    if not (authenticated(request) and user):
        return redirect('login')

    # Get all authors
    ret_authors = []
    all_authors = Author.objects.exclude(username=user)
    for a in all_authors:
        entry = {}
        entry['name']=a.username
        if a.host == user.host:
            entry["host"] = 'Local'
        else:
            entry["host"] = 'Remote'
        ret_authors.append(entry)



    # Get all follows
    my_follows = Follow.objects.filter(Q(follower=user))
    follows_me = Follow.objects.filter(Q(following=user))
    all_follows = my_follows.union(follows_me)

    # The follow object doesn't return names, it returns more objects
    # So I need to put it in a form that JS will understand
    ret_follows = []
    for f in all_follows:
        entry = {}
        entry["follower"] = f.follower.username
        entry["following"] = f.following.username
        entry["follower_uuid"] = f.follower.uuid
        entry["following_uuid"] = f.following.uuid

        #see if they are local or remote
        if f.following.host == user.host:
            entry["followinghost"] = 'Local'
        else:
            entry["followinghost"] = 'Remote'
        if f.follower.host == user.host:
            entry["followerhost"] = 'Local'
        else:
            entry["followerhost"] = 'Remote'

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
            if f.author.host == user.host:
                entry["host"] = 'Local'
            else:
                entry["host"] = 'Remote'
        else:
            entry["uuid"] = f.friend.uuid
            entry["name"] = f.friend.username
            if f.friend.host == user.host:
                entry["host"] = 'Local'
            else:
                entry["host"] = 'Remote'            
        ret_friends.append(entry)

    context = {}
    context['authors'] = [author.username for author in all_authors]
    context['authors_full'] = ret_authors
    context["current_user"] = user
    context["follows"] = ret_follows
    context["friends"] = ret_friends
    return render(request, 'sd/search.html', context)


def notifications(request):
    if valid_method(request):
        user = get_current_user(request)
        if authenticated(request) and user:

            # Get all friend requests
            fr_requests = FriendRequest.objects.filter(Q(to_author=user) & Q(rejected=False))
            all_requests = []
            for a in fr_requests:
                entry = {}
                entry["name"] = a.from_author.username
                if a.from_author.host == user.host:
                    entry["host"] = 'Local'
                else:
                    entry["host"] = 'Remote'
                all_requests.append(entry)

            # Get all authors
            all_authors = Author.objects.exclude(username=user)

            # Get all users that current user follows
            my_follows = Follow.objects.filter(Q(follower=user))
            follows_me = Follow.objects.filter(Q(following=user))

            #find a list of people who follow you
            follows_me_list = []
            for f in follows_me:
                follows_me_list.append(f.follower.uuid)

            # The follow object doesn't return names, it returns more objects
            # So I need to put it in a form that JS will understand
            # only returns people you follow if you are not friends with them (they don't follow you back)
            ret_follows = []
            for f in my_follows:
                if f.following.uuid not in follows_me_list:
                    entry = {}
                    entry["following"] = f.following.username
                    entry["following_uuid"] = f.following.uuid
                    if f.following.host == user.host:
                        entry["host"] = 'Local'
                    else:
                        entry["host"] = 'Remote'
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
                    if f.author.host == user.host:
                        entry["host"] = 'Local'
                    else:
                        entry["host"] = 'Remote'
                else:
                    entry["uuid"] = f.friend.uuid
                    entry["name"] = f.friend.username
                    if f.friend.host == user.host:
                        entry["host"] = 'Local'
                    else:
                        entry["host"] = 'Remote'
                ret_friends.append(entry)
            
            context = {}
            context['authors'] = [author.username for author in all_authors]
            context["current_user"] = user
            context["follows"] = ret_follows
            context["friends"] = ret_friends
            context["requests"] = all_requests

            return render(request, 'sd/notifications.html', context)
        else:
            return redirect('login')
    else:
        return HttpResponse(status_code=405)


def post_comment(request, post_id):
    if valid_method(request):
        comments = Comment.objects.filter(post=post_id)
        result = paginated_result(
            request, comments, CommentSerializer, "comments", query="comments")
        return HttpResponse("Post Comments Page")
    else:
        return HttpResponse(status_code=405)


def login(request):
    if valid_method(request):
        user = get_current_user(request)
        if authenticated(request) and user:
            try:
                request.session['authenticated'] = False
                request.session.pop('auth-user')
                request.session.flush()
            except:
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
            errors = "No account found for "+user_name+". Please check the spelling and try again."
            return render(request, 'sd/login.html', {'username':user_name, 'errors':errors})

        if (pass_word != user.password) and not (check_password(pass_word, user.password)):
            errors = "Invalid password, please try again."
            return render(request, 'sd/login.html', {'username':user_name, 'errors':errors})
        
        elif not user.verified:
            errors = "Unverified user. Please wait until the administrators approve your account."
            return render(request, 'sd/login.html', {'username':user_name, 'errors':errors})

        request.session['authenticated'] = True
        key = user.uuid
        request.session['auth-user'] = str(key)
        request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True

        load_foreign_databases()
        return redirect('my_feed')
    else:
        return HttpResponse(status_code=405)


def register(request):
    if valid_method(request):
        user = get_current_user(request)
        if authenticated(request) and user:
            try:
                request.session['authenticated'] = False
                request.session.pop('auth-user')
                request.session.flush()
            except:
                pass

        if request.method == "GET":
            return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False})
        info = request._post
        try:
            author_serializer = CreateAuthorSerializer(data=info)
            if author_serializer.is_valid():
                author_serializer.save()
                request.session['authenticated'] = True
                user = Author.objects.get(
                    username=author_serializer.data['username'])
                key = user.uuid
                request.session['auth-user'] = str(key)
                request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
                return redirect('my_feed')
            else:
                errors = "Username taken"
                return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False, 'errors':errors, 'first_name':info['first_name'], 'last_name':info['last_name'], 'username':info['username'], 'email':info['email']})
        except:
            errors = "Username taken"
            return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False, 'errors':errors, 'first_name':info['first_name'], 'last_name':info['last_name'], 'username':info['username'], 'email':info['email']})
    else:
        return HttpResponse(status_code=405)


def logout(request):
    if valid_method(request):
        user = get_current_user(request)
        if authenticated(request) and user:
            try:
                request.session['authenticated'] = False
                request.session.pop('auth-user')
                request.session.flush()
            except:
                pass
            return redirect('login')
        else:
            return redirect('login')
    else:
        return HttpResponse(status_code=405)

def new_post(request):
    if valid_method(request):
        user = get_current_user(request)
        if not authenticated(request) or not user:
            return redirect('login')

        if request.method == "GET":
            form = NewPostForm()
            return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})

        else:
            if request.FILES:
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
                    with open(post.link_to_image, "rb") as image:
                        temp = base64.b64encode(image.read())    
                    post.link_to_image = temp.decode('utf-8')
                    post.save()
                    return redirect('my_feed')
                else:
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
                    return redirect('my_feed')
                else:
                    return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})
    else:
        return HttpResponse(status_code=405)


def get_image(request, pk):
    if request.method == "GET":
        try:
            post = Post.objects.get(uuid=pk)
        except:
            return render(request, 'sd/404.html', status=404) #Can't find user, return Not Found

        if post.image and post.link_to_image:

            if post.visibility=="PUBLIC":
                img_format = post.image.name.split('.')[-1]
                outfile = open('temp.'+img_format, 'wb')
                outfile.write(base64.b64decode(post.link_to_image))
                outfile.close()
                with open(outfile.name, 'rb') as out:
                    return HttpResponse(out, content_type='image/'+img_format) #200

            try:
                user = get_current_user(request)
                target = post.author
            except:
                return render(request, 'sd/404.html', status=404) #Author not found, return Not Found
            
            if user==target:
                img_format = post.image.name.split('.')[-1]
                outfile = open('temp.'+img_format, 'wb')
                outfile.write(base64.b64decode(post.link_to_image))
                outfile.close()
                with open(outfile.name, 'rb') as out:
                    return HttpResponse(out, content_type='image/'+img_format) #200

            my_friends = Friend.objects.filter(Q(author=user.uuid) | Q(friend=user.uuid))
            f1 = Friend.objects.filter(Q(author=user.uuid)).values('friend')
            f2 = Friend.objects.filter(Q(friend=user.uuid)).values('author')
            friend_ids = []
            for i in f1:
                friend_ids.append(i['friend'])
            for j in f2:
                friend_ids.append(j['author'])
            friend_check = my_friends.filter(Q(author=target.uuid) | Q(friend=target.uuid))
            if friend_check and (post.visibility=="FRIENDS" or post.visibility=="FOAF"):
                img_format = post.image.name.split('.')[-1]
                outfile = open('temp.'+img_format, 'wb')
                outfile.write(base64.b64decode(post.link_to_image))
                outfile.close()
                with open(outfile.name, 'rb') as out:
                    return HttpResponse(out, content_type='image/'+img_format) #200

            if friend_check and post.visibility=="SERVERONLY" and target.host==user.host:
                img_format = post.image.name.split('.')[-1]
                outfile = open('temp.'+img_format, 'wb')
                outfile.write(base64.b64decode(post.link_to_image))
                outfile.close()
                with open(outfile.name, 'rb') as out:
                    return HttpResponse(out, content_type='image/'+img_format) #200

            if post.visibility == "FOAF":
                for friend in friend_ids:
                    friends_of_friends = Friend.objects.filter(Q(author=friend)|Q(friend=friend)).exclude(author=user).exclude(friend=user)
                foaf_check = friends_of_friends.filter(Q(author=target.uuid) | Q(friend=target.uuid))
                if foaf_check:
                    img_format = post.image.name.split('.')[-1]
                    outfile = open('temp.'+img_format, 'wb')
                    outfile.write(base64.b64decode(post.link_to_image))
                    outfile.close()
                    with open(outfile.name, 'rb') as out:
                        return HttpResponse(out, content_type='image/'+img_format) #200
            
            if post.visibility == "PRIVATE" and user.username in post.visibleTo:
                img_format = post.image.name.split('.')[-1]
                outfile = open('temp.'+img_format, 'wb')
                outfile.write(base64.b64decode(post.link_to_image))
                outfile.close()
                with open(outfile.name, 'rb') as out:
                    return HttpResponse(out, content_type='image/'+img_format) #200
        
            return render(request, 'sd/401.html', status=401) #Checked all the rules and you're not allowed to see it
        else:
            return render(request, 'sd/404.html', status=404) #Can't find no image/link to image        
    else:
        return HttpResponse(status_code=405) # Bad Method


def edit_post(request, post_id):
    if valid_method(request):
        user = get_current_user(request)
        if not authenticated(request) or not user:
            return redirect('login')

        post = Post.objects.get(uuid=post_id)
        if(user.uuid != post.author_id):
            return redirect('my_feed')

        if request.method == "GET":
            form = EditPostForm(instance=post)
            return render(request, 'sd/edit_post.html', {'form': form, 'current_user': user, 'authenticated': True})
        else:
            data = request.POST
            post.title = data['title']
            post.content = data['content']
            post.contentType = data['contentType']
            post.description = data['description']
            post.categories = data['categories']
            post.visibility = data['visibility']
            post.visibleTo = data['visibleTo']
            post.unlisted = data['unlisted']
            post.save()
            return redirect('my_feed')
    else:
        return HttpResponse(status_code=405)

def edit_account(request):
    if valid_method(request):
        user = get_current_user(request)
        if not authenticated(request) or not user:
            return redirect('login')

        if request.method == "GET":
            form = EditAccountForm(instance=user)
            return render(request, 'sd/edit_account.html', {'form': form, 'current_user': user, 'authenticated': True})
        else:
            data = request.POST
            if Author.objects.filter(username=data['username']).exclude(uuid=user.uuid):
                errors = "Username taken"
                return render(request, 'sd/edit_account.html', {'form': EditAccountForm(instance=user), 'current_user': user, 'authenticated': True, 'errors':errors})
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

def verify(request):
    if request.method == "GET":
        if authenticated(request) and get_current_user(request).is_superuser and get_current_user(request).is_staff:
            unverified = Author.objects.filter(Q(verified=False))
            all_users = Author.objects.all()
            return render(request, 'sd/verify.html', {'unverified': unverified, 'allusers': all_users})
        else:
            return render(request, 'sd/401.html', status=401)
    else:
        return render(request, 'sd/405.html', status=405)