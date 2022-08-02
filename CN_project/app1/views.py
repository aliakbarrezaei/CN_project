from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
# Create your views here.



def home(request):
    videos=models.Video.objects.all().order_by('-pub_date')
    all_videos=[]
    for video in videos:
        all_videos+=[(video.id,video.title)]
    return HttpResponse(all_videos)
@csrf_exempt
def upload_video(request):
    try:
        if request.method == 'POST':
            title = request.POST['title']
            video_file = request.FILES['video_file']
            user_obj = models.Users.objects.get(user__username=request.user)
            if user_obj.status=='N':
                upload_video =models.Video(user=user_obj,title=title, video_file=video_file)
                upload_video.save()
                return HttpResponse('The video has been uploaded.')
            else:
                return HttpResponse('you are striked!!')

    except:
        return HttpResponse('error')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user=models.Users(user=user)
                user.save()
                return HttpResponse(f'welcome {username}! you can login now.')
            except:
                return HttpResponse('error!!')
        return HttpResponse(f'you need to log out first')
    return HttpResponse('error!!')

@csrf_exempt
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            check_user = authenticate(username= username, password= password)
            if check_user is not None:
                try:
                    user=models.Users.objects.get(user=check_user)
                    if user.status=='N':
                        login(request, check_user)
                        return HttpResponse(f'hi {username}!')
                    else:
                        login(request, check_user)
                        return HttpResponse(f'hi {username}!, you are striked.so you cant upload')
                except:
                    return HttpResponse(f'invalid username.')
            else:
                return HttpResponse(f'invalid username.')
    return HttpResponse(f'you need to log out first')

@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponse(f'goodbye!')
        

        


