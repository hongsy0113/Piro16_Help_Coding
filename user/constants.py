'''
(1) question : 질문 글
(2) answer : 답변 글 (대댓글이 아닌 댓글)
(3) answer_reply : 대댓글
(4) comment : 모든 댓글 (answer + answer_reply)
'''

# 기본 이미지 선택지
BASE_IMAGES = ('profile1.png', 'profile2.png', 'profile3.png', 'profile4.png')

# 직업 선택지
JOB_CHOICE = (('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'),
              ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('teacher', '교사'), ('etc', '기타'))
JOB_CATEGORY = {'student': ['elementary_school', 'middle_school', 'high_school'],
                'adult': ['university', 'programmer', 'parents', 'teacher', 'etc']}

# 레벨 체계
LEVEL = (('level_1', '1단계'), ('level_2', '2단계'),
         ('level_3', '3단계'), ('level_4', '4단계'), ('level_5', '5단계'))
LEVEL_STEP = [LEVEL[i][0] for i in range(len(LEVEL))]
LEVEL_UP_BOUNDARY = {'student': [0, 100, 200, 300, 400],
                     'adult': [0, 150, 300, 450, 500]}
POINT_TYPE = (('question_like', '질문에 대한 좋아요 획득'), ('comment_like', '댓글에 대한 좋아요 획득'), ('question', '질문 작성'), ('answer', '답변 작성'), ('answer_reply', '대댓글 작성'),
              ('question_like_cancel', '질문에 대한 좋아요 취소'), ('comment_like_cancel', '댓글에 대한 좋아요 취소'), ('question_cancel', '질문 삭제'), ('answer_cancel', '답변 삭제'), ('answer_reply_cancel', '대댓글 삭제'))
POINT = {'student': {'question_like': 20, 'comment_like': 15, 'question': 10, 'answer': 5, 'answer_reply': 5},
         'adult': {'question_like': 10, 'comment_like': 20, 'question': 5, 'answer': 10, 'answer_reply': 5}}

# 업적 체계
REWARD_TYPE = (('total_like', '총 좋아요 수'), ('question_like', '게시글 좋아요 수'),
               ('comment_like', '댓글 좋아요 수'), ('total_question', '총 질문 수'),
               ('total_answer', '총 답변 수'), ('total_comment', '총 댓글 수'),
               ('total_group_joined', '총 가입한 그룹 수'), ('total_group_created',
                                                      '총 개설한 그룹 수 (위임 포함)'),
               ('total_group_post', '그룹에서 공유한 글 수'))

# 알림 체계
ALERT_TYPE = (('level_up', '레벨 상승'), ('level_change', '레벨 변경'), ('get_reward', '배지 획득'), ('new_comment_qna', '새 댓글 (묻고 답하기)'), ('new_reply_qna', '새 대댓글 (묻고 답하기)'), ('new_comment_group', '새 댓글 (내 그룹)'), ('new_reply_group', '새 대댓글 (내 그룹)'),
              ('group_create', '그룹 생성'), ('group_join', '그룹 가입'), ('group_reject',
                                                                   '그룹 거절'), ('group_register', '그룹 가입 신청'),
              ('group_delete', '그룹 삭제'), ('group_drop', '그룹 탈퇴'), ('group_maker', '그룹 대표 위임'), ('etc', '기타'))

