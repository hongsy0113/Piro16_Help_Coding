'''
(1) question : 질문 글
(2) answer : 답변 글 (대댓글이 아닌 댓글)
(3) answer_reply : 대댓글
(4) comment : 모든 댓글 (answer + answer_reply)
'''

# 직업 선택지
JOB_CHOICE = (('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'), ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('etc', '기타'))
JOB_CATEGORY = {'student': ['elementary_school', 'middle_school', 'high_school'],
                'adult': ['university', 'programmer', 'parents', 'etc']}

# 레벨 체계
LEVEL = (('level_1', '1단계'), ('level_2', '2단계'), ('level_3', '3단계'), ('level_4', '4단계'), ('level_5', '5단계'))
LEVEL_UP_BOUNDARY = {'student': [0, 100, 200, 300, 400], 'adult': [0, 150, 300, 450, 500]}
POINT = {'student': {'question_like': 20, 'comment_like': 15, 'question': 10, 'answer': 5, 'answer_reply': 5},
        'adult': {'question_like': 10, 'comment_like': 20, 'question': 5, 'answer': 10, 'answer_reply': 5}}
        # 좋아요(질문) / 좋아요(댓글) / 글(질문) / 댓글(답변) / 대댓글

# 업적 체계
REWARD_TYPE = (('total_like', '총 좋아요 수'), ('question_like', '게시글 좋아요 수'), ('comment_like', '댓글 좋아요 수'),
        ('total_question', '총 질문 수'), ('total_answer', '총 답변 수'), ('total_comment', '총 댓글 수'),
        ('total_group_joined', '총 가입한 그룹 수'), ('total_group_created', '총 개설한 그룹 수'))