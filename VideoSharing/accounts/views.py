import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from templates import commands


# Create your views here.

'''def index(request):
    return HttpResponse(commands.user_commands())

@csrf_exempt
def extract_keywords(request):
    text = request.POST.get('text')
    return JsonResponse(text)'''


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:

            form_data = json.loads(request.body.decode())
            username = form_data['username']
            password = form_data['password']

            user = authenticate(username=username, password=password)
            if not user:
                return HttpResponse(f'invalid username.')
            if user.is_active:
                login(request, user)
                return HttpResponse(f'hi {username}!')

        return HttpResponse(f'you need to log out first')


@csrf_exempt
@login_required
def user_logout(request):
    logout(request)
    return HttpResponse(f'goodbye!')


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form_data = json.loads(request.body.decode())
            username = form_data['username']
            password = form_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse(f'welcome {username}! you can login now.')
        return HttpResponse(f'you need to log out first')
    return HttpResponse('')
