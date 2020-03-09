from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
import os

def index(request):
	return redirect('explore', permanent=True)

def login(request):
	page = 'sd/login.html'
	return render(request, page)

def create_account(request):
	page = 'sd/create_account.html'
	return render(request, page)

def new_post(request):
	page = 'sd/new_post.html'
	return render(request, page)

def requests(request):
	return HttpResponse("Friend Requests Page")

def feed(request):
	return HttpResponse("Your Feed")

def explore(request):
	feed = Post.objects.all()
	page = 'sd/index.html'
	return render(request, page, {'feed':feed})

def author(request, author_id):
	author = Author.objects.get(uuid=author_id)
	return HttpResponse(author.username+"'s Page")

def post(request, post_id):
	post = Post.objects.get(uuid=post_id)
	return HttpResponse(post)

def post_comment(request, post_id):
	post = Comment.objects.get(post=post_id)
	return HttpResponse(post)

# def search(request):
# 	return HttpResponse("User Search Page")

# def friends(request):
# 	return HttpResponse("Friends Page")

def account(request):
	page = 'sd/my_account.html'
	return render(request, page)