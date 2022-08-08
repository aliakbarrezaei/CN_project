import os, mimetypes
from wsgiref.util import FileWrapper
from django.http import HttpResponse, JsonResponse
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models
from .client import Client


@csrf_exempt
def home(request):
    videos = models.Video.objects.all().order_by('-pub_date')
    all_videos = []
    for video in videos:
        if video.status == 'I':
            continue
        all_videos += [{'video ID': video.id, 'Title': video.title, 'publisher': video.user.user.username,
                        'publish date': str(video.pub_date), 'likes': video.likes.all().count(),
                        'dislike': video.dislikes.all().count()}]
    return JsonResponse({'videos': all_videos})


@csrf_exempt
@login_required
def profile(request):
    user = request.user
    username = user.username
    is_staff = user.is_staff
    proxy_msg = ''
    if request.user.is_staff and not request.user.is_superuser:
        if not connected_to_proxy(request):
            proxy_msg = 'you are not connected to proxy. if you dont have proxy information, send a ticket to manager.'

    resp = f'username = {username}  <br>\nis_staff = {is_staff}   <br>\n{proxy_msg}'
    return HttpResponse(resp)


# ------------------------------------------  management -------------------------------------
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user = models.Users(user=user)
                user.save()
                return HttpResponse(f'welcome {username}! you can login now.')
            except:
                return HttpResponse('error!!')
        return HttpResponse(f'you need to log out first')
    return HttpResponse('error!!')


@csrf_exempt
def adminsignup(request):
    '''visitor_add=request.environ["wsgi.input"].stream.raw._sock.getpeername()
    print(visitor_add)
    if visitor_add[0].find('127.0.0')==-1:
        return HttpResponse('error!!!, use proxy fo signup')
    else:'''
    if request.method == 'POST':
        if not request.user.is_authenticated:
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password, is_staff=True)
                user.save()
                admin = models.Admin(admin=user)
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
            check_user = authenticate(username=username, password=password)
            if check_user is not None:
                try:
                    user = models.Users.objects.get(user=check_user)
                    if user.status == 'N':
                        login(request, check_user)
                        return redirect('app1:profile')
                    else:
                        login(request, check_user)
                        return redirect('app1:profile')
                        # return HttpResponse(f'hi {username}!, you are striked. so you cant upload')
                except:
                    return render(request, 'login.html', {'is_staff': False,
                                                          'error_message': 'Incorrect username and / or password.'})
            else:
                return render(request, 'login.html', {'is_staff': False,
                                                      'error_message': 'Incorrect username and / or password.'})
                # return HttpResponse(f'invalid username.')
        else:
            return render(request, 'login.html', {'is_staff': False})
    else:
        return HttpResponse(f'you need to log out first')


@csrf_exempt
def admin_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            check_user = authenticate(username=username, password=password)
            if check_user is not None:
                try:
                    admin = models.Admin.objects.get(admin=check_user)
                    if admin.status == 'C':
                        login(request, check_user)
                        return redirect('app1:profile')
                    else:
                        return render(request, 'login.html', {'is_staff': True,
                                                              'error_message': 'Your registration has not been confirmed'})
                except:
                    return render(request, 'login.html', {'is_staff': True,
                                                          'error_message': 'Incorrect username and / or password.'})
            else:
                return render(request, 'login.html', {'is_staff': False,
                                                      'error_message': 'Incorrect username and / or password.'})
        else:
            return render(request, 'login.html', {'is_staff': True})
    else:
        return HttpResponse(f'you need to log out first')


@csrf_exempt
@login_required
def user_logout(request):
    logout(request)
    return HttpResponse(f'goodbye!')


@csrf_exempt
def strike_resolving(request, username):
    try:
        if not connected_to_proxy(request):
            return HttpResponse('error: you are not connected to proxy.')
        admin_obj = models.Admin.objects.get(admin__username=request.user)
        user_obj = models.Users.objects.get(user__username=username)
        if user_obj.status == 'S':
            user_obj.status = 'N'
            user_obj.save()
            return HttpResponse('The user removed from the strike mode')
        else:
            return HttpResponse('The user was not strike')
    except Exception as e:
        return HttpResponse(e)


