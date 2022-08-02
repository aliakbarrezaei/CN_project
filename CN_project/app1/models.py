from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Video(models.Model):
    user=models.ForeignKey('Users', on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    video_file=models.FileField(upload_to='videos/')
    pub_date=models.DateField(auto_now_add=True)
    likes=models.ManyToManyField(User, related_name='likes')
    dislike=models.ManyToManyField(User, related_name='dislike')
    def __str__(self):
        return self.title

class Comment(models.Model):
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.CharField(max_length=300)

    def __str__(self):
        return self.user.username

class Users(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    strike_status=(('Y','striked'),('N','non-striked'))
    status=models.CharField(max_length=1, choices=strike_status,default='N', help_text='Strike status')
    def __str__(self):
        return self.user.username

class Admin(models.Model):
    admin=models.OneToOneField(User, on_delete=models.CASCADE)
    register_status=(('Y','not confirmed'),('N','confirmed'))
    status=models.CharField(max_length=1, choices=register_status,default='N', help_text='Register status')
    def __str__(self):
        return self.user.username