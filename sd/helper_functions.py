import uuid, requests, datetime, json, re
from .models import *
from django.db.models import Q
from django.db import IntegrityError


def valid_method(request):
    return request.method in ("GET", "POST")


def authenticated(request):
    try:
        return request.session['authenticated'] and get_current_user(request).verified
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
    print('CONSOLE: request details:', request.GET)
    page_num = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 10))
    first_result = size*(page_num-1)
    count = objects.count()
    if count <= first_result:
        first_result = 0
        page_num = 1
    last_result = first_result + size

    result["count"] = count
    result["size"] = size
    if page_num > 1:
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
                if 'pushed_at' in repo:
                    d = repo['pushed_at'].split('T')[0].split('-')
                    date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
                    if(current-date).days < 30:
                        repo_names.append(repo['name'])
            print("CONSOLE: repo_names", repo_names)
            for r in repo_names:
                commit_data = json.loads(requests.get('https://api.github.com/repos/'+user.github+'/' + r + '/commits').content.decode())
                posts = []
                for com in commit_data:
                    d = com['commit']['author']['date'].split('T')[0].split('-')
                    date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
                    if(current-date).days < 30:
                        exists = Post.objects.filter(description=com['node_id'])
                        if not exists:
                            try:
                                post = Post.objects.create(title = "Commit to "+r, source=user.host, description=com['node_id'], contentType = 2, content = com['commit']['author']['date'].split('T')[0]+': '+com['committer']['login'].upper()+': '+com['commit']['message'], author = user, categories = 'github', visibility='PRIVATE', unlisted=False, link_to_image=com['committer']['avatar_url'])
                                print("CONSOLE: Created a Github post: "+com['commit']['message'])
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

        trimmed_name = node.hostname.split('https://')[1].split('.herokuapp.com/')[0]

        try:
            authors = requests.get(node.hostname + 'author').json()
            for author in authors:
                if author['host'] != node.hostname:
                    continue
                new_author = Author(uuid=author['id'],
                       username=author['displayName'],
                       password='password',
                       github=author['github'],
                       host=node)
        except IntegrityError:
            new_author.username = new_author.username+'('+trimmed_name+')'
        new_author.save()
            

        try:
            posts = requests.get(node.hostname + 'posts').json()
        except:
            try:
                posts = requests.get(node.hostname + 'posts/').json()
            except Exception:
                posts = {}
        while True:
            for post in posts.get('posts',[]):
                try:
                    author = Author.objects.get(uuid=post['author']['id'])
                except:
                    try:
                        author = Author(uuid=post['author']['id'],
                                        username=post['author']['displayName'],
                                        password='password',
                                        github=post['author']['github'],
                                        host=node)
                        author.save()
                    except IntegrityError:
                        author.username = author.username+'('+trimmed_name+')'
                    author.save()
                
                print("CONSOLE: post:", post)

                new_post = Post(uuid=post.get('id', 'NOUUIDFOUND'),
                     title=post.get('title', 'NOTITLEFOUND'),
                     source=post.get('source', node),
                     origin=post.get('source', node),
                     content=post.get('content', 'NOCONTENTFOUND')[:5000],
                     description=post.get('description', 'NODESCRIPTIONFOUND'),
                     contentType=post.get('contentType', 'text/plain'),
                     author=author,
                     categories='remote',
                     published=post.get('published', 'NOPUBLISHDATEFOUND'),
                     unlisted=post.get('unlisted', False),
                     visibility=post.get('visibility','PUBLIC'),
                     image=post.get('image', None),
                     link_to_image=post.get('link', '')
                     )

                if any(x in new_post.title for x in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico']):
                    new_post.image = new_post.title
                    new_post.link_to_image = post.get('content', 'NOCONTENTFOUND')
                    new_post.title = 'Image'
                    new_post.content = 'Content'
                elif re.findall('.*\[(.*?)\]\((.*)\)', new_post.content):
                    new_post.contentType='text/markdown'
                elif any(x in new_post.content for x in ['#', '*', '_']):
                    new_post.contentType='text/markdown'
                new_post.save()

                comments = post.get('comments',[])
                for comment in comments:
                     try:
                         author = Author.objects.get(uuid=comment['author']['id'])
                     except:
                         continue
                     Comment(uuid=comment.get('id', 'NOUUIDFOUND'),
                             comment=comment.get('comment', 'NOTITLEFOUND'),
                             published=comment.get('published', datetime.datetime.now()),
                             contentType=comment.get('contentType', 'text/plain'),
                             author=author,
                             post=post
                             ).save()
            try:
                posts = requests.get('{}posts?page={}'.format(node.hostname, int(posts['next']))).json()
            except:
                break
