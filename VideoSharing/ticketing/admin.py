from django.contrib import admin
from .models import Ticket, Comment


# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'status', 'assignee')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'created_on')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment, CommentAdmin)
