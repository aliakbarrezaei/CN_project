from django.contrib import admin
from .models import Ticket, Message


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'status', 'assignee')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket_id', 'user', 'text', 'created_on')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
