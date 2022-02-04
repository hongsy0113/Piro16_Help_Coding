from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
# admin.site.register(QuestionReaction)
# admin.site.register(AnswerReaction)
admin.site.register(QnaTag)
#admin.site.register(QnaTagging)
