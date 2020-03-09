from django.test import TestCase
from sd.models import Post, Author, Comment, FriendRequest, Follow, FriendList
from django.utils import timezone

class ModelTests(TestCase):
    def create_author(self, first_name="Test", last_name="Author", bio="I am a test author"):
        return Author(
            first_name = "Test",
            last_name = "Author",
            bio = "I am a test author"
        )
        
    def create_post(self, author=None, title="test post", body="this is a test", status="public", link_to_image=""):
        a = author if author != None else self.create_author()

        return Post(
            author = a,
            title = title,
            body = body,
            date = timezone.now(),
            status = status,
            link_to_image = link_to_image
        )

    def create_comment(self, author, post, body="comment"):
        return Comment(
            author = author,
            body = body,
            date = timezone.now(),
            post = post
        )

    def create_friend_request(self, to, fr):
        return FriendRequest(
            to_author = to,
            from_author = fr,
            date = timezone.now()
        )

    def create_follow(self, following, follower):
        return Follow(
            following = following,
            follower = follower,
            date = timezone.now()
        )

    def create_friend_list(self, current):
        return FriendList(
            current_author = current
        )

    def test_author(self):
        a = self.create_author()
        self.assertTrue(isinstance(a, Author))

        self.assertEqual(a.first_name, "Test")
        self.assertEqual(a.last_name, "Author")
        self.assertEqual(a.bio, "I am a test author")

    def test_post(self):
        p = self.create_post()
        self.assertTrue(isinstance(p, Post))
        self.assertTrue(isinstance(p.author, Author))

        self.assertEqual(p.title, "test post")
        self.assertEqual(p.body, "this is a test")
        self.assertEqual(p.status, "public")
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

        self.assertEqual(c.body, "comment")

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

    def test_friend_list(self):
        a1 = self.create_author(first_name="Current", last_name="Auth")
        a2 = self.create_author(first_name="Friend", last_name="Auth")

        fl = self.create_friend_list(a1)

        fl.author_friends.set([a2])

        self.assertTrue(isinstance(fl, FriendList))
        self.assertEqual(a1, fl.current_author)
        self.assertEqual(a2, fl.author_friends)



class BasicActions(TestCase):

    def setUp(self):
        pass

    def test_edit_post(self):
        pass

    def test_delete_post(self):
        pass

    def test_edit_not_my_post(self):
        pass

    def test_delete_not_my_post(self):
        pass

    def test_create_plaintext_post(self):
        pass

    def test_create_markdown_post(self):
        pass

    def test_cant_comment_on_post(self):
        pass

    def test_post_with_image(self):
        pass

    def test_access_image_no_auth(self):
        pass

    def test_view_public_posts(self):
        pass

class FriendsTestCases(TestCase):
    def setUp(self):
        pass

    def test_render_friend_post(self):
        pass

    def test_send_friend_request(self):
        pass

    def test_receive_friend_request(self):
        pass

    def test_post_from_not_friend(self):
        pass

    def test_create_unlisted_post(self):
        pass

    def test_create_private_post(self):
        pass

    def test_create_private_to_friends_post(self):
        pass

    def test_creat_foaf_post(self):
        # post is only visible to friend of a friend
        pass

    def test_create_public_post(self):
        pass

    def test_unfriend_local(self):
        pass

    def test_unfriend_remote(self):
        pass

class ServerTests(TestCase):
    def setUp(self):
        pass

    def test_host_images(self):
        pass

    def test_add_author(self):
        pass

    def test_modify_author(self):
        pass

    def test_remove_author(self):
        pass

    def test_allow_new_user(self):
        pass

    def test_setup_not_approved(self):
        # As a user who signed up but hasn't been approved by the server,
        # I shouldn't be able to do anything
        pass

    def test_add_remote_server_with_auth(self):
        pass

    def test_add_remote_server_no_auth(self):
        # This shouldn't work
        pass
    
    def test_disable_remote_server_conn(self):
        pass

    def test_share_posts_across_server(self):
        pass

    def test_no_share_posts_across_server(self):
        pass
