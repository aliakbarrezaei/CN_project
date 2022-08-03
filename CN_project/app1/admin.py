from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Users)
class UserManager(admin.ModelAdmin):
    list_display=('user','status')
    list_filter=('status',)
@admin.register(models.Admin)
class AdminManager(admin.ModelAdmin):
    list_display=('admin','status')
    list_filter=('status',)
