// qna 게시판 디테일 화면과 관련된 js
// template에서 data 가져오기
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const question_id = JSON.parse(document.getElementById('question_id').textContent);

/////////////////////////////////////////////////////
////////////////////답변 작성 ///////////////////////
/////////////////////////////////////////////////////
const onClickAnswer = async (questionId, content) => {
    const url = "/qna/answer_ajax/";
    // 입력을 하지 않았다면 작성 버튼 눌러도 작동 안하도록
    if (content.length>0){
        const {data} = await axios.post(url,{
            questionId, content, user: user_id
        });
        answerHandleResponse(data.id, data.content, data.user, data.created_at)
    } 
}

const answerHandleResponse = (id, content, user, created_at) => {
    
    const element = document.querySelector(`.answer__input`);
    const answerList = document.querySelector(`.answer__list`);
    
    // input 비우기
    element.value = "";

    const newAnswer = document.createElement('div');
    newAnswer.classList.add('answer__container', `answer__container--${id}`)
    newAnswer.innerHTML = `<h2>${user}</h2>
            <p>${created_at}</p>
            <div>
                <p>${content}</p>
                <p>좋아요 0 </p>
            </div>`;
    answerList.append(newAnswer);

    //////////////////////////////////////////////////////////
    //TODO : 댓글 ajax 로 달릴 때 . 답변 추가 버튼도 달리도록


    // TODO : 총 답변 개수도 바뀌어야 함 (complete )
    const answerCount = document.querySelector('.answer__total-count');
    const [text1 , num, text2] = answerCount.innerHTML.split(' ');
    
    const count = Number(num)+1;

    answerCount.innerHTML = `답변 ${count} 개`
}

const answerButton = document.querySelector('.answer__submit');
const answerInput = document.querySelector('.answer__input');
// 익명 함수를 통해 addEvent 호출 함수에 파라미터를 넣을 수 있다.

answerButton.addEventListener('click', function(){onClickAnswer(question_id , answerInput.value)});
/////////////////////////////////////////////////////

/////////////////////////////////////////////////////
///////////////////대댓글 작성 ///////////////////////
/////////////////////////////////////////////////////

// 답변 작성 누르면 대댓글 작성폼 나오도록
const replyButton = document.querySelectorAll('.answer__write-reply');

const onClickReplyCheck = function (e, answerId) {
    const replyForm = document.querySelector(`.reply__form--${answerId}`);
    if (e.target.checked) {
        replyForm.style.display = 'block';
    }
    else {
        replyForm.style.display = 'none';
    }
}

replyButton.forEach(function(btn) {
    btn.addEventListener('click',function(e){
        // button class 이름에서 해당 대댓글 작성 버튼이 속한 답변 id 가져오기
        const [text1 , text2, answerId] = btn.getAttribute('id').split('-');
        onClickReplyCheck(e, answerId);
    })
})

const onClickReply = async (answerId, content) => {
    const url = "/qna/reply_ajax/";
    // 입력을 하지 않았다면 작성 버튼 눌러도 작동 안하도록
    if (content.length>0){
        const {data} = await axios.post(url,{
            answerId, content, user: 'user_id'
        });
        relpyHandleResponse()
    } 
}

// 같은 클래스 여러 요소에 같은 event 등록
const replySubmitButton = document.querySelectorAll('.reply__submit');
replySubmitButton.forEach(function(btn) {
    btn.addEventListener('click',function(){
        // button class 이름에서 해당 대댓글 작성 버튼이 속한 답변 id 가져오기
        const [text1 , text2, answerId] = btn.getAttribute('id').split('-');
        // 그걸 바탕으로 해당하는 대댓글 입력 받아오기
        const replyInput = document.querySelector(`.reply__input--${answerId}`);
        
        onClickReply(answerId, replyInput.value);
    })
})

/////////////////////////////////////////////////////