from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname']
    list_display_links = ['id', 'nickname']

    
admin.site.register(Job)
admin.site.register(Reward)
admin.site.register(GetReward)
admin.site.register(Alert)
