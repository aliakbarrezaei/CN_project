from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
# Create your views here.


@csrf_exempt   
def home(request):
    videos=models.Video.objects.all().order_by('-pub_date')
    all_videos=[]
    for video in videos:
        if video.status=='I':
            continue
        all_videos+=[{'video ID':video.id,'Title':video.title,'publisher':video.user.user.username,'publication date':str(video.pub_date),'likes':video.likes.all().count(),'dislike':video.dislikes.all().count()}]
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
def adminsignup(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password, is_staff=True)
                user.save()
                admin=models.Admin(admin=user)
                admin.save()
                return HttpResponse(f'welcome {username}! you can login now.')
            except:
                return HttpResponse('error!!!')
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
def admin_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            check_user = authenticate(username= username, password= password)
            if check_user is not None:
                try:
                    admin=models.Admin.objects.get(admin=check_user)
                    if admin.status=='C':
                        login(request, check_user)
                        return HttpResponse(f'hi {username}!')
                    else:
                        return HttpResponse(f'hi {username}!,Your registration has not been confirmed')
                except:
                    return HttpResponse(f'invalid username.')
            else:
                return HttpResponse(f'invalid username.')
    return HttpResponse(f'you need to log out first')

@csrf_exempt
@login_required
def user_logout(request):
    logout(request)
    return HttpResponse(f'goodbye!')

@csrf_exempt        
def add_comment(request):
    try:  
        if request.method == 'POST':
            video_id = request.POST['video_id']
            comment = request.POST['comment']
            video_obj = models.Video.objects.get(id=video_id)
            user_obj = models.Users.objects.get(user__username=request.user)
            create_comment = models.Comment.objects.create(video=video_obj, user=user_obj,comment=comment)
            create_comment.save()
            return HttpResponse('your comment sent')
    except:
        return HttpResponse('error')

@csrf_exempt
def add_like(request):
    try:
        if request.method == 'POST':
            video_id = request.POST['video_id']
            user_obj = models.Users.objects.get(user__username=request.user)
            video_obj = models.Video.objects.get(id=video_id)
            if user_obj in video_obj.dislikes.all():
                video_obj.dislikes.remove(user_obj)
                video_obj.likes.add(user_obj)
                return HttpResponse('your like add')
            elif user_obj in video_obj.likes.all():
                video_obj.likes.remove(user_obj)
                return HttpResponse('your like remove')
            else:
                video_obj.likes.add(user_obj)
                return HttpResponse('your like add')
    except:
        return HttpResponse('error')
            
@csrf_exempt
def add_dislike(request):
    try:
        if request.method == 'POST':
            video_id = request.POST['video_id']
            user_obj = models.Users.objects.get(user__username=request.user)
            video_obj = models.Video.objects.get(id=video_id)
            if user_obj in video_obj.likes.all():
                video_obj.likes.remove(user_obj)
                video_obj.dislikes.add(user_obj)
                return HttpResponse('your dislike add')
            elif user_obj in video_obj.dislikes.all():
                video_obj.likes.remove(user_obj)
                return HttpResponse('your dislike remove')
            else:
                video_obj.dislikes.add(user_obj)
                return HttpResponse('your dislike add')
    except:
        return HttpResponse('error')

@csrf_exempt
def add_label(request):
    try:
        if request.method == 'POST':
            video_id = request.POST['video_id']
            admin_obj = models.Admin.objects.get(admin__username=request.user)
            video_obj = models.Video.objects.get(id=video_id)
            if video_obj.label=='U':
                video_obj.label='L'
                video_obj.save()
                return HttpResponse('label add')
            else:
                video_obj.label='U'
                video_obj.save()
                return HttpResponse('label remove')
    except:
        return HttpResponse('error')

@csrf_exempt
def video_status(request):
    try:
        if request.method == 'POST':
            video_id = request.POST['video_id']
            admin_obj = models.Admin.objects.get(admin__username=request.user)
            video_obj = models.Video.objects.get(id=video_id)
            if video_obj.status=='A':
                video_obj.status='I'
                video_obj.save()
                user_object=video_obj.user
                if user_object.status=='N':
                    user_object.unavailable_videos_count+=1
                    user_object.save()
                    if user_object.unavailable_videos_count==2:
                        user_object.status='S'
                        user_object.save()
                        return HttpResponse('The video became unavailable,and user has been striked')
                return HttpResponse('The video became unavailable')
            else:
                return HttpResponse('The video was unavailable')
    except:
        return HttpResponse('error')


@csrf_exempt
def watch_video(request,video_id):
    try:
        video_obj=models.Video.objects.get(id=video_id)
    except:
        return HttpResponse('There is no video')
    try:
        user_obj=models.Users.objects.get(user__username=request.user)
    except:
        try:
            admin_obj=models.Admin.objects.get(admin__username=request.user)
        except:
            return HttpResponse('You are not login to watch this video.')
    video_comments= models.Comment.objects.filter(video=video_obj).order_by('-id')
    video_likes=video_obj.likes.all().count()
    video_dislikes=video_obj.dislikes.all().count()

@csrf_exempt
def strike_resolving(request,username):
    try:
        admin_obj = models.Admin.objects.get(admin__username=request.user)
        user_obj=models.Users.objects.get(user__username=username)
        if user_obj.status=='S':
            user_obj.status='N'
            user_obj.save()
            return HttpResponse('The user removed from the strike mode')
        else:
            return HttpResponse('The user was not strike')
    except:
        return HttpResponse('error')

      



