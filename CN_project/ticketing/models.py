from django.db import models
from django.contrib.auth.models import User


class TicketStatus(models.TextChoices):
    OPEN = 'OPEN'
    PENDING = 'PENDING'
    RESOLVED = 'SOLVED'
    CLOSED = 'CLOSED'


class Ticket(models.Model):
    title = models.CharField('title', max_length=200)
    owner = models.ForeignKey(User, related_name='owner', blank=True, null=True, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.OPEN)

    def to_dict(self):
        d = {'id': self.id,
             'title': self.title,
             'owner': self.owner.username,
             'assignee': self.assignee.username if self.assignee else None,
             'status': self.status}
        return d


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='ticket', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField('text', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.user.username} ({str(self.created_on)}) : {self.text}'

    def to_dict(self):
        return {'from': self.user.username,
                'date': self.created_on.strftime('%Y-%m-%d %H:%M'),
                'text': self.text}
