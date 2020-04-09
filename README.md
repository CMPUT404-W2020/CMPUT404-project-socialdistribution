# CMPUT404-project-socialdistribution

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

# Contributors / Licensing

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Base Contributors (pre 2020):

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma

# Winter 2020 - Social Distribution Team - Squawk

Project base requirements, setup and licensing defined by the Contributors listed above

Django is LICENSED under the 3-clause BSD License https://github.com/django/django/blob/master/LICENSE

Django (Version 3.0.3) [Computer Software]. (2013). Retrieved from https://djangoproject.com.

Contributions:

    Austin Goebel
    Daniel Cones
    Jolene Poulin
    Natalie Hervieux
    Warren Thomas

## Acknowledgements:

    1. https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
    2. https://stackoverflow.com/questions/3003146/best-way-to-write-an-image-to-a-django-httpresponse
    3. Photo use: https://thenounproject.com/term/question/1101884/ Author: AliWijaya. This file is licensed under the 	Creative Commons Attribution-Share Alike 3.0 Unported license.
    4. All other photos are licensed under free use.
    5. https://stackoverflow.com/questions/29321494/show-input-field-only-if-a-specific-option-is-selected/29321711. Author: https://stackoverflow.com/users/4721273/josephus87
    6. https://www.w3schools.com/howto/howto_css_fixed_sidebar.asp
    7. https://stackoverflow.com/questions/15950007/centering-floated-images-in-div. author: https://stackoverflow.com/users/2157321/dhaval-marthak*/
    8. https://www.tjvantoll.com/2015/09/13/fetch-and-errors/

# Squawk Documentation

Squawk is a distributed social network that gives control back to the user. With Squawk, you get all the features you expect from a modern social network without sacrificing privacy or being flooded with promotional content. For every post you create, you decide exactly who can view it. When viewing content, you can access the Explore page to see all public posts connected to your node, or head to Your Feed to see only the curated content that you choose to follow.

## User Access

#### The website is hosted by Heroku at: https://cmput-404.herokuapp.com/

On first use, you will not be logged in but are granted access to the explore page. This allows users to explore public posts before deciding to sign up with Squawk. After signing in or making an account (click on the account button), you will be granted access to the full functionality.

For testing, we have created a number of sample user credentials:

| First   | Last     | Username        | Password |
| ------- | -------- | --------------- | -------- |
| James   | Smith    | JamesSmith      | cmput404 |
| John    | Johnson  | John Johnson    | cmput404 |
| Robert  | Williams | Robert Williams | cmput404 |
| Michael | Jones    | Michael Jones   | cmput404 |
| Ava     | Wilson   | Ava Wilson      | cmput404 |
| Olivia  | Lewis    | Olivia Lewis    | cmput404 |

## Site Features

Now that you're logged into your Squawk account, you can take advantage of all of the exciting features:

### Server to Server Connections

There is no more need to have accounts on countless social media sites; Squawk lets you pull information from different sources into one convenient feed. You can follow other authors within the Squawk server and all connecting servers. Refer to the "Current Connections" section in this document to see the servers available to you through Squawk or contact the Squawk admins to request a new server be added.

### Curate your Content

On **_Your Feed_** you see content from the authors that you follow. All of your posts, regardless of their privacy settings, will also be visible to you on your feed.

With our **_Github compatibility_**, see your github activity feed on your Squawk feed. Enable this option by adding your Github ID to your Squawk profile.

### Find New Content

Check out the **_Explore_** page to see all public posts from local and remote servers. This is a great way to find new authors to follow and to gain popularity through your public posts.

When you'd like to follow or unfollow an author, look them up on the **_Search_** page to change your current relationship.

You will be notified on the **_Notifications_** page when another author follows you. You can choose to follow them back and become friends, or dismiss the notification. Here you can also see a list of users you are following or are **_friends_** with.

### Own your Content

Choose how you display yourself to others by editing the information on your **_Account_** page.

Every post you create has several **_privacy_** options to choose from. If you set your post to **_public_**, then it will show on the explore page of all other users directly or indirectly connected to the Squawk server. Alternatively, you can restrict your post to the personal feeds of your **_friends_**, **_friends of friends_**, **_server only_**, or a spectific group of users with **_private_** posts. For added privacy, select **_unlisted_** and your post will only be visible to the aforementioned audience if you provide them with the direct link. If you change your mind later, you can easily edit your own posts and change their privacy setting.

All users have unlimited **_image storage_** hosted by our site. When creating a post, upload an image and it will automatically get a url on our site. Right click an image on your feed to copy the url. The image will have all of the privacy settings of the parent post. 


