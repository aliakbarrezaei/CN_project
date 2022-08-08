from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from .models import Ticket, Message
from app1.models import User


@csrf_exempt
@login_required
@user_passes_test(lambda user: not user.is_superuser)
def my_tickets_view(request):
    tickets = [ticket.to_dict() for ticket in Ticket.objects.filter(owner=request.user)]
    return JsonResponse({"tickets": tickets})


@csrf_exempt
@login_required
@user_passes_test(lambda user: not user.is_superuser)
def my_ticket_view(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        if ticket.owner != request.user:
            raise Ticket.DoesNotExist

        return JsonResponse(get_ticket_details(pk))

    except Ticket.DoesNotExist:
        return HttpResponse(f'invalid ticket id.')


def get_ticket_details(pk):
    ticket_dict = Ticket.objects.get(id=pk).to_dict()
    messages = Message.objects.filter(ticket_id=pk)
    messages_list = [msg.to_dict() for msg in messages]
    d = {'ticket': ticket_dict, 'messages': messages_list}
    return d


@csrf_exempt
@login_required
@user_passes_test(lambda user: not user.is_superuser)
def create_ticket(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            text = request.POST['text']
            owner = request.user
            status = 'OPEN'
            assignee = None
            if request.user.is_staff:
                assignee = User.objects.get(user__username='manager')
                status = 'PENDING'

            ticket = Ticket.objects.create(title=title, owner=owner, status=status, assignee=assignee)
            ticket.save()
            message = Message.objects.create(ticket=ticket, user=owner, text=text)
            message.save()
            return HttpResponse('successfully added ticket.')
        except:
            return HttpResponse('error')


@csrf_exempt
@login_required
@user_passes_test(lambda user: not user.is_superuser)
def my_ticket_reply(request, pk):
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(id=pk)
            if ticket.owner != request.user:
                raise Ticket.DoesNotExist
            if ticket.status != 'SOLVED':
                return HttpResponse(f'cant send new message. (ticket status = {ticket.status})')

            ticket.status = 'PENDING'
            ticket.save()
            text = request.POST['text']
            message = Message.objects.create(ticket=ticket, user=request.user, text=text)
            message.save()
            return HttpResponse(f'successfully sent message. (ticket status = {ticket.status})')

        except Ticket.DoesNotExist:
            return HttpResponse(f'invalid ticket id.')


# ------------------------ manage tickets -------------------------------


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff)
def assigned_tickets_view(request):
    tickets = [ticket.to_dict() for ticket in Ticket.objects.filter(assignee=request.user)]
    return JsonResponse({"tickets": tickets})


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff)
def user_ticket_view(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        if ticket.assignee != request.user:
            raise Ticket.DoesNotExist
        return JsonResponse(get_ticket_details(pk))
    except Ticket.DoesNotExist:
        return HttpResponse(f'invalid ticket id.')


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def unassigned_tickets_view(request):
    tickets = [ticket.to_dict() for ticket in Ticket.objects.filter(assignee=None)]
    return JsonResponse({"tickets": tickets})


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def assign_ticket(request, pk):
    try:
        if not connected_to_proxy(request):
            return HttpResponse('error: you are not connected to proxy.')
        ticket = Ticket.objects.get(id=pk)
        if ticket.assignee is not None:
            return HttpResponse('cannot assign this ticket.')
        ticket.assignee = request.user
        ticket.status = 'PENDING'
        ticket.save()
        return HttpResponse('successfully assigned ticket.')
    except Ticket.DoesNotExist:
        return HttpResponse(f'ticket with id={pk} does not exist.')


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff)
def user_ticket_reply(request, pk):
    if request.method == 'POST':
        if not request.user.is_superuser and not connected_to_proxy(request):
            return HttpResponse('error: you are not connected to proxy.')
        try:
            ticket = Ticket.objects.get(id=pk)
            if request.user == ticket.assignee and ticket.status != 'CLOSED':
                text = request.POST['text']
                ticket.status = 'SOLVED'
                ticket.save()
                message = Message.objects.create(ticket=ticket, user=request.user, text=text)
                message.save()
            else:
                return HttpResponse(f'you cant reply to this ticket. (ticket status = {ticket.status})')
            return HttpResponse(f'successfully sent message. (ticket status = {ticket.status})')

        except Ticket.DoesNotExist:
            return HttpResponse(f'invalid ticket id.')


@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_staff)
def user_ticket_close(request, pk):
    if not request.user.is_superuser and not connected_to_proxy(request):
        return HttpResponse('error: you are not connected to proxy.')
    try:
        ticket = Ticket.objects.get(id=pk)
        if request.user == ticket.assignee and ticket.status != 'CLOSED':
            ticket.status = 'CLOSED'
            ticket.save()
            return HttpResponse(f'successfully closed the ticket. (ticket status = {ticket.status})')
        else:
            return HttpResponse(f'you cant edit this ticket. (ticket status = {ticket.status})')
    except Ticket.DoesNotExist:
        return HttpResponse(f'invalid ticket id.')


def connected_to_proxy(request):
    visitor_add = request.environ["wsgi.input"].stream.raw._sock.getpeername()
    print(visitor_add)
    if visitor_add[0].find('127.0.0') == -1:
        return False
    else:
        return True
