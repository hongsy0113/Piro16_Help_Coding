from .models import User, Reward, GetPoint, GetReward, Alert
from group.models import Group
from .constants import *
from datetime import datetime

# 질문에 좋아요를 달았을 때


def update_question_like(question, posted_user, liked_user):
    # question : 해당 질문
    # posted_user : 질문 작성자
    # liked_user : 좋아요 누른 유저
    if posted_user:
        posted_user.total_question_like += 1
        posted_user.save()
        posted_user.get_level()
        update_point_history(posted_user, 'question_like')
        update_reward(posted_user, 'total_like', posted_user.total_like())
        update_reward(posted_user, 'question_like', question.like_user.count())

# 질문에 좋아요를 취소했을 때


def update_question_like_cancel(question, posted_user, liked_user):
    # question : 해당 질문
    # posted_user : 질문 작성자
    # liked_user : 좋아요 누른 유저
    if posted_user:
        posted_user.total_question_like -= 1
        posted_user.save()
        posted_user.get_level()
        update_point_history(posted_user, 'question_like_cancel')

# 댓글에 좋아요를 달았을 때


def update_comment_like(comment, commented_user, liked_user):
    # comment : 해당 댓글
    # commented_user : 댓글 작성자
    # liked_user : 좋아요 누른 유저
    if commented_user:
        commented_user.total_comment_like += 1
        commented_user.save()
        commented_user.get_level()
        update_point_history(commented_user, 'comment_like')
        update_reward(commented_user, 'total_like',
                      commented_user.total_like())
        update_reward(commented_user, 'comment_like',
                      comment.like_user.count())

# 댓글에 좋아요를 취소했을 때


def update_comment_like_cancel(comment, commented_user, liked_user):
    # comment : 해당 댓글
    # commented_user : 댓글 작성자
    # liked_user : 좋아요 누른 유저
    if commented_user:
        commented_user.total_comment_like -= 1
        commented_user.save()
        commented_user.get_level()
        update_point_history(commented_user, 'comment_like_cancel')

# 질문을 작성했을 때


def update_question(question, posted_user):
    # question : 해당 질문
    # posted_user : 질문 작성자
    if posted_user:
        posted_user.total_question += 1
        posted_user.save()
        posted_user.get_level()
        update_point_history(posted_user, 'question')
        update_reward(posted_user, 'total_question',
                      posted_user.total_question)

# 질문을 삭제했을 때


def update_question_cancel(question, posted_user):
    # question : 해당 질문
    # posted_user : 질문 작성자
    if posted_user:
        posted_user.total_question -= 1
        posted_user.save()
        posted_user.get_level()
        update_point_history(posted_user, 'question_cancel')
        for num_like in range(question.like_user.count()):
            posted_user.total_question_like -= 1
            update_point_history(posted_user, 'question_like_cancel')
        posted_user.save()

# 질문에 답변을 작성했을 때


def update_answer(question, answer, posted_user, answered_user):
    # question : 해당 질문
    # answer : 해당 답변
    # posted_user : 질문 작성자
    # answered_user : 답변 작성자
    if answered_user:
        answered_user.total_answer += 1
        answered_user.save()
        answered_user.get_level()
        update_point_history(answered_user, 'answer')
        update_reward(answered_user, 'total_comment',
                      answered_user.total_comment())
        update_reward(answered_user, 'total_answer',
                      answered_user.total_answer)
        if answered_user != posted_user and posted_user:
            Alert.objects.create(user=posted_user, content="[{}] 질문글에 댓글이 달렸어요.".format(
                question.title), alert_type="new_comment", related_id=question.id, time=datetime.now())

# 질문에 답변을 삭제했을 때


def update_answer_cancel(question, answer, posted_user, answered_user):
    # question : 해당 질문
    # answer : 해당 답변
    # posted_user : 질문 작성자
    # answered_user : 답변 작성자
    if answered_user:
        answered_user.total_answer -= 1
        answered_user.save()
        answered_user.get_level()
        update_point_history(answered_user, 'answer_cancel')
        for num_like in range(answer.like_user.count()):
            answered_user.total_comment_like -= 1
            update_point_history(answered_user, 'comment_like_cancel')
        answered_user.save()

# 질문에 대댓글을 작성했을 때


def update_answer_reply(question, reply, replied_user):
    # question : 해당 질문
    # reply : 해당 대댓글
    # replied_user : 대댓글 작성자
    if replied_user:
        replied_user.total_answer_reply += 1
        replied_user.save()
        replied_user.get_level()
        update_point_history(replied_user, 'answer_reply')
        update_reward(replied_user, 'total_comment',
                      replied_user.total_comment())
        if replied_user != question.user and question.user:
            Alert.objects.create(user=question.user, content="[{}] 질문글에 댓글이 달렸어요.".format(
                question.title), alert_type="new_comment", related_id=question.id, time=datetime.now())
        if replied_user != reply.parent_answer.user and reply.parent_answer.user:
            # 댓글을 삭제한 경우 고려해야 함
            Alert.objects.create(user=reply.parent_answer.user, content="[{}] 댓글에 대댓글이 달렸어요.".format(
                reply.parent_answer.content), alert_type="new_reply", related_id=question.id, time=datetime.now())

