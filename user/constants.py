# 직업 선택지
JOB_CHOICE = (('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'), ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('etc', '기타'))
JOB_CATEGORY = {'student': ['elementary_school', 'middle_school', 'high_school'],
                'adult': ['university', 'programmer', 'parents', 'etc']}

# 레벨 체계
LEVEL = (('level_1', '1단계'), ('level_2', '2단계'), ('level_3', '3단계'), ('level_4', '4단계'), ('level_5', '5단계'))
LEVEL_UP_BOUNDARY = {'student': [0, 100, 200, 300, 400], 'adult': [0, 150, 300, 450, 500]}
POINT = {'student': {'like': 20, 'question': 10, 'answer': 5, 'answer_reply': 5},
        'adult': {'like': 20, 'question': 5, 'answer': 10, 'answer_reply': 5}}
        # 좋아요 / 글(질문) / 댓글(답변) / 대댓글