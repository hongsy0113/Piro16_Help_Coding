from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Group)
admin.site.register(GroupPost)
admin.site.register(GroupAnswer)

admin.site.register(GroupTag)
