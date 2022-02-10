from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'nickname']
    list_display_links = ['id', 'email', 'nickname']

admin.site.register(GetPoint)
admin.site.register(Reward)
admin.site.register(GetReward)
admin.site.register(Alert)