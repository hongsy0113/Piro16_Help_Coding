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
                <div class="answer__like-btn answer__like-btn--${id} btn"  id="answer-like-${id}"  onclick="onClickAnswerLike(${id})">
                        <i class="far fa-heart"></i>
                        <span>좋아요 0개</span>
                </div>
            </div>
            <div>
                    <input type="checkbox" class="answer__write-reply answer__write-reply--${id} btn-check" id="reply-btn-${id}" autocomplete="off" onclick="onClickReplyCheck(event,${id})">
                    <label class="btn btn-primary" for="reply-btn-${id}">답글 작성</label>
            </div>
            <h6>대댓글</h4>
            <hr>
            <div class="reply__list reply__list--${id}"></div>
            <div class="reply__form reply__form--${id}" style="display: none;">
                <input type="text" name="new_reply_${id}" placeholder="답변을 입력하세요" class="reply__input reply__input--${id}" id = "reply-input-${id}"style="width:200px; height:20px;">    
                <input type="button" value = "작성" class="reply__submit reply__submit--${id}" id = "reply-submit-${id}" onclick="onClickReply(${id})">
            </div>
            `;
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
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        onClickReplyCheck(e, answerId);
    })
})

const onClickReply = async (answerId) => {
    const url = "/qna/reply_ajax/";
    
    const content = document.querySelector(`#reply-input-${answerId}`).value;
    // 입력을 하지 않았다면 작성 버튼 눌러도 작동 안하도록
    if (content.length>0){
        const {data} = await axios.post(url,{
            answerId, content, user: user_id
        });
        relpyHandleResponse(
            data.reply_id, 
            data.answer_id,
            data.content,
            data.user,
            data.created_at,
        )
    } 
}

relpyHandleResponse = (replyId, answerId ,content, user, created_at) => {
    
    const element = document.querySelector(`.reply__input--${answerId}`);
    const replyList = document.querySelector(`.reply__list--${answerId}`);
    
    // input 비우기
    element.value = "";

    const newReply = document.createElement('div');
    newReply.classList.add('reply__container', `reply__container--${replyId}`)
    newReply.innerHTML = `<p>
        ${user}   ${created_at}
        <br>
        ${content}
        <br>
        <div class="answer__like-btn answer__like-btn--${replyId} btn"  id="answer-like-${replyId}"  onclick="onClickAnswerLike(${replyId})">
        <i class="far fa-heart"></i>
        <span>좋아요 0개</span>
        </div>
        </p>`;

    replyList.append(newReply);
}


// 같은 클래스 여러 요소에 같은 event 등록
const replySubmitButton = document.querySelectorAll('.reply__submit');
replySubmitButton.forEach(function(btn) {
    btn.addEventListener('click',function(){
        // button class 이름에서 해당 대댓글 작성 버튼이 속한 답변 id 가져오기
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        onClickReply(answerId);
    })
})

/////////////////////////////////////////////////////

/////////////////////////////////////////////////////
////////////////// 좋아요 ajax //////////////////////
/////////////////////////////////////////////////////

const questionLikeBtn = document.querySelector('.question__like-btn');

onClickQuestionLike = async (questionId) => {
    const url = "/qna/question_like_ajax/";
    const {data} = await axios.post(url,{
        questionId
    });
    questionLikeHandleResponse(data.question_id, data.total_likes, data.is_liking)
    
}

questionLikeBtn.addEventListener('click', function(){
    onClickQuestionLike(question_id);
})

questionLikeHandleResponse = (questionId, totalLikes, isLiking) => {
    if (isLiking){
        questionLikeBtn.innerHTML = `
        <i class="fas fa-heart"></i>
        <span>좋아요 ${totalLikes}개</span>
        `
    }
    else {
        questionLikeBtn.innerHTML = `
        <i class="far fa-heart"></i>
        <span>좋아요 ${totalLikes}개</span>
        `
    }
}
///
const onClickAnswerLike = async (id) => {
    const url = "/qna/answer_like_ajax/";
    const {data} = await axios.post(url,{
        id
    });
    answerLikeHandleResponse(data.answer_id, data.total_likes, data.is_liking)
}
// 같은 클래스 여러 요소에 같은 event 등록
const answerLikeButtons = document.querySelectorAll('.answer__like-btn');
answerLikeButtons.forEach(function(btn) {
    btn.addEventListener('click',function(){
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        
        onClickAnswerLike(answerId);
    })
})

