from django.http import HttpResponse, JsonResponse
from templates import commands
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    urls = commands.account_urls()
    urls += ['<br><br>'] + commands.ticketing_urls()
    return HttpResponse(urls)