# 업적 종류
REWARD_ALL = (
  # name, info, type, criteria, img
  ('좋아요2', '총 좋아요 수 2개 달성', 'total_like', 2, '/static/img/reward/heart/heart2.png'),
  ('좋아요5', '총 좋아요 수 5개 달성', 'total_like', 5, '/static/img/reward/heart/heart5.png'),
  ('좋아요10', '총 좋아요 수 10개 달성', 'total_like', 10, '/static/img/reward/heart/heart10.png'),
  ('좋아요20', '총 좋아요 수 20개 달성', 'total_like', 20, '/static/img/reward/heart/heart20.png'),
  ('좋아요50', '총 좋아요 수 50개 달성', 'total_like', 50, '/static/img/reward/heart/heart50.png'),
  ('좋아요100', '총 좋아요 수 100개 달성', 'total_like', 100, '/static/img/reward/heart/heart100.png'),

  ('질문2', '총 질문 수 2개 달성', 'total_question', 2, '/static/img/reward/question/question2.png'),
  ('질문5', '총 질문 수 5개 달성', 'total_question', 5, '/static/img/reward/question/question5.png'),
  ('질문10', '총 질문 수 10개 달성', 'total_question', 10, '/static/img/reward/question/question10.png'),
  ('질문20', '총 질문 수 20개 달성', 'total_question', 20, '/static/img/reward/question/question20.png'),
  ('질문50', '총 질문 수 50개 달성', 'total_question', 50, '/static/img/reward/question/question50.png'),
  ('질문100', '총 질문 수 100개 달성', 'total_question', 100, '/static/img/reward/question/question100.png'),

  ('답변2', '총 답변 수 2개 달성', 'total_answer', 2, '/static/img/reward/answer/answer2.png'),
  ('답변5', '총 답변 수 5개 달성', 'total_answer', 5, '/static/img/reward/answer/answer5.png'),
  ('답변10', '총 답변 수 10개 달성', 'total_answer', 10, '/static/img/reward/answer/answer10.png'),
  ('답변20', '총 답변 수 20개 달성', 'total_answer', 20, '/static/img/reward/answer/answer20.png'),
  ('답변50', '총 답변 수 50개 달성', 'total_answer', 50, '/static/img/reward/answer/answer50.png'),
  ('답변100', '총 답변 수 100개 달성', 'total_answer', 100, '/static/img/reward/answer/answer100.png'),

  ### 여기부터 이미지 없음
  ('댓글2', '총 댓글 수 2개 달성', 'total_comment', 2, '/static/img/reward/base1.png'),
  ('댓글5', '총 댓글 수 5개 달성', 'total_comment', 5, '/static/img/reward/base1.png'),
  ('댓글10', '총 댓글 수 10개 달성', 'total_comment', 10, '/static/img/reward/base1.png'),
  ('댓글20', '총 댓글 수 20개 달성', 'total_comment', 20, '/static/img/reward/base1.png'),
  ('댓글50', '총 댓글 수 50개 달성', 'total_comment', 50, '/static/img/reward/base1.png'),
  ('댓글100', '총 댓글 수 100개 달성', 'total_comment', 100, '/static/img/reward/base1.png'),

  ('게시글 좋아요2', '한 게시글 좋아요 수 2개 달성', 'question_like', 2, '/static/img/reward/base1.png'),
  ('게시글 좋아요5', '한 게시글 좋아요 수 5개 달성', 'question_like', 5, '/static/img/reward/base1.png'),
  ('게시글 좋아요10', '한 게시글 좋아요 수 10개 달성', 'question_like', 10, '/static/img/reward/base1.png'),

  ('댓글 좋아요2', '한 댓글 좋아요 수 2개 달성', 'comment_like', 2, '/static/img/reward/base1.png'),
  ('댓글 좋아요5', '한 댓글 좋아요 수 5개 달성', 'comment_like', 5, '/static/img/reward/base1.png'),
  ('댓글 좋아요10', '한 댓글 좋아요 수 10개 달성', 'comment_like', 10, '/static/img/reward/base1.png'),

  ('그룹 가입2', '가입한 그룹 2개 달성', 'total_group_joined', 2, '/static/img/reward/base1.png'),
  ('그룹 가입5', '가입한 그룹 5개 달성', 'total_group_joined', 5, '/static/img/reward/base1.png'),
  ('그룹 가입10', '가입한 그룹 10개 달성', 'total_group_joined', 10, '/static/img/reward/base1.png'),

  ('그룹 대표2', '그룹 2개에서 대표로 활동', 'total_group_created', 2, '/static/img/reward/base1.png'),
  ('그룹 대표5', '그룹 5개에서 대표로 활동', 'total_group_created', 5, '/static/img/reward/base1.png'),
  ('그룹 대표10', '그룹 10개에서 대표로 활동', 'total_group_created', 10, '/static/img/reward/base1.png'),

  ('그룹 공유2', '그룹 게시판에서 글 2개 작성', 'total_group_post', 2, '/static/img/reward/base1.png'),
  ('그룹 공유5', '그룹 게시판에서 글 5개 작성', 'total_group_post', 5, '/static/img/reward/base1.png'),
  ('그룹 공유10', '그룹 게시판에서 글 10개 작성', 'total_group_post', 10, '/static/img/reward/base1.png'),
  ('그룹 공유20', '그룹 게시판에서 글 20개 작성', 'total_group_post', 20, '/static/img/reward/base1.png'),
  ('그룹 공유50', '그룹 게시판에서 글 50개 작성', 'total_group_post', 50, '/static/img/reward/base1.png'),
  ('그룹 공유100', '그룹 게시판에서 글 100개 작성', 'total_group_post', 100, '/static/img/reward/base1.png'),
)