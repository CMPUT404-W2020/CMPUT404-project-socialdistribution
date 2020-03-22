CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

Contributors / Licensing
========================

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

Winter 2020 - Social Distribution Team - Squawk
========================

Project base requirements, setup and licensing defined by the Contributors listed above

Django is LICENSES'D under the 3-clause BSD License https://github.com/django/django/blob/master/LICENSE 

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

Squawk is a distributed social network that gives control back to the user. With Squawk, you get all the features you expect from a modern social network without sacrificing privacy or being flooded with promotional content. For every post you create, you can choose exactly who can view it. When viewing content, you can access the Explore page to see all public posts connected to your node, or head to Your Feed to see only the currated content that you choose to follow. 

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
|---------|----------|-----------------|----------|
| James   | Smith    | JamesSmith      | cmput404 |
| John    | Johnson  | John Johnson    | cmput404 |
| Robert  | Williams | Robert Williams | cmput404 |
| Michael | Jones    | Michael Jones   | cmput404 |
| Ava     | Wilson   | Ava Wilson      | cmput404 |
| Olivia  | Lewis    | Olivia Lewis    | cmput404 |

## Admin Access

**TODO**: add superuser information for heroku. *not sure if django superuser is the same. Can we provide them with superuser login in that will work for them?

When running locally, you can run this command to create a superuser and access the admin interface:
	
	python3 manage.py createsuperuser


## API Call Formats:

The format of requests are found in the example_requests folder (https://github.com/CMPUT404-W2020/CMPUT404-project-socialdistribution/tree/master/example_requests). 

**TODO**: update this 

The system only allows GET and POST requests; all other requests will be responded to with an HTTP 405 response
(will be updated to match social_distribution/sd/urls.py found on the api branch)

    
    auth/register               (POST)
    auth/logout                 (GET)
    auth/getuser                (GET)
    auth/edituser/<uuid>        (POST)
    auth/getpost                (GET)
    auth/deletepost             (GET)
    auth/getallpost             (GET)
    posts/<uuid>                (GET)
    posts/<uuid>/comments       (GET)
    author/<uuid>/post          (POST)
    author/<uuid>/posts         (GET)
    author/posts                (GET)
    posts/<uuid>/comment        (POST)

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

   
