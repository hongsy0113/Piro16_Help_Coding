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
