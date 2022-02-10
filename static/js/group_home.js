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
        groupStar.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="33" height="33" viewBox="0 0 33 33" fill="none"><path d="M14.2841 1.9274L14.284 1.92759L10.7818 9.44224L2.95814 10.6493C1.06844 10.9394 0.387624 13.3429 1.69516 14.6904C1.69521 14.6905 1.69526 14.6905 1.6953 14.6906L7.37193 20.5445L6.02817 28.821L6.02812 28.8213C5.72253 30.7113 7.63006 32.2674 9.33438 31.3119C9.33462 31.3118 9.33486 31.3117 9.33509 31.3115L16.3261 27.4227L23.3185 31.3124C23.3186 31.3124 23.3186 31.3124 23.3186 31.3124C25.0196 32.2589 26.9302 30.7151 26.624 28.8213L26.6239 28.821L25.2802 20.5446L30.9568 14.6906C32.2645 13.3431 31.5837 10.9394 29.694 10.6493L21.8703 9.44224L18.3681 1.92759L18.3677 1.92669C17.5428 0.165947 15.1196 0.136632 14.2841 1.9274Z" fill="#FFD76F" stroke="#828282"/></svg>`;
    } else {
        groupStar.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="33" height="33" viewBox="0 0 33 33" fill="none"><path d="M14.515 1.92759L14.5151 1.9274C15.3505 0.136631 17.7738 0.165947 18.5986 1.92669L18.5991 1.92759L22.1012 9.44224L29.9249 10.6493L29.9253 10.6494L29.8491 11.1435C31.2995 11.3662 31.8808 13.2585 30.829 14.3424L14.515 1.92759ZM14.515 1.92759L11.0128 9.44224L3.1891 10.6493C3.18901 10.6493 3.18893 10.6494 3.18884 10.6494C3.1888 10.6494 3.18875 10.6494 3.18871 10.6494C1.29931 10.9397 0.618669 13.343 1.92612 14.6904C1.92617 14.6905 1.92621 14.6905 1.92626 14.6906L7.60289 20.5446L6.25913 28.821L6.25907 28.8213C5.95349 30.7113 7.86102 32.2674 9.56534 31.3119C9.56557 31.3118 9.56581 31.3117 9.56605 31.3115L16.557 27.4227L23.5495 31.3124C25.2505 32.259 27.1611 30.7151 26.855 28.8213L26.8549 28.821L25.5111 20.5445L31.1878 14.6906L14.515 1.92759Z" stroke="white"/></svg>`;
    }
};

// 초대 코드 입력 창 
const groupJoinBtn = document.querySelector('.right__joinbtn');
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