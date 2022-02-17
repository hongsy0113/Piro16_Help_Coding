from django.urls import path
from . import views
from .views import FileDownloadView

app_name = 'group'

urlpatterns = [
    path('', view=views.group_home, name='group_home'),
    path('group_search_public/', view=views.group_search_public, name='group_search_public'),
    path('group_create/', view=views.group_create, name='group_create'),
    path('<int:pk>/group_update/', view=views.group_update, name='group_update'),
    path('<int:pk>/group_delete/', view=views.group_delete, name='group_delete'),
    path('<int:pk>/group_drop/', view=views.group_drop, name='group_drop'),
    path('<int:pk>/group_detail/', view=views.group_detail, name='group_detail' ),
    path('group_list/', view=views.group_list, name='group_list'),
    path('<int:pk>/public_group_join/', view=views.public_group_join, name='public_group_join'),
    path('<int:pk>/group_wait_cancel/', view=views.group_wait_cancel, name='group_wait_cancel'),
    path('interest_ajax/', view=views.interest_ajax, name='interest_ajax'),
    path('join_code_ajax/', view=views.join_code_ajax, name='join_code_ajax'),
    path('create_code_ajax/', view=views.create_code_ajax, name='create_code_ajax'),
    path('wait_list_ajax/', view=views.wait_list_ajax, name='wait_list_ajax'),
    path('group_star_ajax/', view=views.group_star_ajax, name='group_star_ajax'),
    path('group_join_accept/', view=views.group_join_accept, name='group_join_accept'),
    path('group_join_reject/', view=views.group_join_reject, name='group_join_reject'),
    path('group_member_state/', view=views.group_member_state, name='group_member_state'),
    # path('<int:pk>/member_thumbnail/', view=views.member_thumbnail, name='member_thumbnail'),
    #### 게시판 관련 url
    path('<int:pk>/post_list/', view=views.post_list, name='post_list'),
    path('<int:pk>/post_create/', view=views.post_create, name='post_create'),
    path('<int:pk>/post_update/<int:post_pk>', view=views.post_update, name='post_update'),
    path('<int:pk>/post_delete/<int:post_pk>', view=views.post_delete, name='post_delete'),
    path('<int:group_pk>/post_detail/<int:pk>', view=views.GroupPostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/search_list/', view=views.search_result, name='search_result'),
    path('answer_ajax/', view=views.answer_ajax, name='answer_ajax'),
    path('reply_ajax/', view=views.reply_ajax, name='reply_ajax'),
    path('post_like_ajax/', view=views.post_like_ajax, name='post_like_ajax'),
    path('answer_like_ajax/', view=views.answer_like_ajax, name='answer_like_ajax'),
    path('answer_delete_ajax/', view=views.answer_delete_ajax, name='answer_delete_ajax'),
    path('answer_edit_ajax/', view=views.answer_edit_ajax, name='answer_edit_ajax'),
    path('answer_edit_submit_ajax/', view=views.answer_edit_submit_ajax, name='answer_edit_submit_ajax'),
    path('<int:pk>/download/', FileDownloadView.as_view(), name="download"),
]