answerLikeHandleResponse = (answerId, totalLikes, isLiking) => {
    const answerLikeBtn = document.querySelector(`.answer__like-btn--${answerId}`)

    if (isLiking){
        answerLikeBtn.innerHTML = `
        <i class="fas fa-heart"></i>
        <span>좋아요 ${totalLikes}개</span>
        `
    }
    else {
        answerLikeBtn.innerHTML = `
        <i class="far fa-heart"></i>
        <span>좋아요 ${totalLikes}개</span>
        `
    }
}

//------------댓글 삭제 -----------//
const answerDeleteButtons = document.querySelectorAll('.answer__delete-btn');
answerDeleteButtons.forEach(function(btn) {
    btn.addEventListener('click',function(){
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        onClickAnswerDelete(answerId);
    })
})

const onClickAnswerDelete = async (id) => {
    const url = "/qna/answer_delete_ajax/";
    const {data} = await axios.post(url,{
        id
    });
    answerDeleteHandleResponse(data.id)
}

answerDeleteHandleResponse = (answerId) => {
    const answerContainer = document.querySelector(`.answer__container--${answerId}`)

    // 답변 개수도 바뀌어야함
    // 대댓글, 답변 다 한 함수로 통일 했으므로 조건 나눠줘야 한다.
    if (!answerContainer.classList.contains('reply__container')){
        const answerCount = document.querySelector('.answer__total-count');
        const [text1 , num, text2] = answerCount.innerHTML.split(' ');
    
        const count = Number(num)-1;

        answerCount.innerHTML = `답변 ${count} 개`
    }
    answerContainer.remove();
}
//---------------------------------//

//------------댓글 수정 -----------//
///일단 먼저 댓글 수정 클릭하면 form 뜨는 거 부터 하자
//// 그 다음에 동적 요소 이벤트 바인딩

////// 1.  댓글 수정 클릭하면 해당 form ajax로 나오게 
const answerEditButtons = document.querySelectorAll('.answer__edit-btn');
answerEditButtons.forEach(function(btn) {
    btn.addEventListener('click',function(){
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        onClickAnswerEdit(answerId);
    })
})

const onClickAnswerEdit = async (id) => {
    const url = "/qna/answer_edit_ajax/";
    const {data} = await axios.post(url,{
        id
    });
    answerEditHandleResponse(data.id, data.content)
}
answerEditHandleResponse = (answerId, content) => {
    const answerContainer = document.querySelector(`.answer__content-container--${answerId}`);
    answerContainer.style.display = 'none';

    const answerEditForm = document.querySelector(`.answer__edit--${answerId}`);
    answerEditForm.style.display = 'block';
}

////// 2.  해당 폼에서 수정 클릭하면 ajax로 댓글 수정
const answerEditSubmitButtons = document.querySelectorAll('.answer__edit-submit');
answerEditSubmitButtons.forEach(function(btn) {
    btn.addEventListener('click',function(){
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        onClickAnswerEditSubmit(answerId);
    })
})

const onClickAnswerEditSubmit = async(id) => {
    const url = '/qna/answer_edit_submit_ajax/'

    const content = document.querySelector(`#answer-edit-input-${id}`).value;
    const {data} = await axios.post(url,{
        id, content
    });
    answerEditSubmitHandleResponse(data.id, data.content)
}
answerEditSubmitHandleResponse = (answerId, content) => {
    const answerContainer = document.querySelector(`.answer__content-container--${answerId}`);
    answerContainer.style.display = 'block';

    const answerContent = document.querySelector(`.answer__content--${answerId}`);
    answerContent.innerHTML = content;
    
    const answerEditForm = document.querySelector(`.answer__edit--${answerId}`);
    answerEditForm.style.display = 'none';
    console.dir(answerEditForm);
}