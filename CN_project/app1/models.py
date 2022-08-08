from django.contrib.auth.models import User
from django.db import models
import os, re


# ------------------------------------------  management -------------------------------------
class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strike_status = (('S', 'striked'), ('N', 'non-striked'))
    status = models.CharField(max_length=1, choices=strike_status, default='N', help_text='Strike status')
    unavailable_videos_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User management'
        verbose_name_plural = 'User management'


class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    register_status = (('N', 'not confirmed'), ('C', 'confirmed'))
    status = models.CharField(max_length=1, choices=register_status, default='N', help_text='Register status')

    def __str__(self):
        return self.admin.username

    class Meta:
        verbose_name = 'Admin management'
        verbose_name_plural = 'Admin management'


# ------------------------------------------  videos -------------------------------------

def user_vote(user_obj, video_obj):
    if user_obj in video_obj.likes.all():
        return 'liked'
    elif user_obj in video_obj.dislikes.all():
        return 'disliked'
    return ''


class Video(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    pub_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField('Users', related_name='likes')
    dislikes = models.ManyToManyField('Users', related_name='dislike')
    video_status = (('A', 'accessible'), ('I', 'inaccessible'))
    label_status = (('L', 'limited'), ('U', 'unlimited'))
    label = models.CharField(max_length=1, choices=label_status, default='U', help_text='label status')
    status = models.CharField(max_length=1, choices=video_status, default='A', help_text='Video status')

    def __str__(self):
        return '%s , %s,  like_count: %s, dislike_count: %s' % (
            self.title, self.video_file, self.likes.all().count(), self.dislikes.all().count())

    def like_count(self):
        return self.likes.all().count()

    def dislike_count(self):
        return self.dislikes.all().count()

    def get_path(self):
        path = str(os.path.dirname(os.path.abspath("__file__")).replace('\\', '/').replace('/app1', ''))
        return path + '/media/' + str(self.video_file)


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)

    def __str__(self):
        return ('%s, %s ,%s') % (self.user.user, self.video, self.comment)


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, file, chunksize=4096, offset=0, length=None):
        self.file = file
        self.file.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.chunksize = chunksize

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining:
            data = self.file.read(self.chunksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.file.read(min(self.remaining, self.chunksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

    def close(self):
        self.file.close()
