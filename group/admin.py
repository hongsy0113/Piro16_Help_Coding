from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(GroupPost)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user','content','created_at', 'updated_at']
    list_display_links = ['id', 'title','content']

admin.site.register(Group)

admin.site.register(GroupAnswer)

admin.site.register(GroupTag)

@admin.register(GroupStar)
class GroupStarAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'user']
    list_display_links = ['id', 'group', 'user']