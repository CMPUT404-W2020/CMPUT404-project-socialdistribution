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



class LoginForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['username', 'password']


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'contentType', 'description', 'categories', 'image', 'link_to_image', 'author', 'visibility', 'visibleTo', 'unlisted',)
        widgets = {
            'contentType': forms.Select(choices=WEB_CONTENT_CHOICES),
            'visibility': forms.Select(),
            'author': forms.HiddenInput(),
            'content': forms.Textarea(),
            'title': forms.Textarea(),
            'description': forms.Textarea(),
            'link_to_image': forms.Textarea(),
            'categories': forms.Textarea(),
            'visibleTo': forms.Textarea()
        }
        labels = {
            "title" : "* Title:",
            "image" : "Upload Image:",
            "link_to_image" : "Image link (will be ignored if an image file is uploaded)",
            "visibility" : "* Privacy:",
            "visibleTo" : "Who can see your private post?",
            "unlisted" : "* Allow your post to be listed in other's feeds?",
            "contentType" : "* Content Type:"
        }

class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'contentType', 'description', 'categories', 'author', 'visibility', 'visibleTo', 'unlisted',)
        widgets = {
            'contentType': forms.Select(choices=WEB_CONTENT_CHOICES),
            'visibility': forms.Select(),
            'author': forms.HiddenInput(),
            'content': forms.Textarea(),
            'title': forms.Textarea(),
            'description': forms.Textarea(),
            'categories': forms.Textarea(),
            'visibleTo': forms.Textarea()
        }
        labels = {
            "title" : "* Title:",
            "visibility" : "* Privacy:",
            "visibleTo" : "Who can see your private post?",
            "unlisted" : "* Allow your post to be listed in other's feeds?",
            "contentType" : "* Content Type:"
        }