# ------------------------------------------  videos -------------------------------------
@csrf_exempt
def upload_video(request):
    try:
        if request.method == 'POST':
            MAX_UPLOAD_SIZE = 52428800
            title = request.POST['title']
            video_file = request.FILES['video_file']
            user_obj = models.Users.objects.get(user__username=request.user)

            if user_obj.status == 'N':
                if video_file.size > MAX_UPLOAD_SIZE:
                    return HttpResponse(f'error: file size should be under 50MB.')
                if not str(video_file).endswith('.mp4'):
                    return HttpResponse(f'file format should be .mp4')
                upload_video = models.Video(user=user_obj, title=title, video_file=video_file)
                upload_video.save()
                return HttpResponse('The video has been uploaded.')
            else:
                return HttpResponse('you are striked!!')

    except Exception as e:
        return HttpResponse('error')


@csrf_exempt
def add_label(request):
    try:
        if request.method == 'POST':
            if not connected_to_proxy(request):
                return HttpResponse('error: you are not connected to proxy.')
            video_id = request.POST['video_id']
            admin_obj = models.Admin.objects.get(admin__username=request.user)
            video_obj = models.Video.objects.get(id=video_id)
            if video_obj.label == 'U':
                video_obj.label = 'L'
                video_obj.save()
                return HttpResponse('label add')
            else:
                video_obj.label = 'U'
                video_obj.save()
                return HttpResponse('label remove')
    except:
        return HttpResponse('error')


@csrf_exempt
def video_status(request):
    try:
        if request.method == 'POST':
            if not connected_to_proxy(request):
                return HttpResponse('error: you are not connected to proxy.')
            video_id = request.POST['video_id']
            admin_obj = models.Admin.objects.get(admin__username=request.user)
            video_obj = models.Video.objects.get(id=video_id)
            if video_obj.status == 'A':
                video_obj.status = 'I'
                video_obj.save()
                user_object = video_obj.user
                if user_object.status == 'N':
                    user_object.unavailable_videos_count += 1
                    user_object.save()
                    if user_object.unavailable_videos_count == 2:
                        user_object.status = 'S'
                        user_object.save()
                        return HttpResponse('The video became unavailable,and user has been striked')
                return HttpResponse('The video became unavailable')
            else:
                return HttpResponse('The video was unavailable')
    except:
        return HttpResponse('error')


@csrf_exempt
@login_required
def stream_video(request, video_id):
    try:
        video_obj = models.Video.objects.get(id=video_id)
        if video_obj.status == 'I':
            return HttpResponse('video is unavailable')
        comments = models.Comment.objects.filter(video=video_obj)
        user_vote = ''
        if not request.user.is_staff:
            user_obj = models.Users.objects.get(user__username=request.user)
            user_vote = models.user_vote(user_obj, video_obj)
        return render(request, 'video_view.html', {'video_url': f'f/',
                                                   'video': video_obj,
                                                   'video_id': video_id,
                                                   'comments': comments,
                                                   'user_vote': user_vote})
    except models.Video.DoesNotExist:
        return HttpResponse('invalid video ID')


@login_required
@csrf_exempt
def fstream(request, video_id):
    video_obj = models.Video.objects.get(id=video_id)
    if video_obj.status == 'I':
        return HttpResponse('video is unavailable')
    path = video_obj.get_path()
    size = os.path.getsize(path)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = models.range_re.match(range_header)
    content_type, encoding = mimetypes.guess_type(path)
    file = open(path, 'rb')
    if range_match:
        start, end = range_match.groups()
        start = int(start)
        end = int(end) if end else size - 1
        if end >= size:
            end = size - 1
        length = end - start + 1

        bytes = models.RangeFileWrapper(file, offset=start, length=length)
        resp = StreamingHttpResponse(bytes, status=206, content_type=content_type)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (start, end, size)
        resp['Content-Length'] = str(length)
    else:
        bytes = FileWrapper(file)
        resp = StreamingHttpResponse(bytes, content_type=content_type)
        resp['Content-Length'] = str(size)
        resp['Cache-Control'] = 'no-cache'
    resp['Accept-Ranges'] = 'bytes'
    return resp


