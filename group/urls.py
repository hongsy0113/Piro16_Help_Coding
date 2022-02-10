from django.urls import path
from . import views

app_name = 'group'

urlpatterns = [
    path('', view=views.group_home, name='group_home'),
    path('group_search/', view=views.group_search, name='group_search'),
    path('group_search_public/', view=views.group_search_public, name='group_search_public'),
    path('group_create/', view=views.group_create, name='group_create'),
    path('<int:pk>/group_update/', view=views.group_update, name='group_update'),
    path('<int:pk>/group_delete/', view=views.group_delete, name='group_delete'),
    path('<int:pk>/group_drop/', view=views.group_drop, name='group_drop'),
    path('<int:pk>/group_detail/', view=views.group_detail, name='group_detail' ),
    path('<int:pk>/create_code/', view=views.create_code, name='create_code'),
    path('join_group/', view=views.join_group, name='join_group'),
    path('star_ajax/', view=views.star_ajax, name='star_ajax'),
    path('group_list/', view=views.group_list, name='group_list'),
    path('<int:pk>/public_group_join/', view=views.public_group_join, name='public_group_join'),
    path('<int:pk>/join_list/', view=views.join_list, name='join_list'),
    path('interest_ajax/', view=views.interest_ajax, name='interest_ajax'),
    path('join_code_ajax/', view=views.join_code_ajax, name='join_code_ajax'),
    # path('<int:pk>/member_thumbnail/', view=views.member_thumbnail, name='member_thumbnail'),
]