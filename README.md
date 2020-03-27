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

# Squawk Documentation

Squawk is a distributed social network that gives control back to the user. With Squawk, you get all the features you expect from a modern social network without sacrificing privacy or being flooded with promotional content. For every post you create, you can choose exactly who can view it. When viewing content, you can access the Explore page to see all public posts connected to your node, or head to Your Feed to see only the curated content that you choose to follow.

## User Access

The website is hosted by Heroku at https://cmput-404.herokuapp.com/

Alternatively, one can run the app locally by running the following command from the root directory:
virtualenv venv --python=python3
source venv/bin/activate
pip3 install -r requirements.txt
python3 social_distribution/manage.py runserver

If you make local changes that result in database errors, try:
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py migrate

Once the app is running, use your web browser to access: http://127.0.0.1:8000/

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

## Admin Access

**TODO**: add superuser information for heroku. \*not sure if django superuser is the same. Can we provide them with superuser login in that will work for them?

When running locally, you can run this command to create a superuser and access the admin interface:
python3 manage.py createsuperuser

## API Call Formats:

The format of requests are found in the example_requests folder (https://github.com/CMPUT404-W2020/CMPUT404-project-socialdistribution/tree/master/example_requests).

**TODO**: update this

The system allows GET, PUT, POST, and DELETE requests; all other requests will be responded to with an HTTP 405 response
(will be updated to match social_distribution/sd/urls.py found on the api branch)

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

posts/<uuid>

- GET
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

## Web-Browser Page Paths:

**(will be updated to match social_distribution/sd/urls.py found on the api branch)**

    /                    (displays the default explore page with all public posts in servers connected to yours)
    /feed                (displays all posts created by the logged in user, and all posts by users that the logged in user follows, if they have permission to view those posts.
    /login               (provides a form for the user to login to the system)
    /logout              (logs the currently authenticated user out)
    /search              (allows the user to search for other users. From the search results, they can follow/unfollow users and see their current relationship to them)
    /account             (displays the currently authenticated user's information and allows them to edit that information)
    /editpost/<post_id>  (allows the user to edit the specified post if it is their post)
    /newpost             (provides a form for the user to create a new post)
    /register            (provides a form for the user to register as an Author)
    /notifications       (displays a concept UI for the user's notification of requests)

## Testing

**TODO**: Update to explain the tests briefly, where they can be found and how to run them.