@csrf_exempt
def add_comment(request, video_id):
    try:
        if request.method == 'POST':
            video_id = video_id
            comment = request.POST['comment']
            video_obj = models.Video.objects.get(id=video_id)
            user_obj = models.Users.objects.get(user__username=request.user)
            if not len(comment.split()):
                return JsonResponse({'update_error': {'msg': 'you cant post an empty comment!'}})
            create_comment = models.Comment.objects.create(video=video_obj, user=user_obj, comment=comment)
            create_comment.save()
            resp = {'cmn_username': user_obj.user.username, 'cmn_text': comment}
            return JsonResponse({'update_data': resp})
    except models.Users.DoesNotExist:
        return JsonResponse({'update_error': {'msg': 'you cant post comment!'}})
    except models.Video.DoesNotExist:
        return JsonResponse({'update_error': {'msg': 'invalid video ID'}})


@csrf_exempt
def add_like(request, video_id):
    try:
        '''if request.method == 'POST':
            video_id = request.POST['video_id']'''
        user_obj = models.Users.objects.get(user__username=request.user)
        video_obj = models.Video.objects.get(id=video_id)
        if user_obj in video_obj.dislikes.all():
            video_obj.dislikes.remove(user_obj)
            video_obj.likes.add(user_obj)
        elif user_obj in video_obj.likes.all():
            video_obj.likes.remove(user_obj)
        else:
            video_obj.likes.add(user_obj)
        user_vote = models.user_vote(user_obj, video_obj)
        resp = {'likes_count': video_obj.like_count(),
                'dislikes_count': video_obj.dislike_count(),
                'user_vote': user_vote}
        return JsonResponse({'update_data': resp})
    except models.Users.DoesNotExist:
        return JsonResponse({'update_error': {'msg': 'you cant vote!'}})

    except models.Video.DoesNotExist:
        return JsonResponse({'update_error': {'msg': 'invalid video ID'}})


@csrf_exempt
def add_dislike(request, video_id):
    try:
        user_obj = models.Users.objects.get(user__username=request.user)
        video_obj = models.Video.objects.get(id=video_id)
        if user_obj in video_obj.likes.all():
            video_obj.likes.remove(user_obj)
            video_obj.dislikes.add(user_obj)
        elif user_obj in video_obj.dislikes.all():
            video_obj.dislikes.remove(user_obj)
        else:
            video_obj.dislikes.add(user_obj)
        user_vote = models.user_vote(user_obj, video_obj)
        resp = {'likes_count': video_obj.like_count(),
                'dislikes_count': video_obj.dislike_count(),
                'user_vote': user_vote}
        return JsonResponse({'update_data': resp})
    except models.Users.DoesNotExist:
        return JsonResponse({'update_error': {'msg': 'you cant vote!'}})

    except models.Video.DoesNotExist:
        return JsonResponse({'update_error': {'msg': 'invalid video ID'}})


@csrf_exempt
@login_required
def watch_video(request, video_id):
    try:
        video_obj = models.Video.objects.get(id=video_id)
        if video_obj.video_status != 'I':
            comments = models.Comment.objects.filter(video=video_obj)
            video_comments = [{'user': comment.user.user.username, 'comment': comment.comment} for comment in comments]
            video_likes = video_obj.likes.all().count()
            video_dislikes = video_obj.dislikes.all().count()
            details = {'Title': video_obj.title,
                       'publisher': video_obj.user.user.username,
                       'publish date': str(video_obj.pub_date),
                       'label': video_obj.label,
                       'likes': video_likes,
                       'dislikes': video_dislikes,
                       'comments': video_comments}

            user = request.user
            password = request.POST['password']
            client = Client('127.0.0.1', 8001, video_id, user.username, password)
            return JsonResponse({'details': details})

        else:
            return HttpResponse(f'video is inaccessible')
    except models.Video.DoesNotExist:
        return HttpResponse(f'There is no video with id={video_id}')


def connected_to_proxy(request):
    visitor_add = request.environ["wsgi.input"].stream.raw._sock.getpeername()
    print(visitor_add)
    if visitor_add[0].find('127.0.0') == -1:
        return False
    else:
        return True
