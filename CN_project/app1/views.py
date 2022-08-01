from django.shortcuts import render
#####
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import Video, Comment, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        #demo_videos = VideoPost.objects.all().order_by('-id')
        return render(request, 'app1/sinup.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST['uname']
        pwd = request.POST['pwd']
        new_user = User.objects.create(username,pwd)
        new_user.username = username
        new_user.save()
        messages.success(request, 'Account has been created successfully.')