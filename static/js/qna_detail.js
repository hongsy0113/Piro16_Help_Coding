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
        answerHandleResponse(data.id, data.content, data.user, data.created_at, data.user_image_url, data.is_author)
    } 
}

const answerHandleResponse = (id, content, user, created_at, img_url, is_author) => {
    
    const element = document.querySelector(`.answer__input`);
    const answerList = document.querySelector(`.answer__list`);
    
    // input 비우기
    element.value = "";
    // 프로필 이미지. 없으면 아무것도 안 들어가도록
    let userProfileImg ="";
    // 작성자 여부
    let isAuthorTag = "";

    if (img_url){
        userProfileImg = `<img src="${img_url}" alt="">`
    }
    if (is_author){
        isAuthorTag = "<span class='answer__writer-mark'>글쓴이</span>"
    }
    const newAnswer = document.createElement('div');
    newAnswer.classList.add('answer__container', `answer__container--${id}`)
    newAnswer.innerHTML = `
    <div class="answer__content-container answer__content-container--${id}">
        <div class="answer__user__profile">
            <div class="answer__user__profile-left">
                ${userProfileImg}
            </div>
            <div class="answer__user__profile-right">
                <div>
                    <div class="answer__user__name answer__user__name--${id}"> 
                        <h2>${user}</h2>
                        ${isAuthorTag}
                    </div>
                    <p>${created_at}</p>
                </div>
                <div>
                    <button class="answer__edit-btn answer__edit-btn--${id} " id="answer-edit-btn-${id}">수정</button>
                    <button class="answer__delete-btn answer__delete-btn--${id} " id="answer-delete-btn-${id}">삭제</button>
                </div>
            </div>
        </div>
        <p class="answer__content answer__content--${id}">${content}</p>
        <div class="answer__like__reply">
            <div>
                <input type="checkbox" class="answer__write-reply answer__write-reply--${id} btn-check " id="reply-btn-${id}" autocomplete="off">
                <label class="answer__reply-btn" for="reply-btn-${id}">답글 작성</label>
            </div>
            <div class="answer__like-btn answer__like-btn--${id}"  id="answer-like-${id}">
                <i class="far fa-heart"></i>
                <span>0</span>
            </div>
        </div>
    </div>
    <div class="answer__edit answer__edit--${id}" style=" display: none;">
        <div class="answer__edit__flexbox">
            <input type="text" name="edit_answer_${id}" class="answer__edit-input answer__edit-input--${id}" id = "answer-edit-input-${id}" style="width:200px; height:20px;" value="${content}">    
            <input type="button" value = "수정" class="answer__edit-submit answer__edit-submit--${id}" id = "answer-edit-submit-${id}">
        </div>
    </div>
    <div class="reply__list reply__list--${id}"></div>
    <div class="reply__form reply__form--${id}" style="display: none;">
        <div class="reply__form__flexbox">
            <input type="text" name="new_reply_${id}" placeholder="답변을 입력하세요" class="reply__input reply__input--${id}" id = "reply-input-${id}">    
            <input type="button" value = "작성" class="reply__submit reply__submit--${id}" id = "reply-submit-${id}">  
        </div>
    </div>
    
    `;

    answerList.append(newAnswer);

    /// 동적으로 생성된 요소들에 이벤트 바인딩
    const answerLikeButton = document.querySelector(`.answer__like-btn--${id}`);
    answerLikeButton.addEventListener('click',function(){
        onClickAnswerLike(id);
    })
    const answerDeleteButton = document.querySelector(`.answer__delete-btn--${id}`);
    answerDeleteButton.addEventListener('click',function(){
        if (confirm("정말 삭제하시겠습니까?")){
            onClickAnswerDelete(id);
        }
        else {
            return false
        }
    })
    const replyButton = document.querySelector(`.answer__write-reply--${id}`);
    replyButton.addEventListener('click',function(e){
        onClickReplyCheck(e, id);
    })
    const replySubmitButton = document.querySelector(`.reply__submit--${id}`);
    replySubmitButton.addEventListener('click',function(){
        onClickReply(id);
    })
    const answerEditButton = document.querySelector(`.answer__edit-btn--${id}`);
    answerEditButton.addEventListener('click',function(){
        onClickAnswerEdit(id);
    })
    const answerEditSubmitButton = document.querySelector(`.answer__edit-submit--${id}`);
    answerEditSubmitButton.addEventListener('click', function(){
        onClickAnswerEditSubmit(id);
    })
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

if (answerButton){
    answerButton.addEventListener('click', function(){onClickAnswer(question_id , answerInput.value)});
}

/////////////////////////////////////////////////////

/////////////////////////////////////////////////////
///////////////////대댓글 작성 ///////////////////////
/////////////////////////////////////////////////////

// 답변 작성 누르면 대댓글 작성폼 나오도록
const onClickReplyCheck = function (e, answerId) {
    const replyForm = document.querySelector(`.reply__form--${answerId}`);
    if (e.target.checked) {
        replyForm.style.display = 'block';
    }
    else {
        replyForm.style.display = 'none';
    }
}

const replyButtons = document.querySelectorAll('.answer__write-reply');

if (user_id){
    replyButtons.forEach(function(btn) {
        btn.addEventListener('click',function(e){
            // button class 이름에서 해당 대댓글 작성 버튼이 속한 답변 id 가져오기
            const btnElementId = btn.getAttribute('id').split('-');
            const answerId = btnElementId[btnElementId.length-1];
            onClickReplyCheck(e, answerId);
        })
    })
}


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
            data.user_image_url, 
            data.is_author,
        )
    } 
}

