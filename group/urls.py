from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.group_home, name='group_home'),
    path('group_create/', view=views.group_create, name='group_create'),
    path('group_list/', view=views.group_list, name='group_list')
]