# 질문에 대댓글을 삭제했을 때


def update_answer_reply_cancel(question, reply, replied_user):
    # question : 해당 질문
    # reply : 해당 대댓글
    if replied_user:
        replied_user.total_answer_reply -= 1
        replied_user.save()
        replied_user.get_level()
        update_point_history(replied_user, 'answer_reply_cancel')
        for num_like in range(reply.like_user.count()):
            replied_user.total_comment_like -= 1
            update_point_history(replied_user, 'comment_like_cancel')
        replied_user.save()

# 그룹을 만들었을 때 (공개/비공개)


def update_group_create(group, created_user):
    Alert.objects.create(user=created_user, content="[{}] 그룹이 만들어졌습니다.".format(
        group.name), alert_type="group_create", related_id=group.id, time=datetime.now())
    update_reward(created_user, 'total_group_created', len(
        Group.objects.filter(maker=created_user)))

# 그룹에 들어갔을 때 (비공개)


def update_private_group_join(group, registered_user):
    Alert.objects.create(user=group.maker, content="[{}] 님이 [{}] 그룹에 가입했습니다.".format(
        registered_user.nickname, group.name), alert_type="group_join", related_id=group.id, time=datetime.now())
    Alert.objects.create(user=registered_user, content="[{}] 그룹에 가입되었습니다.".format(
        group.name), alert_type="group_join", related_id=group.id, time=datetime.now())
    update_reward(registered_user, 'total_group_joined',
                  len(registered_user.group_set.all()))

# 그룹에 가입 신청을 했을 때 (공개)


def update_public_group_register(group, registered_user):
    Alert.objects.create(user=group.maker, content="[{}] 님이 [{}] 그룹에 가입하고 싶어합니다.".format(
        registered_user.nickname, group.name), alert_type="group_register", related_id=group.id, time=datetime.now())
    Alert.objects.create(user=registered_user, content="[{}] 그룹 가입을 요청했습니다. 승인될 때까지 기다려주세요!".format(
        group.name), alert_type="group_register", related_id=group.id, time=datetime.now())

# 그룹 가입 신청을 수락했을 때 (공개)


def update_public_group_join(group, registered_user):
    Alert.objects.create(user=group.maker, content="[{}] 님이 [{}] 그룹에 가입했습니다.".format(
        registered_user.nickname, group.name), alert_type="group_join", related_id=group.id, time=datetime.now())
    Alert.objects.create(user=registered_user, content="[{}] 그룹에 가입되었습니다.".format(
        group.name), alert_type="group_join", related_id=group.id, time=datetime.now())
    update_reward(registered_user, 'total_group_joined',
                  len(registered_user.group_set.all()))

# 그룹 가입 신청을 거절했을 때 (공개)


def update_public_group_reject(group, registered_user):
    Alert.objects.create(user=registered_user, content="[{}] 그룹 가입 신청이 거절되었습니다.".format(
        group.name), alert_type="group_reject", related_id=group.id, time=datetime.now())


# 그룹 대표를 넘겨줄 때

def update_change_group_maker(group, original_maker, new_maker):
    Alert.objects.create(user=original_maker, content="[{}] 그룹에서 탈퇴했습니다.".format(
        group.name), alert_type="group_drop", related_id=group.id, time=datetime.now())
    Alert.objects.create(user=new_maker, content="[{}] 그룹 대표가 되었습니다.".format(
        group.name), alert_type="group_maker", related_id=group.id, time=datetime.now())


# 그룹을 탈퇴할 때
def update_drop_group(group, dropped_user):
    Alert.objects.create(user=dropped_user, content="[{}] 그룹에서 탈퇴했습니다.".format(
        group.name), alert_type="group_drop", related_id=group.id, time=datetime.now())

# 그룹을 삭제할 때


def update_delete_group(group):
    for member in group.members.all():
        Alert.objects.create(user=member, content="[{}] 그룹이 삭제되었습니다.".format(
            group.name), alert_type="group_delete", related_id=group.id, time=datetime.now())

# 업적 업데이트


def update_reward(user, type, current_state):
    if Reward.objects.filter(type=type, criteria=current_state):
        reward = Reward.objects.get(type=type, criteria=current_state)
        if not GetReward.objects.filter(user=user, reward=reward):
            GetReward.objects.create(
                user=user, reward=reward, get_date=datetime.now())
            Alert.objects.create(user=user, content="짝짝짝! [{}] 배지를 획득했어요!".format(
                reward.name), alert_type="get_reward", time=datetime.now())

# 포인트 업데이트


def update_point_history(user, type):
    for category in JOB_CATEGORY:
        if user.job in JOB_CATEGORY[category]:
            if '_cancel' not in type:
                point = POINT[category][type]
            else:
                point = POINT[category][type[:-7]] * (-1)
            GetPoint.objects.create(
                user=user, type=type, point=point, get_date=datetime.now())
