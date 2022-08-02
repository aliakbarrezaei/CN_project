from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Video(models.Model):
    user=models.ForeignKey('Users', on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    video_file=models.FileField(upload_to='videos/')
    pub_date=models.DateField(auto_now_add=True)
    likes=models.ManyToManyField('Users', related_name='likes')
    dislikes=models.ManyToManyField('Users', related_name='dislike')
    video_status=(('A','accessible'),('I','inaccessible'))
    label_status=(('L','limited'),('U','unlimited'))
    label=models.CharField(max_length=1, choices=label_status,default='U', help_text='label status')
    status=models.CharField(max_length=1, choices=video_status,default='A', help_text='Video status')
    def __str__(self):
        return '%s , %s,  like_count: %s, dislike_count: %s' %(self.title,self.video_file,self.likes.all().count(),self.dislikes.all().count())

class Comment(models.Model):
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    user=models.ForeignKey('Users', on_delete=models.CASCADE)
    comment=models.CharField(max_length=300)

    def __str__(self):
        return ('%s, %s ,%s') %(self.user.user,self.video,self.comment)

class Users(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    strike_status=(('S','striked'),('N','non-striked'))
    status=models.CharField(max_length=1, choices=strike_status,default='N', help_text='Strike status')
    unavailable_videos_count=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Admin(models.Model):
    admin=models.OneToOneField(User, on_delete=models.CASCADE)
    register_status=(('N','not confirmed'),('C','confirmed'))
    status=models.CharField(max_length=1, choices=register_status,default='N', help_text='Register status')
    def __str__(self):
        return self.admin.username