from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

# https://stackoverflow.com/questions/13202845/removing-help-text-from-django-usercreateform

# class RegistrationForm(UserCreationForm):

WEB_CONTENT_CHOICES= [
    ('text/plain', 'Plaintext'),
    ('text/markdown', 'Markdown')
]


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'bio', 'github']
        widgets = {
            'password': forms.PasswordInput(),
        }

class EditAccountForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'github']
        widgets = {
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'last_name': forms.TextInput(attrs={'required':'true'}),
            'username': forms.TextInput(attrs={'required':'true'}),
            'email': forms.TextInput(attrs={'placeholder': 'e.g. coolbear@uberta.ca'}),
            'bio': forms.Textarea(),
            'github': forms.TextInput(attrs={'placeholder': 'Github account name e.g. wlt91'})
        }
        labels = {
            "first_name" : "* First Name:",
            "last_name" : "* Last Name:",
            "username" : "* Username:",
            "email" : "Email:",
            "bio" : "Bio:",
            "github" : "Github:"
        }



class LoginForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['username', 'password']


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'contentType', 'description', 'categories', 'image', 'link_to_image', 'author', 'visibility', 'visibleTo', 'unlisted',)
        widgets = {
            'contentType': forms.Select(choices=WEB_CONTENT_CHOICES, attrs={'required':'true'}),
            'visibility': forms.Select(attrs={'required':'true'}),
            'author': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'required':'true'}),
            'title': forms.Textarea(attrs={'required':'true'}),
            'description': forms.Textarea(),
            'link_to_image': forms.Textarea(attrs={'placeholder':'https://example-photo=link.png'}),
            'categories': forms.Textarea(attrs={'placeholder': 'comma-separated tags'}),
            'visibleTo': forms.Textarea(attrs={'placeholder': 'comma-separated usernames'})
        }
        labels = {
            "title" : "* Title:",
            "image" : "Upload Image:",
            "link_to_image" : "Image link (will be ignored if an image file is uploaded)",
            "visibility" : "* Privacy:",
            "visibleTo" : "Who can see your private post?",
            "unlisted" : "* Allow your post to be listed in other's feeds?",
            "contentType" : "* Content Type:",
            "content": "* Content:"
        }

class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'contentType', 'description', 'categories', 'author', 'visibility', 'visibleTo', 'unlisted',)
        widgets = {
            'contentType': forms.Select(choices=WEB_CONTENT_CHOICES, attrs={'required':'true'}),
            'visibility': forms.Select(attrs={'required':'true'}),
            'author': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'required':'true'}),
            'title': forms.Textarea(attrs={'required':'true'}),
            'description': forms.Textarea(),
            'categories': forms.Textarea(attrs={'placeholder': 'comma-separated tags'}),
            'visibleTo': forms.Textarea(attrs={'placeholder': 'comma-separated usernames'})
        }
        labels = {
            "title" : "* Title:",
            "visibility" : "* Privacy:",
            "visibleTo" : "Who can see your private post?",
            "unlisted" : "* Allow your post to be listed in other's feeds?",
            "contentType" : "* Content Type:",
            "content": "* Content:"
        }