relpyHandleResponse = (replyId, answerId ,content, user, created_at, img_url, is_author ) => {
    
    const element = document.querySelector(`.reply__input--${answerId}`);
    const replyList = document.querySelector(`.reply__list--${answerId}`);
    
    // input 비우기
    element.value = "";

    let userProfileImg ="";
    // 작성자 여부
    let isAuthorTag = "";
    
    if (img_url){
        userProfileImg = `<img src="${img_url}" alt="">`
    }
    if (is_author){
        isAuthorTag = "<span class='answer__writer-mark'>글쓴이</span>"
    }

    const newReply = document.createElement('div');
    newReply.classList.add('reply__container', `reply__container--${replyId}`, `answer__container--${replyId}`)
    newReply.innerHTML = `
    <div class="answer__content-container answer__content-container--${replyId}">
        <div class="answer__user__profile">
            <div class="answer__user__profile-left">
                ${userProfileImg}
            </div>
            <div class="answer__user__profile-right">
                <div>
                    <div class="answer__user__profile-name">
                        <h2>${user}</h2>
                        ${isAuthorTag}
                    </div>
                    <p>${created_at}</p>
                </div>
                <div>
                    <button class="answer__edit-btn answer__edit-btn--${replyId} " id="answer-edit-btn-${replyId}">수정</button>
                    <button class="answer__delete-btn answer__delete-btn--${replyId} " id="answer-delete-btn-${replyId}">삭제</button>
                </div>
            </div>
        </div>
        <p class= "answer__content answer__content--${replyId}"> ${content}</p>
        <div class="answer__like-btn answer__like-btn--${replyId}" id="reply-like-${replyId}" style="align-self:flex-end">
            <i class="far fa-heart"></i>
            <span>0</span>
        </div>

    </div>
    <div class="answer__edit answer__edit--${replyId}" style=" display: none;">
        <div class="answer__edit__flexbox">
            <input type="text" name="edit_answer_${replyId}" class="answer__edit-input answer__edit-input--${replyId}" id = "answer-edit-input-${replyId}" 
            style="width:200px; height:20px;" value="${content}">    
            <input type="button" value = "수정" class="answer__edit-submit answer__edit-submit--${replyId}" id = "answer-edit-submit-${replyId}">
        </div>
    </div>
        `;

    replyList.append(newReply);


    /// 동적으로 생성된 요소들에 이벤트 바인딩
    const answerLikeButton = document.querySelector(`.answer__like-btn--${replyId}`);
    answerLikeButton.addEventListener('click',function(){
        onClickAnswerLike(replyId);
    })
    const answerDeleteButton = document.querySelector(`.answer__delete-btn--${replyId}`);
    answerDeleteButton.addEventListener('click',function(){
        if (confirm("정말 삭제하시겠습니까?")){
            onClickAnswerDelete(replyId);
        }
        else {
            return false
        }
    })
    const answerEditButton = document.querySelector(`.answer__edit-btn--${replyId}`);
    answerEditButton.addEventListener('click',function(){
        onClickAnswerEdit(replyId);
    })
    const answerEditSubmitButton = document.querySelector(`.answer__edit-submit--${replyId}`);
    answerEditSubmitButton.addEventListener('click', function(){
        onClickAnswerEditSubmit(replyId);
    })
}


