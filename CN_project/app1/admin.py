from django.contrib import admin
from . import models


@admin.register(models.Users)
class UserManager(admin.ModelAdmin):
    list_display = ('user', 'status')
    list_filter = ('status',)


@admin.register(models.Admin)
class AdminManager(admin.ModelAdmin):
    list_display = ('admin', 'status')
    list_filter = ('status',)


@admin.register(models.Video)
class AdminManager(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'pub_date', 'status', 'label', 'video_file')
    list_filter = ('id', 'title', 'user', 'pub_date', 'status', 'label')


@admin.register(models.Comment)
class AdminManager(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment', 'video')
    list_filter = ('id', 'user', 'comment', 'video')

