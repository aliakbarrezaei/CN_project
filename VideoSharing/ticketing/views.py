import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket, Comment


# Create your views here.

@csrf_exempt
@login_required
def my_tickets_view(request):
    tickets = Ticket.objects.filter(owner=request.user).values()
    # print(tickets)
    return JsonResponse({"tickets": list(tickets)})


@csrf_exempt
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())
        title = form_data['title']
        owner = request.user
        status = 'OPEN'
        description = form_data['description']
        ticket = Ticket(title=title, owner=owner, status=status, description=description)
        ticket.save()

        return HttpResponse('successfully added ticket.')
    return HttpResponse('')


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def create_ticket(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())
        title = form_data['title']
        owner = request.user
        assignee = None
        status = 'OPEN'
        description = form_data['description']
        if request.user.is_staff:
            assignee = User.objects.get(username='manager')
        ticket = Ticket(title=title, owner=owner, status=status, description=description, assignee=assignee)
        ticket.save()

        return HttpResponse('successfully added ticket.')
    return HttpResponse('')


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def unassigned_tickets_view(request):
    if request.method == 'GET':
        tickets = Ticket.objects.filter(assignee=None).values()
        return JsonResponse({"tickets": list(tickets)})


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def assign_ticket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        ticket.assignee = request.user
        ticket.save()
        return HttpResponse('successfully assigned ticket.')
    except Ticket.DoesNotExist:
        return HttpResponse(f'ticket with id={pk} does not exist.')


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff)
def assigned_tickets_view(request):
    tickets = Ticket.objects.filter(assignee=request.user).values()
    return JsonResponse({"tickets": list(tickets)})


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff)
def edit_ticket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        if request.method == 'POST' and request.user == ticket.assignee:
            if ticket.status == 'CLOSED':
                return HttpResponse('cant edit a closed ticket.')

            form_data = json.loads(request.body.decode())
            if 'status' in form_data.keys():
                status = form_data['status']
                if ticket.status == 'CLOSED':
                    return HttpResponse('cant change status a closed ticket.')
                ticket.status = status
            if 'reply' in form_data.keys():
                reply = form_data['reply']
                ticket.reply = reply
            ticket.save()
            return HttpResponse('successfully edited ticket.')
        else:
            return HttpResponse('you cant edit this ticket.')
    except Ticket.DoesNotExist:
        return HttpResponse(f'ticket with id={pk} does not exist.')

