from django.test import SimpleTestCase
from django.urls import resolve
from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from sd.models import *
from sd.views import *
import social_distribution.settings as settings
import time


class ModelTests(SimpleTestCase):
    # Simple tests for all the django models
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
    # simple tests for all the views
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

class IntegratedTests(StaticLiveServerTestCase):
    def setUp(self):
        # start selenium webdriver
        self.driver = webdriver.Firefox()
        self.live_server_url = "https://cmput-404.herokuapp.com/"

    def tearDown(self):
        # stop selenium webdriver
        self.driver.close()

    def test_login_success(self):
        # test successful login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

    def test_login_failure_bad_pass(self):
        # test unsuccessful login, wrong password
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "login"

    def test_login_failure_no_user(self):
        # test unsuccessful login, wrong password
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("BadUserName")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("nopass")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "login"

    def test_side_bar_post_auth(self):
        # test locate sidebar and press all the buttons

        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        # ensure the page is loaded before continuing
        time.sleep(2)

        # Look for sidebar
        sidebar_post = driver.find_element_by_class_name("sidebarpost")
        assert "POST" in sidebar_post.get_attribute('innerHTML')

        nav = driver.find_element_by_class_name("sidebarfeed")
        assert "EXPLORE" in nav.get_attribute('innerHTML')
        assert "MY FEED" in nav.get_attribute('innerHTML')

        # test clicks on sidebar
        driver.find_element_by_class_name("plusicon").click()
        assert driver.current_url == self.live_server_url + "newpost"

    def test_side_bar_explore_auth(self):
        # test locat sidebar and press all the buttons

        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        # ensure the page is loaded before continuing
        time.sleep(2)

        # Look for sidebar
        sidebar_post = driver.find_element_by_class_name("sidebarpost")
        assert "POST" in sidebar_post.get_attribute('innerHTML')

        nav = driver.find_element_by_class_name("sidebarfeed")
        assert "EXPLORE" in nav.get_attribute('innerHTML')
        assert "MY FEED" in nav.get_attribute('innerHTML')

        # click explore button
        explore = driver.find_element_by_class_name("compassicon")
        explore.click()
        assert driver.current_url == self.live_server_url

    def test_side_bar_feed_auth(self):
        # test locat sidebar and press all the buttons

        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        # ensure the page is loaded before continuing
        time.sleep(2)

        # Look for sidebar
        sidebar_post = driver.find_element_by_class_name("sidebarpost")
        assert "POST" in sidebar_post.get_attribute('innerHTML')

        nav = driver.find_element_by_class_name("sidebarfeed")
        assert "EXPLORE" in nav.get_attribute('innerHTML')
        assert "MY FEED" in nav.get_attribute('innerHTML')

        # click feed button
        feed = driver.find_element_by_class_name("yourfeed")
        feed.click()
        assert driver.current_url == self.live_server_url + "feed"
        
    def test_header(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # check for all icons
        icons = driver.find_elements_by_class_name("icons")
        assert len(icons) == 3

    def test_create_post_auth(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        # ensure the page is loaded before continuing
        time.sleep(2)

        # Look for sidebar
        sidebar_post = driver.find_element_by_class_name("sidebarpost")
        assert "POST" in sidebar_post.get_attribute('innerHTML')

        nav = driver.find_element_by_class_name("sidebarfeed")
        assert "EXPLORE" in nav.get_attribute('innerHTML')
        assert "MY FEED" in nav.get_attribute('innerHTML')

        # go to new post page
        driver.find_element_by_class_name("plusicon").click()
        assert driver.current_url == self.live_server_url + "newpost"
        time.sleep(2)

        # enter all the info for the new post
        title = driver.find_element_by_id("id_title")
        title.send_keys("This is the post title")
        
        content = driver.find_element_by_id("id_content")
        content.send_keys("This is the content of my post! It was made by Selenium, isn't that neat?")

        content_type = Select(driver.find_element_by_id("id_contentType"))
        content_type.select_by_visible_text("text/plain")

        privacy = Select(driver.find_element_by_id("id_visibility"))
        privacy.select_by_visible_text("Public")

        unlisted = Select(driver.find_element_by_id("id_unlisted"))
        unlisted.select_by_visible_text("LISTED")

        # submit a new post
        submit = driver.find_element_by_id("bluebackground-button")
        submit.click()
        time.sleep(2)

        assert driver.current_url == self.live_server_url + "feed"

    def test_edit_post_auth(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # find the options button on a post
        opts = driver.find_element_by_class_name("dropdown-button")
        opts.click()

        edit_btn = driver.find_element_by_link_text("Edit")
        edit_btn.click()
        assert self.live_server_url + "edit" in driver.current_url

    def test_notifications_auth(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find notifications button
        notis = driver.find_element_by_xpath('//img[@alt="Network"]')
        notis.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "notifications"

    def test_notifications_no_auth(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(2)
        
        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find notifications button
        notis = driver.find_element_by_xpath('//img[@alt="Network"]')
        notis.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "login"

    def test_account_auth(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find account button
        account = driver.find_element_by_xpath('//img[@alt="Account"]')
        account.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "account"

    def test_account_no_auth(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find account button
        account = driver.find_element_by_xpath('//img[@alt="Account"]')
        account.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "login"

    def test_search_auth(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find search button
        search = driver.find_element_by_xpath('//img[@alt="Search"]')
        search.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "search"

        # submit empty search, turns up all authors in db
        search_bar = driver.find_element_by_id("search-val")
        search_bar.click()
        search_bar.send_keys(Keys.RETURN)
        time.sleep(1)

        # make sure there's at least 1 result
        results = driver.find_elements_by_class_name("searchauthor")
        assert len(results) > 0

    def test_search_no_auth(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(2)
        
        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find search button
        search = driver.find_element_by_xpath('//img[@alt="Search"]')
        search.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "login"

    @skip("Dealing with alerts is tricky; this test hangs")
    def test_send_friend_request(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find notifications button
        search = driver.find_element_by_xpath('//img[@alt="Search"]')
        search.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "search"

        # submit empty search, turns up all authors in db
        search_bar = driver.find_element_by_id("search-val")
        search_bar.click()
        search_bar.send_keys(Keys.RETURN)
        time.sleep(1)

        # make sure there's at least 1 result
        results = driver.find_elements_by_class_name("searchauthor")
        assert len(results) > 0

        add_btn = driver.find_element_by_id("circle-button-John-Johnson")
        add_btn.click()

        alert_obj = driver.switch_to.alert
        assert "John Johnson" in alert_obj.text()
        time.sleep(2)

        alert_obj.accept()

    def test_logout(self):
        # Login
        driver = self.driver
        driver.get(self.live_server_url + "login")
        u_name = driver.find_element_by_name("username")
        u_name.send_keys("JamesSmith")
        p_word = driver.find_element_by_name("password")
        p_word.send_keys("cmput404")
        login_btn = driver.find_element_by_id("login-button")
        login_btn.click()
        assert driver.current_url == self.live_server_url + "feed"

        time.sleep(2)

        # Look for header
        header = driver.find_element_by_id("header")
        assert "SQUAWK" in header.get_attribute('innerHTML')

        # find notifications button
        account = driver.find_element_by_xpath('//img[@alt="Account"]')
        account.click()
        time.sleep(2)
        assert driver.current_url == self.live_server_url + "account"

        logout_btn = driver.find_element_by_xpath("//input[@value='LOGOUT']")
        logout_btn.click()
        assert driver.current_url == self.live_server_url + "login"