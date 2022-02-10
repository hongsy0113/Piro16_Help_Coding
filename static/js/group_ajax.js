const user_id = JSON.parse(document.getElementById('user_id').textContent);
const group_id = JSON.parse(document.getElementById('group_id').textContent);

/////////////////// Ajax //////////////////////

// 나의 그룹 찜 기능 ajax
const onClickStar = async (id) => {
    const url = '/group/star_ajax/';
    const {data} = await axios.post(url, {
        id
    });
    starHandleResponse(data.id, data.is_star);
};

const starButton = document.querySelectorAll('.group__keyword-star');
starButton.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const [txt1, txt2, groupId] = btn.getAttribute('id').split('-');
        // const groupStar = document.querySelector(`.group__keyword-star--${groupId}`);

        onClickStar(groupId);
    })
}) 

const starHandleResponse = (groupId, is_star) => {
    const groupStar = document.querySelector(`.group__keyword-star--${groupId}`);

    if(is_star) {
        groupStar.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="none" d="M0 0h24v24H0z"/><path d="M12 18.26l-7.053 3.948 1.575-7.928L.587 8.792l8.027-.952L12 .5l3.386 7.34 8.027.952-5.935 5.488 1.575 7.928z"/></svg>`;
    } else {
        groupStar.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="none" d="M0 0h24v24H0z"/><path d="M12 18.26l-7.053 3.948 1.575-7.928L.587 8.792l8.027-.952L12 .5l3.386 7.34 8.027.952-5.935 5.488 1.575 7.928L12 18.26zm0-2.292l4.247 2.377-.949-4.773 3.573-3.305-4.833-.573L12 5.275l-2.038 4.42-4.833.572 3.573 3.305-.949 4.773L12 15.968z"/></svg>`;
    }
};


// 공개 그룹 좋아요 ajax
const heartBtn = document.getElementById('all-group__heart');

onClickLike = async(groupId) => {
    const url = '/group/interest_ajax/';
    const {data} = await axios.post(url,{
        groupId
    });
    likeHandleResponse(data.groupId, data.total_likes, data.is_liked);
}

heartBtn.addEventListener('click', function(){
    onClickLike(group_id);
})

likeHandleResponse = (groupId, total_likes, is_liked) => {

    if (is_liked){
        heartBtn.innerHTML = `
        <i class="fas fa-heart"></i>
        <span>좋아요 ${total_likes}개</span>
        `
    }
    else {
        heartBtn.innerHTML = `
        <i class="far fa-heart"></i>
        <span>좋아요 ${total_likes}개</span>
        `
    }
};


////////////////////// Modal ////////////////////////

// 초대 코드 모달 구현
const createCodeBtn = document.querySelector('.group__code--btn');
const closeCodeBtn = document.querySelector('.group__code--close');
const groupJoinBtn = document.querySelector('.group-join__btn');
const closeJoinBtn = document.querySelector('.group-join__close');

function showCreateCode() {
    const createCodeAlert = document.getElementById('create-code');
    createCodeAlert.style.display = 'block';
}

function closeCreateCode() {
    const createCodeAlert = document.getElementById('create-code');
    createCodeAlert.style.display = 'none';
}

function showGroupJoin() {
    const groupJoinAlert = document.getElementById('join-group');
    groupJoinAlert.style.display = 'block';
}

function closeGroupJoin() {
    const closeJoinAlert = document.getElementById('join-group');
    closeJoinAlert.style.display = 'none';
}

createCodeBtn.addEventListener('click', function() {
    createCode();
})

closeCodeBtn.addEventListener('click', closeCode);

// 그룹 초대코드 생성
const onClickCode = async(id) => {
    const url ='/group/create_code/';
    const { data } = await axios.get(url, {
        id
    });
    codeHandleResponse(data.id, data.code, data.name);

};

createCodeBtn.addEventListener('click', function() {
    onClickCode(group_id);
});

codeHandleResponse = (groupId, code, name) => {
    const codeBox = document.querySelector('.code_box');
    codeBox.innerHTML = `
    <h3>그룹명: ${ name }</h3>
    <h3>다음 코드로 친구를 초대하세요!</h3>
    <h1>${ code }</h1>
    `
};