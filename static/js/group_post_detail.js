// qna 게시판 디테일 화면과 관련된 js
// template에서 data 가져오기
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const post_id = JSON.parse(document.getElementById('post_id').textContent);

/////////////////////////////////////////////////////
////////////////////답변 작성 ///////////////////////
/////////////////////////////////////////////////////
const onClickAnswer = async (postId, content) => {
    const url = "/group/answer_ajax/";
    // 입력을 하지 않았다면 작성 버튼 눌러도 작동 안하도록
    if (content.length>0){
        const {data} = await axios.post(url,{
            postId, content, user: user_id
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
    newAnswer.innerHTML = `
        <div class="answer__content-container answer__content-container--${id}">
            <h2>${user}</h2>
            <p>${created_at}</p>
            <div>
                <span>(작성자)</span>
                <p class="answer__content answer__content--${id}">${content}</p>
                <div class="answer__like-btn answer__like-btn--${id} btn"  id="answer-like-${id}" >
                    <i class="far fa-heart"></i>
                    <span>좋아요 0개</span>
                </div>
            </div>
            <div>
                <button class="btn btn-secondary answer__edit-btn answer__edit-btn--${id} " id="answer-edit-btn-${id}">답변 수정</button>
                <button class="btn btn-secondary answer__delete-btn answer__delete-btn--${id}" id="answer-delete-btn-${id}">답변 삭제</button>
            </div>
            <div>
                <input type="checkbox" class="answer__write-reply answer__write-reply--${id} btn-check" id="reply-btn-${id}" autocomplete="off"">
                <label class="btn btn-primary" for="reply-btn-${id}">답글 작성</label>
            </div>
            <h6>대댓글</h4>
            <hr>
            <div class="reply__list reply__list--${id}"></div>
            <div class="reply__form reply__form--${id}" style="display: none;">
                <input type="text" name="new_reply_${id}" placeholder="답변을 입력하세요" class="reply__input reply__input--${id}" id = "reply-input-${id}"style="width:200px; height:20px;">    
                <input type="button" value = "작성" class="reply__submit reply__submit--${id}" id ="reply-submit-${id}">
            </div>
        </div>
        <div class="answer__edit answer__edit--${id}" style="display: none;">
            <input type="text" name="edit_answer_${id}" class="answer__edit-input answer__edit-input--${id}" id = "answer-edit-input-${id}" style="width:200px; height:20px;" value="${content}">    
            <input type="button" value = "수정" class="answer__edit-submit answer__edit-submit--${id}" id = "answer-edit-submit-${id}">
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
        onClickAnswerDelete(id);
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

answerButton.addEventListener('click', function(){onClickAnswer(post_id , answerInput.value)});
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
replyButtons.forEach(function(btn) {
    btn.addEventListener('click',function(e){
        // button class 이름에서 해당 대댓글 작성 버튼이 속한 답변 id 가져오기
        const btnElementId = btn.getAttribute('id').split('-');
        const answerId = btnElementId[btnElementId.length-1];
        onClickReplyCheck(e, answerId);
    })
})

const onClickReply = async (answerId) => {
    const url = "/group/reply_ajax/";
    
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
    newReply.classList.add('reply__container', `reply__container--${replyId}`, `answer__container--${replyId}`)
    newReply.innerHTML = `
        <div class="answer__content-container answer__content-container--${replyId}">
            <p>
            ${user}   ${created_at}
            <br>
            <span>(작성자)</span>
            <p class= "answer__content answer__content--${replyId}"> ${content}</p>
            <br>
            <div class="answer__like-btn answer__like-btn--${replyId} btn"  id="answer-like-${replyId}" >
            <i class="far fa-heart"></i>
            <span>좋아요 0개</span>
            </div>
            </p>
            <div>
                <button class="btn btn-sm btn-secondary answer__edit-btn answer__edit-btn--${replyId} " id="answer-edit-btn-${replyId}">답변 수정</button>
                <button class="btn btn-sm btn-secondary answer__delete-btn answer__delete-btn--${replyId} " id="answer-delete-btn-${replyId}">답변 삭제</button>
            </div>
        </div>
        <div class="answer__edit answer__edit--${replyId}" style=" display: none;">
            <input type="text" name="edit_answer_${replyId}" class="answer__edit-input answer__edit-input--${replyId}" id = "answer-edit-input-${replyId}" 
            style="width:200px; height:20px;" value="${content}">    
            <input type="button" value = "수정" class="answer__edit-submit answer__edit-submit--${replyId}" id = "answer-edit-submit-${replyId}">
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
        onClickAnswerDelete(replyId);
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

const postLikeBtn = document.querySelector('.post__like-btn');

onClickPostLike = async (postId) => {
    const url = "/group/post_like_ajax/";
    const {data} = await axios.post(url,{
        postId
    });
    postLikeHandleResponse(data.post_id, data.total_likes, data.is_liking)
    
}

postLikeBtn.addEventListener('click', function(){
    onClickPostLike(post_id);
})

postLikeHandleResponse = (postId, totalLikes, isLiking) => {
    if (isLiking){
        postLikeBtn.innerHTML = `
        <i class="fas fa-heart"></i>
        <span>좋아요 ${totalLikes}개</span>
        `
    }
    else {
        postLikeBtn.innerHTML = `
        <i class="far fa-heart"></i>
        <span>좋아요 ${totalLikes}개</span>
        `
    }
}

/// 댓글 좋아요
const onClickAnswerLike = async (id) => {
    const url = "/group/answer_like_ajax/";
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
    const url = "/group/answer_delete_ajax/";
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
    const url = "/group/answer_edit_ajax/";
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
    const url = '/group/answer_edit_submit_ajax/'

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
}

//////////////////////////////////////////
//// iframe fullscreen

const iframeFullscreenButton = document.querySelector('.iframe__fullscreen');

iframeFullscreenButton.addEventListener('click', function() {
    onClickIframeFullscreen();
})

const onClickIframeFullscreen =() => {
    const iframeContainer = document.querySelector('.iframe__container');
    console.log(iframeContainer)
    const smallScreenButton = document.createElement('button');
    smallScreenButton.innerHTML = '작은 화면으로';
    //iframeContainer.appendChild(smallScreenButton);
    // smallScreenButton.addEventListener('click', function() {

    // })

    
    document.querySelector("header").style.display = "none";
    document.querySelector("section").style.display = "none";
    
    iframeContainer.style.display ='block'
    iframeContainer.style.position = 'fixed';
    iframeContainer.style.width ='90%'
    iframeContainer.style.height ='90%'
    

    document.body.append(iframeContainer);
    iframeContainer.append(smallScreenButton);
    smallScreenButton.style.display='block';
    const iframe = iframeContainer.firstElementChild;
    iframe.setAttribute('width', '100%');
    iframe.setAttribute('height', '150%');
    //iframe.style.width='100% !important';
    //iframe.style.height ='100% !important'
    iframe.style.postion = 'absolute'
    console.log(body)
    console.log(iframe)
}

const fullscreen = element => {
    if (element.requestFullscreen) return element.requestFullscreen()
    if (element.webkitRequestFullscreen) return element.webkitRequestFullscreen()
    if (element.mozRequestFullScreen) return element.mozRequestFullScreen()
    if (element.msRequestFullscreen) return element.msRequestFullscreen()
  }

// iframeFullscreenButton.addEventListener('click', e => {
//     fullscreen(document.querySelector('.iframe__container'));
// })