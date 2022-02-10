const user_id = JSON.parse(document.getElementById('user_id').textContent);
const group_id = JSON.parse(document.getElementById('group_id').textContent);

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

// 초대 코드 입력 창 
const groupJoinBtn = document.querySelector('.group-join__btn');
const closeJoinBtn = document.querySelector('.group-join__close');

function showGroupJoin() {
    const groupJoinAlert = document.getElementById('join-group');
    groupJoinAlert.style.display = 'block';
}

function closeGroupJoin() {
    const closeJoinAlert = document.getElementById('join-group');
    closeJoinAlert.style.display = 'none';
}

// groupJoinBtn.addEventListener('click', showGroupJoin);
// closeJoinBtn.addEventListener('click', closeGroupJoin);

// 초대 코드 입력 Modal 
const groupCodeSubmitButton = document.querySelector('.group-code__submit');
const groupCodeInput = document.querySelector('.group-code__input');

groupCodeSubmitButton.addEventListener('click', function() {
    onClickGroupCodeSubmit(groupCodeInput.value);
});

const onClickGroupCodeSubmit = async(code) => {
    const url = '/group/join_code_ajax/';
    const { data } = await axios.post(url, {
        code
    });

    groupCodeHandleResponse(data.message);
}

const groupCodeHandleResponse = (message) => {
    const groupCodeAlert = document.querySelector('.group-join__alert-box');
    const groupCodeAlertText = document.querySelector('.group-code__text');
    
    groupCodeAlertText.innerHTML = message;
    groupCodeAlert.style.display = 'block';
}