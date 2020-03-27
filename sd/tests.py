from django.test import SimpleTestCase
from django.urls import resolve
from unittest import skip

from sd.models import *
from sd.views import *
import social_distribution.settings as settings


class ModelTests(SimpleTestCase):
    def create_node(self):
        return Node()

    def create_author(self, first_name="Test", last_name="Author", bio="I am a test author"):
        return Author(
            host = self.create_node(),
            first_name = first_name,
            last_name = last_name,
            bio = "I am a test author"
        )

    def create_post(self, author=None, title="test post", content="this is a test", visibility='PUBLIC', link_to_image=""):
        a = author if author != None else self.create_author()

        return Post(
            contentType = 'text/plain',
            author = a,
            title = title,
            content = content,
            visibility = visibility,
            link_to_image = link_to_image,
            unlisted = False,
            host = self.create_node()
        )

    def create_comment(self, author, post, comment="comment"):
        return Comment(
            author = author,
            comment = comment,
            contentType = 'text/plain',
            post = post
        )

    def create_friend_request(self, to, fr):
        return FriendRequest(
            to_author = to,
            from_author = fr
        )

    def create_follow(self, following, follower):
        return Follow(
            following = following,
            follower = follower
        )

    def create_friend(self, current, friend):
        return Friend(
            author = current,
            friend = friend
        )

    def test_node(self):
        self.n = self.create_node()
        self.assertTrue(isinstance(self.n, Node))

        self.assertEqual(self.n.hostname, settings.HOSTNAME)

    def test_author(self):
        a = self.create_author()
        self.assertTrue(isinstance(a, Author))

        self.assertEqual(a.host.hostname, settings.HOSTNAME)
        self.assertEqual(a.first_name, "Test")
        self.assertEqual(a.last_name, "Author")
        self.assertEqual(a.bio, "I am a test author")

    def test_post(self):
        p = self.create_post()
        self.assertTrue(isinstance(p, Post))
        self.assertTrue(isinstance(p.author, Author))

        self.assertEqual(p.title, "test post")
        self.assertEqual(p.content, "this is a test")
        self.assertEqual(p.visibility, 'PUBLIC')
        self.assertEqual(p.link_to_image, "")

        self.assertEqual(p.author.first_name, "Test")
        self.assertEqual(p.author.last_name, "Author")
        self.assertEqual(p.author.bio, "I am a test author")

    def test_comment(self):
        a = self.create_author(first_name="Justan", last_name="Author")
        a2 = self.create_author(first_name="Makea", last_name="Post")
        p = self.create_post(author=a2)

        c = self.create_comment(a, p)

        self.assertTrue(isinstance(c, Comment))
        self.assertEqual(c.author, a)
        self.assertEqual(c.post, p)

        self.assertEqual(c.comment, "comment")

    def test_friend_request(self):
        a1 = self.create_author(first_name="To", last_name="Me")
        a2 = self.create_author(first_name="From", last_name="Me")

        fr = self.create_friend_request(a1, a2)

        self.assertTrue(isinstance(fr, FriendRequest))
        self.assertEqual(a1, fr.to_author)
        self.assertEqual(a2, fr.from_author)

    def test_follow(self):
        a1 = self.create_author(first_name="Follow", last_name="Ing")
        a2 = self.create_author(first_name="Follow", last_name="Er")

        f = self.create_follow(a1, a2)

        self.assertTrue(isinstance(f, Follow))
        self.assertEqual(a1, f.following)
        self.assertEqual(a2, f.follower)

    def test_friend(self):
        a1 = self.create_author(first_name="Current", last_name="Auth")
        a2 = self.create_author(first_name="Friend", last_name="Auth")

        fr = self.create_friend(a1, a2)

        self.assertTrue(isinstance(fr, Friend))
        self.assertEqual(a1, fr.author)
        self.assertEqual(a2, fr.friend)

class URLTests(SimpleTestCase):
    def test_get_login(self):
        r = resolve('')
        self.assertEqual(r.func, explore)

    def test_get_login(self):
        r = resolve('/login')
        self.assertEqual(r.func, login)

    def test_get_login(self):
        r = resolve('/logout/')
        self.assertEqual(r.func, logout)

    def test_get_register(self):
        r = resolve('/register/')
        self.assertEqual(r.func, register)

    def test_get_newpost(self):
        r = resolve('/newpost')
        self.assertEqual(r.func, new_post)

    def test_get_feed(self):
        r = resolve('/feed')
        self.assertEqual(r.func, feed)

    def test_get_notifications(self):
        r = resolve('/notifications')
        self.assertEqual(r.func, notifications)

    def test_get_friendrequest(self):
        r = resolve('/friendrequest')
        self.assertEqual(r.func, friendrequest)

    def test_get_media(self):
        r = resolve('/media/1')
        self.assertEqual(r.func, get_image)

    def test_get_search(self):
        r = resolve('/search')
        self.assertEqual(r.func, search)

    def test_get_account(self):
        r = resolve('/account')
        self.assertEqual(r.func, account)

    def test_get_edit_account(self):
        r = resolve('/edit_account')
        self.assertEqual(r.func, edit_account)
