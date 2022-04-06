# 도와줘, 코딩
![도와줘코딩-readme-섬네일-001](https://user-images.githubusercontent.com/87005840/159614128-3c6211e8-6b42-4ca5-8376-4e196f553950.png)
[도와줘, 코딩](https://help-coding.com)


### DEMO 계정
ID: demo@demo.com
Password: demo1234

# 기획의도
코딩 교육이 활성화되면서 코딩을 공부하는 어린이, 청소년들이 많아지고 있습니다.

코딩을 하다보면 문제를 해결하는데 많은 시간을 쏟게 됩니다. 그럴 때 개발자들은 구글 등에서 도움을 많이 받는데요, 

그렇다면 어린이, 청소년 프로그래머가 문제를 쉽게 해결할 수 있는 플랫폼은 없을까요? 

또한 누구나 그룹을 만들어 내가 프로그래밍한 작품을 멤버들과 공유할 수 있다면 더욱 흥미를 가지고 코딩을 배울 수 있지 않을까요?

이러한 고민에서 도와줘, 코딩은 시작되었습니다.

<br/>

도와줘, 코딩의 묻고답하기 게시판에서 궁금한 내용을 질문하세요!

학생, 대학생, 개발자 모두가 질문에 답변을 해줄 수 있습니다. 

답변을 하며 학생들을 도와주고 포인트를 모아보세요!

<br/>

도와줘, 코딩의 그룹 기능을 통해 다양한 공개/비공개 그룹을 만들어보세요!

그룹 게시판에서 자신의 작품을 자랑하고 소통할 수 있습니다.

스크래치, 엔트리 작품 링크를 첨부하면 도와줘, 코딩에서도 작품을 실행할 수 있어요.

<br/>

도와줘, 코딩이 많은 어린이, 청소년 프로그래머에게 도움이 되길 바랍니다 😄

# 주요기능
* 질문 및 답변 작성, 대댓글 작성
* 질문 정렬, 필터 기능 - (최신순, 조회수순, 좋아요순), (답변완료/미완료, 스크래치/엔트리/기타)
* 질문 좋아요, 답변 좋아요
* 게시글 해시태그 기능
* 게시글 검색 기능(제목, 내용, 해시태그)
* 공개/비공개 그룹 생성, 참가, 초대, 탈퇴, 삭제
* 그룹 게시글 및 댓글 작성
* 그룹 찜하기, 좋아요
* 그룹 검색, 그룹 게시글 검색 기능
* 스크래치, 엔트리 작품 첨부 기능
* 계정 프로필 관리.
* 배지 획득, 포인트 쌓기 기능
* 알림 확인 기능

# version

* ver.1.0.0(2022/2/20): <br/>Django, HTML with Django Template, CSS, Vanila JavaScript, AWS
* ver.1.0.1(2022/2/24): <br/>그룹게시판 iframe 오류 수정. 그룹게시판 iframe, 섬네일 이미지 로딩 지연 문제 해결. 질문 답변 여부 필터 오류 수정
* ver.1.1.0(2022/3/12): <br/>검색엔진 최적화. 트위터/페이스북/카카오톡 공유 HTML meta tag 추가
* ver.1.1.1(2022/3/13): <br/>한글명 파일 다운로드 시 파일명,확장자 바뀌는 문제 해결
* ver.1.2.0(2022/3/13): <br/>게시글의 해시태그 클릭 시 해당 태그가진 게시글 목록으로 이동 기능 추가
* ver.1.3.0(2022/3/16): <br/>메인 페이지 최근 질문&답변 띄우기 기능 추가. qna 검색 결과 페이지네이션 오류 수정
* ver.1.4.0(2022/3/16): <br/>채널톡 상담 기능 추가
* ver.1.4.1(2022/3/21): <br/>에러메시지, 삭제 확인 메시지 수정. 게시글 개행 오류 수정
* ver.1.4.2(2022/3/29): <br/>랜딩페이지 모바일 버전 반응형 구현
* ver.1.4.3(2022/4/5): <br/>footer 연락처 링크 추가, 댓글 입력창 개행 오류 수정

### 추가될 기능
* 반응형 웹사이트
* 신고하기 기능
* sb2, ent 파일 실행 기능
* 다양한 배지, 업적

### 코드 컨벤션
* Python
  *  변수, 함수, 메서드 네이밍은 underscore
  *  클래스 네이밍은 IntitialCaps
  *  단따옴표 사용. 문자열이 단따옴표를 포함하는 경우에만 쌍따옴표 사용
  *  디테일한 python, django 컨벤션은 다음 문서를 따름 (https://candypoplatte.github.io/2018/10/10/django_coding_style/)
* JavaScript
  *  변수, 함수, 객체 네이밍은 lowerCamelCase
  *  클래스 네이밍은 PascalCase
  *  디테일한 JavaScript 컨벤션은 다음 문서를 따름(https://velog.io/@cada/%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%BD%94%EB%94%A9-%EB%B0%8F-%EB%84%A4%EC%9D%B4%EB%B0%8D-%EC%BB%A8%EB%B2%A4%EC%85%98-1%ED%8E%B8)
* HTML, CSS
  * BEM 방법론 사용(Block, Element, Modifier)
  * double underscore와 double dash를 이용하여, Block, Element, Modifier를 구분 짓고, 위계화 하여 컴포넌트화 한다.

### 커밋메시지 컨벤션
* ✨ [FEAT] : 새로운 기능 구현
* 🛠 [FIX] : 버그 수정
* 🖋 [UPDATE]: 코드 수정, 내부 파일 수정
* ➕ [ADD] : FEAT 이외의 부수적인 코드 추가, 새로운 파일 추가
* 📜 [DOCS] : 주석 수정, 출력 메시지 수정 등 간단한 문서 수정
* 🎨 [DESIGN] : CSS 등 사용자 UI 디자인 변경
* 🧱 [REFACTOR] : 코드 리팩토링
* 💬 [ETC] : 파일명, 폴더명 수정 OR 파일, 폴더 삭제 OR 디렉터리 구조 변경

## 예시 페이지
### Main
![image](https://user-images.githubusercontent.com/87005840/159621075-2e450951-5826-48cb-aaa2-03c2028074b2.png)
### 묻고답하기
#### 묻고답하기 게시글 목록
![qna게시글목록](https://user-images.githubusercontent.com/87005840/159621142-df8dc50c-8c44-45f2-af97-cfdc8e1128c5.png)
#### 묻고답하기 게시글 작성
![qna게시글생성](https://user-images.githubusercontent.com/87005840/159621148-16636b34-0f14-4108-a321-b03aab35d023.png)
#### 묻고답하기 게시글 디테일 화면
![qna게시글디테일](https://user-images.githubusercontent.com/87005840/159621150-5b6f7370-8e3e-4a91-8d51-4a7d5e5c69b0.png)
### 그룹
#### 그룹 정보
![그룹디테일](https://user-images.githubusercontent.com/87005840/159621181-5b6b530c-0fab-4539-8a1e-2f213afc6c07.png)
#### 그룹 게시글 목록
![그룹게시글목록](https://user-images.githubusercontent.com/87005840/159621211-681a0600-524b-4d81-af03-5cb6e19b2578.png)
#### 그룹 게시글 디테일
![그룹게시글디테일](https://user-images.githubusercontent.com/87005840/159621213-36aa00c8-5bcd-4cf7-a8a9-bc57f7380d26.png)
### 마이페이지
![마이페이지](https://user-images.githubusercontent.com/87005840/159621228-ad846609-38ef-4283-9bca-4819e45c0642.JPG)
#### 알림 확인
![알림](https://user-images.githubusercontent.com/87005840/159621237-3b1e8911-386b-481f-8d50-918350978f95.JPG)



## Tools
* Python/Django
* HTML/CSS/JavaScript
* AWS EC2(Ubuntu)
* AWS RDS(MySQL)
* Notion
* Slack
* Figma
* Zoom
* Gather
* GitKraken

## 도와줘, 코딩을 만든 사람들
### 말랑한 사람들이 모여 말랑한 서비스를 만듭니다.
#### 홍성윤
```
- 도와줘, 코딩 팀장
- 기획
- 데이터베이스 설계
- 백엔드 개발
- 묻고 답하기 게시판, 그룹 커뮤니티 게시판 구현
- AWS 배포
```

#### 길은지
```
- 기획
- 데이터베이스 설계
- 프론트엔드, 백엔드 개발
- 묻고 답하기 게시판, 그룹 커뮤니티 게시판 구현
```

#### 박찬영
```
- 기획
- 데이터베이스 설계
- 백엔드 개발
- user app 구현(회원가입, 로그인, 업적, 알림 기능)
```

#### 권윤
```
- 기획
- 데이터베이스 설계
- 디자인
- 프론트엔드 개발
- 메인 화면 구현
```

#### 박예준
```
- 기획
- 데이터베이스 설계
- 백엔드 개발
- group app 구현(그룹 생성/가입/탈퇴/좋아요/찜하기 기능)
```

## Contact Us
helpcoding22@gmail.com

hsy0113@korea.ac.kr

![share_thumbnail](https://user-images.githubusercontent.com/87005840/159621569-3d5bee8f-bb3e-4e92-bbbd-6167800feca5.png)
