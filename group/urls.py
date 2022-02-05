from django.urls import path
from . import views

#app_name = 'group'

urlpatterns = [
    path('', view=views.group_home, name='group_home'),
    path('group_create/', view=views.group_create, name='group_create'),
    path('<int:pk>/group_update/', view=views.group_update, name='group_update'),
    path('<int:pk>/group_delete/', view=views.group_delete, name='group_delete'),
    path('<int:pk>/group_detail/', view=views.group_detail, name='group_detail' ),
    path('<int:pk>/create_code/', view=views.create_code, name='create_code'),
    path('join_group/', view=views.join_group, name='join_group'),
    # path('<int:pk>/join_group/', view=views.join_group_each, name='join_group_each'),
    path('star_ajax/', view=views.star_ajax, name='star_ajax'),
    # path('group_list/', view=views.group_list, name='group_list')
]