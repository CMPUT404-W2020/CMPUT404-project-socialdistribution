import uuid, requests, datetime, json
from .models import *
from .serializers import *
from django.db.models import Q



def valid_method(request):
    return request.method in ("GET", "POST")


def authenticated(request):
    try:
        return request.session['authenticated'] == True
    except KeyError as k:
        return False


def get_current_user(request):
    try:
        uid = request.session['auth-user']
        new_id = uuid.UUID(uid)
        return Author.objects.get(uuid=new_id)
    except:
        return None


def paginated_result(request, objects, serializer, keyword, **result):
    page_num = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    first_result = size*page_num
    count = objects.count()
    if count <= first_result:
        first_result = 0
        page_num = 0
    last_result = first_result + size

    result["count"] = count
    result["size"] = size
    if page_num >= 1:
        result["previous"] = page_num - 1
    if objects.count() >= last_result:
        result["next"] = page_num + 1
    result[keyword] = list(serializer(objects[first_result:last_result], many=True).data)
    return result


def print_state(request):
    user = get_current_user(request)
    if user and authenticated(request):
        print("CONSOLE: Authenticated user: "+user.username)
    else:
        print("CONSOLE: Browsing as non-authenticated user.")


def get_relationship(user, target):
    f1 = Friend.objects.filter(Q(author=user.uuid) & Q(friend=target.uuid))
    f2 = Friend.objects.filter(Q(author=target.uuid) & Q(friend=user.uuid))
    fr1 = FriendRequest.objects.filter(
        Q(to_author=user.uuid) & Q(from_author=target.uuid))
    fr2 = FriendRequest.objects.filter(
        Q(to_author=target.uuid) & Q(from_author=user.uuid))
    friends = f1.union(f2)
    if friends:
        # if the two users are friends, delete any friend requests between the two of them, if any. working with the logic that an existing Friend objects trumps any friendrequest data
        if(fr1.union(fr2)):
            (fr1.union(fr2)).delete()
        return 1, None  # friends
    if fr1:
        return 2, fr1  # target follows user
    if fr2:
        return 3, fr2 #user follows target
    return 4,None #no relationship

def load_github_feed(user):
    if user.github != '':
        try:
            repo_data = json.loads(requests.get('https://api.github.com/users/'+user.github+'/repos').content.decode())
            repo_names = []
            current = datetime.datetime.now()
            for repo in repo_data:
                if 'pushed_at' in repo_data:
                    d = repo_data['pushed_at'].split('T')[0].split('-')
                    date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
                    if(current-date).days < 30:
                        repo_names.append(repo['name'])
            for r in repo_names:
                commit_data = json.loads(requests.get('https://api.github.com/repos/'+user.github+'/' + r + '/commits').content.decode())
                posts = []
                for com in commit_data:
                    d = com['commit']['author']['date'].split('T')[0].split('-')
                    date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
                    if(current-date).days < 30:
                        exists = Post.objects.filter(source=com['sha'])
                        if not exists:
                            try:
                                info = {'title' : "Commit to "+r, 'source':com['sha'], 'description':'Commit', 'contentType' : 2, 'content' : com['commit']['author']['date'].split('T')[0]+': '+com['committer']['login'].upper()+': '+com['commit']['message'], 'author' : user, 'categories' : 'github', 'visibility' : 'SERVERONLY', 'unlisted' : False, 'link_to_image' : com['committer']['avatar_url']}
                                post = PostSerializer(data=info)
                                if post.is_valid():
                                    post.save()
                            except Exception as e:
                                print("CONSOLE: Error creating Github post", e)
                        else:
                            pass
        except (ConnectionError, IndexError, KeyError) as e:
            print("CONSOLE: ",e)

def load_foreign_databases():
    for node in Node.objects.exclude(hostname=settings.HOSTNAME):
        # delete existing contents
        Author.objects.filter(host=node.hostname).delete()

        try:
            authors = requests.get(node.hostname + 'author').json()
            for author in authors:
                if author['host'] != node.hostname:
                    continue
                Author(uuid=author['id'],
                       username=author['displayName'],
                       password='password',
                       github=author['github'],
                       host=node).save()
        except:
            pass

        try:
            posts = requests.get(node.hostname + 'posts').json()
        except:
            try:
                posts = requests.get(node.hostname + 'posts/').json()
            except Exception as e:
                posts = {}
        while True:
            for post in posts.get('posts',[]):
                try:
                    author = Author.objects.get(uuid=post['author']['id'])
                except:
                    author = Author(uuid=post['author']['id'],
                                    username=post['author']['displayName'],
                                    password='password',
                                    github=post['author']['github'],
                                    host=node)
                    author.save()
                comments = post.get('comments',[])
                info = {'uuid':post.get('id', 'NOUUIDFOUND'), 'title' : post.get('title', 'NOTITLEFOUND'), 'source':post.get('source', node), 'description':post.get('description', 'NODESCRIPTIONFOUND'), 'contentType' : post.get('contentType', 'text/plain'), 'content' : post.get('content', 'NOCONTENTFOUND'), 'author' : author, 'visibility' : post.get('visibility','PUBLIC'), 'unlisted' : post.get('unlisted', False), 'visibleTo':'', 'link_to_image':''}
                # post = Post(uuid=post.get('id', 'NOUUIDFOUND'),
                #      title=post.get('title', 'NOTITLEFOUND'),
                #      source=post.get('source', node),
                #      origin=post.get('source', node),
                #      content=post.get('content', 'NOCONTENTFOUND'),
                #      description=post.get('description', 'NODESCRIPTIONFOUND'),
                #      contentType=post.get('contentType', 'text/plain'),
                #      author=author,
                #      #categories
                #      published=post.get('published', 'NOPUBLISHDATEFOUND'),
                #      unlisted=post.get('unlisted', False),
                #      visibility=post.get('visibility','PUBLIC'),
                #      #visibleTo
                #      )
                # post.save()
                post = PostSerializer(data=info)
                if post.is_valid():
                    post.save()
                for comment in comments:
                     try:
                         author = Author.objects.get(uuid=comment['author']['id'])
                     except:
                         continue
                     Comment(uuid=comment.get('id', 'NOUUIDFOUND'),
                             comment=comment.get('comment', 'NOTITLEFOUND'),
                             published=comment.get('published', 'NOPUBLISHDATEFOUND'),
                             contentType=comment.get('contentType', 'text/plain'),
                             author=author,
                             post=post
                             ).save()
            try:
                posts = requests.get('{}posts?page={}'.format(node.hostname, int(posts['next']))).json()
            except:
                break
