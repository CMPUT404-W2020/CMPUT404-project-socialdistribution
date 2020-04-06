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
        fields = ('title', 'description', 'content', 'image', 'link_to_image', 'author', 'contentType', 'categories','visibility', 'visibleTo', 'unlisted',)
        widgets = {
            'contentType': forms.Select(choices=WEB_CONTENT_CHOICES),
            'visibility': forms.Select(),
            'author': forms.HiddenInput(),
            'content': forms.Textarea()
        }
        labels = {
            "title" : "*Post Title:",
            "image" : "Upload Image:",
            "link_to_image" : "Image link (will be overwritten if an image file is uploaded)",
            "visibility" : "*Privacy Setting:",
            "visibleTo" : "Who can see your private post?",
            "unlisted" : "*Allow your post to be listed in other's feeds?",
            "contentType" : "* Content Type:"
        }

class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'author', 'contentType', 'categories','visibility', 'visibleTo', 'unlisted',)
        widgets = {
            'contentType': forms.Select(choices=WEB_CONTENT_CHOICES),
            'visibility': forms.Select(),
            'author': forms.HiddenInput(),
            'content': forms.Textarea()
        }
        labels = {
            "title" : "*Post Title:",
            "visibility" : "*Privacy Setting:",
            "visibleTo" : "Who can see your private post?",
            "unlisted" : "*Allow your post to be listed in other's feeds?",
            "contentType" : "* Content Type:"
        }