// 같은 클래스 여러 요소에 같은 event 등록
const replySubmitButtons = document.querySelectorAll('.reply__submit');
replySubmitButtons.forEach(function(btn) {
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

if(user_id) {
    questionLikeBtn.addEventListener('click', function(){
        onClickQuestionLike(question_id);
    })
}


questionLikeHandleResponse = (questionId, totalLikes, isLiking) => {
    if (isLiking){
        questionLikeBtn.innerHTML = `
        <i class="fas fa-heart"></i>
        <span>${totalLikes}</span>
        `
    }
    else {
        questionLikeBtn.innerHTML = `
        <i class="far fa-heart"></i>
        <span>${totalLikes}</span>
        `
    }
    const questionInfo = document.querySelector('.question__info');
    const originHTML = questionInfo.innerHTML;
    const [createdAt, hitCount, currentTotalLikes, nickname] = originHTML.split(' · ');
    const [, num] = currentTotalLikes.split(' ');
    const newTotalLikes = Number(num) + (isLiking? 1 : -1);
    questionInfo.innerHTML = `${createdAt} · ${hitCount} · 좋아요 ${newTotalLikes} · ${nickname}`;
}
/// 댓글 좋아요
const onClickAnswerLike = async (id) => {
    const url = "/qna/answer_like_ajax/";
    const {data} = await axios.post(url,{
        id
    });
    answerLikeHandleResponse(data.answer_id, data.total_likes, data.is_liking)
}
// 같은 클래스 여러 요소에 같은 event 등록
const answerLikeButtons = document.querySelectorAll('.answer__like-btn');

if(user_id) {
    answerLikeButtons.forEach(function(btn) {
        btn.addEventListener('click',function(){
            const btnElementId = btn.getAttribute('id').split('-');
            const answerId = btnElementId[btnElementId.length-1];
            
            onClickAnswerLike(answerId);
        })
    })
}


answerLikeHandleResponse = (answerId, totalLikes, isLiking) => {
    const answerLikeBtn = document.querySelector(`.answer__like-btn--${answerId}`)

    if (isLiking){
        answerLikeBtn.innerHTML = `
        <i class="fas fa-heart"></i>
        <span>${totalLikes}</span>
        `
    }
    else {
        answerLikeBtn.innerHTML = `
        <i class="far fa-heart"></i>
        <span>${totalLikes}</span>
        `
    }
}

//------------댓글 삭제 -----------//
const answerDeleteButtons = document.querySelectorAll('.answer__delete-btn');
answerDeleteButtons.forEach(function(btn) {
    btn.addEventListener('click',function(){
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        if (confirm("정말 삭제하시겠습니까?")){
            onClickAnswerDelete(answerId);
        }
        else {
            return false
        }
        
    })
})

const onClickAnswerDelete = async (id) => {
    const url = "/qna/answer_delete_ajax/";
    const {data} = await axios.post(url,{
        id
    });
    answerDeleteHandleResponse(data.id, data.delete_yes, data.answer_count)
}

answerDeleteHandleResponse = (answerId, deleteYes, count) => {
    const answerContainer = document.querySelector(`.answer__container--${answerId}`)

    // 답변 개수도 바뀌어야함
    
    const answerCount = document.querySelector('.answer__total-count');

    answerCount.innerHTML = `답변 ${count} 개`

    if (deleteYes){
        answerContainer.remove();
    }
    else {
        const answeredUser = document.querySelector(`.answer__user__name--${answerId}`);
        answeredUser.innerHTML = '<h2>(알 수 없음)</h2>';
        
        const answerContent = document.querySelector(`.answer__content--${answerId}`);
        answerContent.innerHTML =  '삭제된 답변입니다.';

        const answerEditButton = document.querySelector(`.answer__edit-btn--${answerId}`);
        answerEditButton.remove();

        const answerDeleteButton = document.querySelector(`.answer__delete-btn--${answerId}`);
        answerDeleteButton.remove();
    }
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
    answerEditHandleResponse(data.id)
}
answerEditHandleResponse = (answerId) => {
    const answerContentContainer = document.querySelector(`.answer__content-container--${answerId}`);
    answerContentContainer.style.display = 'none';
    
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
    answerContainer.style.display = 'flex';

    const answerContent = document.querySelector(`.answer__content--${answerId}`);
    answerContent.innerHTML = content;
    
    const answerEditForm = document.querySelector(`.answer__edit--${answerId}`);
    answerEditForm.style.display = 'none';
}


////// 로그인 안 했으면 좋아요 시 alert 창 뜨게 하기
// user_id 의 null 여부로 구분하자

if (user_id == null){
    const questionLikeButton = document.querySelector('.question__like-btn');
    questionLikeButton.addEventListener('click',function(){
        alert('로그인 후 이용해주세요.')
    })


    const answerLikeButtons = document.querySelectorAll('.answer__like-btn');
    answerLikeButtons.forEach(function(btn) {
        btn.addEventListener('click',function(){
            alert('로그인 후 이용해주세요.')
        })
    })

    const answerReplyButtons = document.querySelectorAll('.answer__reply-btn');
    answerReplyButtons.forEach(function(btn) {
        btn.addEventListener('click',function(){
            alert('로그인 후 이용해주세요.')
        })
    })

    const answerContainer = document.querySelector('.answer__input__container');
    answerContainer.addEventListener('click',function(){
        alert('로그인 후 이용해주세요.')
        document.querySelector('.answer__input').blur();
    })
} 

///// 삭제 전 확인
const questionDeleteBtn = document.querySelector('.question__delete-btn--actual');
if (questionDeleteBtn){
    questionDeleteBtn.addEventListener('click',function(){
        if (confirm("정말 삭제하시겠습니까?")){
            document.location.href = `/qna/${question_id}/delete`;//onClickQuestionDelete(question_id);
        }
        else {
            return false
        }
    })
}
