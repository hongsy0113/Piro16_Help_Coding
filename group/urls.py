from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.group_home, name='group_home'),
    path('group_create/', view=views.group_create, name='group_create'),
    path('<int:pk>/group_update/', view=views.group_update, name='group_update'),
    path('<int:pk>/group_delete/', view=views.group_delete, name='group_delete'),
    path('group_list/', view=views.group_list, name='group_list')
]