## Admin Access

Site administrators have the ability to verify or deny new user requests, edit and delete current users, and add and remove nodes. To verify or delete users, sign in to an admin account and go to https://cmput-404.herokuapp.com/verify. You can then click the plus or minus button to verify or delete users, respectively. 

To edit current users or connect with other nodes, you can access the admin page through https://cmput-404.herokuapp.com/admin.

For both pages, you can use the credentials:

    username: warren
    password: cmput404

## API Information:

API Endpoint URL:

https://cmput-404.herokuapp.com/

Credentials:

warren:cmput404

Example HTTPIE:

http GET https://cmput-404.herokuapp.com/posts

Web Service Endpoint URL:

https://cmput-404.herokuapp.com/

Current Connections:
| Remote API Endpoint | Username | Password |
| ---------------------------------------------------- | ---------- | -------------- |
| https://cmput404-socialdistribution.herokuapp.com/ | admindemo | ualberta01! |
| https://glacial-earth-37816.herokuapp.com/api/ | group8 | group8password |

### API Call Formats:

The format of requests are found in the example_requests folder (https://github.com/CMPUT404-W2020/CMPUT404-project-socialdistribution/tree/master/example_requests).

The system allows GET, PUT, POST, and DELETE requests; all other requests will be responded to with an HTTP 405 response
(will be updated to match social_distribution/sd/urls.py found on the api branch)

**/author/**

/author/

- GET
- Returns all users
- Example,
  [
  {
  "id": "192.168.0.143author/ac29def6-dde8-44f7-af24-781a36fb891f",
  "host": "192.168.0.143",
  "displayName": "admin",
  "github": "",
  "url": "192.168.0.143author/ac29def6-dde8-44f7-af24-781a36fb891f"
  },
  {
  "id": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "host": "192.168.0.143",
  "displayName": "1211pmUser",
  "github": "",
  "url": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174"
  },
  {
  "id": "192.168.0.143author/44df6b5a-7f11-4f87-8a35-16daa2a7eab4",
  "host": "192.168.0.143",
  "displayName": "1258pmUser",
  "github": "",
  "url": "192.168.0.143author/44df6b5a-7f11-4f87-8a35-16daa2a7eab4"
  }
  ]

/author/<uuid>

- GET
- Returns user details
- Example:
  {
  "id": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "host": "192.168.0.143",
  "displayName": "1211pmUser",
  "github": "",
  "url": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "bio": "",
  "firstName": "testing",
  "lastName": "testing2",
  "email": "test@test.com",
  "friends": [
  {
  "id": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "host": "192.168.0.143",
  "displayName": "1211pmUser",
  "github": "",
  "url": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "bio": "",
  "firstName": "testing",
  "lastName": "testing2",
  "email": "test@test.com"
  }
  ]
  }

/author/<uuid>/friends

- GET
- Returns all friends of user
- Example:
  [
  {
  "id": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "host": "192.168.0.143",
  "displayName": "1211pmUser",
  "github": "",
  "url": "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174"
  }
  ]

/author/<uuid:pk1>/friends/<uuid:pk2>

- GET
- returns bool to indicate whether or not two users are friends
  {
  "query": "friends",
  "authors": [
  "192.168.0.143author/8484179c-0b95-4a42-8a0f-216f1266b174",
  "192.168.0.143author/ac29def6-dde8-44f7-af24-781a36fb891f"
  ],
  "friends": 1
  }

/author/posts

- GET
- returns all posts visible to user
- uses Auth to determine what posts are visible
- Accepts pagination ie. /author/posts?page=4&size=50
- Example:
  {
  "query": "posts",
  "count": 1,
  "size": 50,
  "next": null,
  "previous": null,
  "posts": [
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/9496fd85-6b0d-4f6b-b359-3697d18d0c50",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "856pm",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/9496fd85-6b0d-4f6b-b359-3697d18d0c50",
  "bio": "",
  "firstName": "adsfadsf",
  "lastName": "fadfdaf",
  "email": "test@tes.com"
  },
  "title": "902pm",
  "description": "",
  "contentType": "1",
  "content": "",
  "categories": "",
  "comments": [
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/a40b2d9c-aaec-4703-a119-1f617ada86ad",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "admin",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/a40b2d9c-aaec-4703-a119-1f617ada86ad",
  "bio": "",
  "firstName": "",
  "lastName": "",
  "email": ""
  },
  "comment": "HELLOOOOOOO",
  "contentType": "1",
  "published": "2020-03-27T05:32:39.587831Z",
  "id": "73b72d79-ce8e-4b4e-b07a-ae7a78cb9971"
  }
  ],
  "published": "2020-03-27T03:02:54.830082Z",
  "id": "b174b292-2d32-47c5-bbe9-dd8fc92582a5",
  "visibility": "1",
  "visibleTo": [],
  "unlisted": "1"
  }
  ]
  }

**/posts/**

posts/<uuid>

- GET
- Requires Auth for posts with privacy restrictions
- Returns values for post specified by uuid
- Example:
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "207pm",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "bio": "",
  "firstName": "asdfasdf",
  "lastName": "sdafadfa",
  "email": "test@test.com"
  },
  "title": "asdfadf",
  "source": "https://cmput-404.herokuapp.com/",
  "origin": "https://cmput-404.herokuapp.com/",
  "description": "asdfasdf",
  "contentType": "text/markdown",
  "content": "asdfsa",
  "categories": "",
  "comments": [
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "admin",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "bio": "",
  "firstName": "",
  "lastName": "",
  "email": ""
  },
  "comment": "HELLOOOOOO",
  "contentType": "text/markdown",
  "published": "2020-03-27T20:19:55.496559Z",
  "id": "3a10eccb-0f2b-40e6-b45c-ea994670e0d0"
  }
  ],
  "published": "2020-03-27T20:08:11.468804Z",
  "id": "d2535b27-4ecf-49d0-baca-b24efd6931ce",
  "visibility": "PUBLIC",
  "visibleTo": [],
  "unlisted": false
  }

posts/<uuid>

- POST
- Returns values for post specified by uuid
- POST Example:
  {
  "query":"getPost",
  "postid":"d2535b27-4ecf-49d0-baca-b24efd6931ce",
  "url":"http://service/posts/d2535b27-4ecf-49d0-baca-b24efd6931ce",
  "author":{
  "id":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
  "host":"http://127.0.0.1:5454/",
  "displayName":"Jerry Johnson",
  "url":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
  "github": "http://github.com/jjohnson"
  },
  "friends":[
  "http://127.0.0.1:5454/author/7deee0684811f22b384ccb5991b2ca7e78abacde",
  "http://127.0.0.1:5454/author/11c3783f15f7ade03430303573098f0d4d20797b"
  ]
  }
- Return example:
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "207pm",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "bio": "",
  "firstName": "asdfasdf",
  "lastName": "sdafadfa",
  "email": "test@test.com"
  },
  "title": "asdfadf",
  "source": "https://cmput-404.herokuapp.com/",
  "origin": "https://cmput-404.herokuapp.com/",
  "description": "asdfasdf",
  "contentType": "text/markdown",
  "content": "asdfsa",
  "categories": "",
  "comments": [
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "admin",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "bio": "",
  "firstName": "",
  "lastName": "",
  "email": ""
  },
  "comment": "HELLOOOOOO",
  "contentType": "text/markdown",
  "published": "2020-03-27T20:19:55.496559Z",
  "id": "3a10eccb-0f2b-40e6-b45c-ea994670e0d0"
  },
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "admin",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "bio": "",
  "firstName": "",
  "lastName": "",
  "email": ""
  },
  "comment": "TEST COMMENT",
  "contentType": "text/markdown",
  "published": "2020-03-27T21:18:04.889486Z",
  "id": "2faf405a-63bc-4922-959d-84534f8b4bf6"
  }
  ],
  "published": "2020-03-27T20:08:11.468804Z",
  "id": "d2535b27-4ecf-49d0-baca-b24efd6931ce",
  "visibility": "PUBLIC",
  "visibleTo": [],
  "unlisted": false
  }

posts/<uuid>/comments

- GET
- returns comments from post with specified uuid
- example:
  {
  "query": "comments",
  "count": 1,
  "size": 50,
  "next": null,
  "previous": null,
  "comments": [
  {
  "author": {
  "id": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "host": "https://cmput-404.herokuapp.com/",
  "displayName": "admin",
  "github": "",
  "url": "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "bio": "",
  "firstName": "",
  "lastName": "",
  "email": ""
  },
  "comment": "HELLOOOOOO",
  "contentType": "text/markdown",
  "published": "2020-03-27T20:19:55.496559Z",
  "id": "3a10eccb-0f2b-40e6-b45c-ea994670e0d0"
  }
  ]
  }

posts/<uuid>/comments

- post
- creates comment on post specified with uuid
- Example POST:
  {
  "query" : "addComment",
  "post" : "https://cmput-404.herokuapp.com/928fe363-766d-4633-a35b-80ece3015c40",
  "comment" : {
  "author": {
  "id" : "https://cmput-404.herokuapp.com/2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "host" : "https://cmput-404.herokuapp.com/",
  "displayName" : "207pm",
  "url" : "https://cmput-404.herokuapp.com/2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "github" : ""
  },
  "comment" : "TEST COMMENT",
  "contentType" : "text/markdown",
  "published" : "2015-03-09T13:07:04+00:00",
  "id" : "928fe363-766d-4633-a35b-80ece3015c40"
  }
  }
- Example return:
  {
  "query": "addComment",
  "success": true,
  "message": "Comment Added"
  }

**/friends/**

/author/<uuid>/friends/<uuid>/

- GET
- Check if two authors are friends
- Example False:
  {
  "query": "friends",
  "authors": [
  "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "https://cmput-404.herokuapp.com/author/2a7b68b3-9d64-4365-8f4b-ae290fa31a28"
  ],
  "friends": false
  }
- Example True:
  {
  "query": "friends",
  "authors": [
  "https://cmput-404.herokuapp.com/author/7829b229-0f5a-4f0f-b312-bbb48dd7b8b9",
  "https://cmput-404.herokuapp.com/author/2a7b68b3-9d64-4365-8f4b-ae290fa31a28"
  ],
  "friends": true
  }
  author/<uuid>/friends
- POST
- Returns authors that are friends with specified author
- Example POST
  {
  "query":"friends",
  "author": <authorid>,
  "authors": [
  "2a7b68b3-9d64-4365-8f4b-ae290fa31a28",
  "65787662-c1e1-451d-a7b3-4386f0bdd9d0",
  "..."
  ]
  }
- Example response:
  {
  "query": "friends",
  "author": <authorid>,
  "authors": [
  "2a7b68b3-9d64-4365-8f4b-ae290fa31a28"
  ]
  }

## Web-Browser Page Paths:

### Post Interaction:

    /                    (displays the default explore page with all public and listed posts in servers connected to yours)
    /feed                (displays all posts created by the logged in user, and all posts by users that the logged in user follows, if they have permission to view those posts.
    /editpost/<post_id>  (allows the user to edit the specified post if it is their post)
    /newpost             (provides a form for the user to create a new post)

### Account Interaction

    /login               (provides a form for user to login to the system with existing credentials)
    /register            (provides a form for the user to register as an Author)
    /logout              (logs the currently authenticated user out)
    /account             (displays the currently authenticated user's information and allows them to edit that information)
    /edit_account        (allows the user to edit their profile information)

### User Interaction

    /search              (allows the user to search for other users. From the search results, they can follow/unfollow users and see their current relationship to them)
    /notifications       (displays the user's notification of requests and a list of other users that they follow or are friends with)
    /verify              (accessible only to superusers; allows the admin to verify/delete unverified users, or delete existing users)

## AJAX

### Fetch Paths:

    /verifyuser         (Sets verified to True for the user specificied in the body of the request which will allow that user to log in and use the site)
    /deleteuser         (deletes the user specificied in the body of the request)
    /rejectrequest      (sets the rejected value of a friendrequest  specificied in the body of the request to True so it doesn't show as a new/pending request)
    /friendrequest      (creates a follow object to the user specificied in the body of the request and sends them a friend request)
    /unfollow           (unfollows the user specificied in the body of the request)
    /deletepost         (deletes the post specificed in the body of the request)
    
## Testing

There is a script for running tests. The tests require selenium, which should be installed when you run `pip install -r requirements.txt` from the root directory of the project. Next, you need Firefox installed on your machine. Lastly, you need gecko installed on your machine, which can be done on a Mac by running `brew install gecko`. Then, ensure the test script is executable or run `chmod +x runtests.sh` to make it executable. Now, run `./runtests.sh` to run the tests! There are basic tests for the models and views as well as integration tests for all the major functionality. The tests should take approximately 4 minutes to run, so please be patient.

The following functions do not have automated tests as they all have alerts and Selenium has a known issue with dismissing alerts:
* Delete post
* Send friend request
* Unfriend another author
* Unfollow another author

It is possible that one of tests will fail on a unique key constraint. This is because we are testing the registration of a new user and this test communicates with our live server. To resolve this issue and have the test pass, login to [https://cmput-404.herokuapp.com/admin] with username "warren" and password "cmput404", navigate to the 'Users' tab, and delete the user with username 'Selenium'.

