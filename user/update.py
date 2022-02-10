from .models import User, Reward, GetReward
from .constants import *
from datetime import datetime

# 질문에 좋아요를 달았을 때
def update_question_like(question, posted_user, liked_user):
    # question : 해당 질문
    # posted_user : 질문 작성자
    # liked_user : 좋아요 누른 유저
    posted_user.total_question_like += 1
    posted_user.save()
    update_reward(posted_user, 'total_like', posted_user.total_like())
    update_reward(posted_user, 'question_like', question.like_user.count())


# 질문에 좋아요를 취소했을 때
def update_question_like_cancel(question, posted_user, liked_user):
    # question : 해당 질문
    # posted_user : 질문 작성자
    # liked_user : 좋아요 누른 유저
    posted_user.total_question_like -= 1
    posted_user.save()

# 댓글에 좋아요를 달았을 때
def update_comment_like(comment, commented_user, liked_user):
    # comment : 해당 댓글
    # commented_user : 댓글 작성자
    # liked_user : 좋아요 누른 유저
    commented_user.total_comment_like += 1
    commented_user.save()
    update_reward(commented_user, 'total_like', commented_user.total_like())
    update_reward(commented_user, 'comment_like', comment.like_user.count())

# 댓글에 좋아요를 취소했을 때
def update_comment_like_cancel(comment, commented_user, liked_user):
    # comment : 해당 댓글
    # commented_user : 댓글 작성자
    # liked_user : 좋아요 누른 유저
    commented_user.total_comment_like -= 1
    commented_user.save()

# 질문을 작성했을 때
def update_question(posted_user):
    # posted_user : 질문 작성자
    posted_user.total_question += 1
    posted_user.save()
    update_reward(posted_user, 'total_question', posted_user.total_question)

# 질문을 삭제했을 때
def update_question_cancel(posted_user):
    # posted_user : 질문 작성자
    posted_user.total_question -= 1
    posted_user.save()

# 질문에 답변을 작성했을 때
def update_answer(posted_user, answered_user):
    # posted_user : 질문 작성자
    # answered_user : 답변 작성자
    answered_user.total_answer += 1
    answered_user.save()
    update_reward(answered_user, 'total_comment', posted_user.total_comment())
    update_reward(answered_user, 'total_answer', posted_user.total_answer)

# 질문에 답변을 삭제했을 때
def update_answer_cancel(posted_user, answered_user):
    # posted_user : 질문 작성자
    # answered_user : 답변 작성자
    answered_user.total_answer -= 1
    answered_user.save()

# 질문에 대댓글을 작성했을 때
def update_answer_reply(replied_user):
    replied_user.total_answer_reply += 1
    replied_user.save()
    update_reward(replied_user, 'total_comment', replied_user.total_comment())

# 질문에 대댓글을 삭제했을 때
def update_answer_reply_cancel(replied_user):
    replied_user.total_answer_reply -= 1
    replied_user.save()

# 그룹을 만들었을 때
#def update_group_create(user):

# 그룹에 가입했을 때
#def update_group_join(user):

def update_reward(user, type, current_state):
    if Reward.objects.filter(type = type, criteria = current_state):
        reward = Reward.objects.get(type = type, criteria = current_state)
        if not GetReward.objects.filter(user_id = user, reward_id = reward):
            GetReward.objects.create(user_id = user, reward_id = reward, get_date = datetime.now())