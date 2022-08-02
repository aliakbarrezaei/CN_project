from django.db import models
from django.contrib.auth.models import User


class TicketStatus(models.TextChoices):
    OPEN = 'Open'
    PENDING = 'Pending'
    RESOLVED = 'Solved'
    CLOSED = 'Closed'


class Ticket(models.Model):
    title = models.CharField('title', max_length=200)
    owner = models.ForeignKey(User, related_name='owner', blank=True, null=True, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', null=True, blank=True, on_delete=models.CASCADE)

    status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    description = models.TextField('description', blank=True, null=True)
    reply = models.TextField('reply', blank=True, null=True)
    '''created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    closed_at = models.DateTimeField('closed at', blank=True, null=True)'''


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='ticket', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', blank=True, null=True, on_delete=models.CASCADE)
    body = models.TextField('body', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']


