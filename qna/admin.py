from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Question)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user','content','created_at', 'updated_at']
    list_display_links = ['id', 'title','content']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'answer_order', 'answer_depth', 'parent_answer','created_at', 'updated_at']
    list_display_links = ['id', 'user']



# admin.site.register(QuestionReaction)
# admin.site.register(AnswerReaction)
admin.site.register(QnaTag)
#admin.site.register(QnaTagging)
