const user_id = JSON.parse(document.getElementById('user_id').textContent);
const group_id = JSON.parse(document.getElementById('group_id').textContent);

// 나의 그룹 찜 기능 ajax
const onClickStar = async (id) => {
    const url = '/group/group_star_ajax/';
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
        groupStar.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="33" height="33" viewBox="0 0 33 33" fill="none">
        <path d="M14.2841 1.9274L14.284 1.92759L10.7818 9.44224L2.95814 10.6493C1.06844 10.9394 0.387624 13.3429 1.69516 14.6904C1.69521 14.6905 1.69526 14.6905 1.6953 14.6906L7.37193 20.5445L6.02817 28.821L6.02812 28.8213C5.72253 30.7113 7.63006 32.2674 9.33438 31.3119C9.33462 31.3118 9.33486 31.3117 9.33509 31.3115L16.3261 27.4227L23.3185 31.3124C23.3186 31.3124 23.3186 31.3124 23.3186 31.3124C25.0196 32.2589 26.9302 30.7151 26.624 28.8213L26.6239 28.821L25.2802 20.5446L30.9568 14.6906C32.2645 13.3431 31.5837 10.9394 29.694 10.6493L21.8703 9.44224L18.3681 1.92759L18.3677 1.92669C17.5428 0.165947 15.1196 0.136632 14.2841 1.9274Z" fill="#FFD76F" stroke="#828282"/>
        </svg>
        <span>그룹 찜하기</span>
        `;
    } else {
        groupStar.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="33" height="33" viewBox="0 0 33 33" fill="none">
        <path d="M14.515 1.92759L14.5151 1.9274C15.3505 0.136631 17.7738 0.165947 18.5986 1.92669L18.5991 1.92759L22.1012 9.44224L29.9249 10.6493L29.9253 10.6494L29.8491 11.1435C31.2995 11.3662 31.8808 13.2585 30.829 14.3424L14.515 1.92759ZM14.515 1.92759L11.0128 9.44224L3.1891 10.6493C3.18901 10.6493 3.18893 10.6494 3.18884 10.6494C3.1888 10.6494 3.18875 10.6494 3.18871 10.6494C1.29931 10.9397 0.618669 13.343 1.92612 14.6904C1.92617 14.6905 1.92621 14.6905 1.92626 14.6906L7.60289 20.5446L6.25913 28.821L6.25907 28.8213C5.95349 30.7113 7.86102 32.2674 9.56534 31.3119C9.56557 31.3118 9.56581 31.3117 9.56605 31.3115L16.557 27.4227L23.5495 31.3124C25.2505 32.259 27.1611 30.7151 26.855 28.8213L26.8549 28.821L25.5111 20.5445L31.1878 14.6906L14.515 1.92759Z" stroke="white"/>
        </svg>
        <span>그룹 찜하기</span>
        `;
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

if(heartBtn) {
    heartBtn.addEventListener('click', function(){
        onClickLike(group_id);
    })
}

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

// 초대 코드 생성 창 & Modal
const createCodeBtn = document.querySelector('.group__code--btn');
const closeCodeBtn = document.querySelector('.group__code--close');

function closeCreateCode() {
    const createCodeAlert = document.getElementById('create-code');
    createCodeAlert.style.display = 'none';
}

if(createCodeBtn){
    createCodeBtn.addEventListener('click', function() {
        onClickCreateCode(group_id);
    })
}

const onClickCreateCode = async(groupId) => {
    const url = '/group/create_code_ajax/';
    const { data } = await axios.post(url, {
        groupId
    });
    createCodeHandleResonse(data.code, data.name);
}

const createCodeHandleResonse = (code, name) => {
    const createCodeAlert = document.getElementById('create-code');
    const createCodeAlertText = document.querySelector('.code_box');

    createCodeAlertText.innerHTML = `    
        <h1>${ code }</h1>
        <h2>이 코드를 공유하여 멤버를 초대하세요.</h2>
        <span>코드 유효 기간 : 7일</span>
    `;
    createCodeAlert.style.display = 'flex';
}

// 그룹 대기자 명단 modal
const showGroupWaitBtn = document.querySelector('.group__wait--btn');
const closeGroupWaitBtn = document.querySelector('.group__wait--close');
const groupWaitAlert = document.querySelector('.group__member--all');
var flag = 0;    // 명단에 대한 반복문이 한 번만 실행되기 위한 변수

function closeGroupWait() {
    groupWaitAlert.style.display = 'none';
}

if(showGroupWaitBtn) {
    showGroupWaitBtn.addEventListener('click', function() {
        onClickGroupWait(group_id);
    })
}

const onClickGroupWait = async(id) => {
    console.log(group_id) 
    const url = '/group/wait_list_ajax/';
    const { data } = await axios.post(url, {
        id
    });

    groupWaitHandleResponse(
        data.groupName,
        data.waitsName,
        data.waitsImg,
        data.waitsId
    );
}

const groupWaitHandleResponse = (groupName, waitsName, waitsImg, waitsId) => {
    const groupWaitName = document.querySelector('.group__wait-name');
    const groupWaitAlertText = document.querySelector('.group__wait--member-list');


    // groupWaitName.innerHTML = `<h4><b>${groupName}</b>의 대기자 명단</h4>`;

    for(var i=0; i<waitsName.length; i++){
        if(waitsImg[i]){
            waitImg = `<img src="${waitsImg[i]}" alt="" height="50" width="50" style="border-radius: 50px;">`;
        }

        waitMemberId = waitsId[i];

        if(flag==0){
            groupWaitAlertText.innerHTML += `
            <form method="GET" class="group-wait__one">
                <div class="wait-member__imgnname">
                    <div class="wait-member__img">
                        ${ waitImg }
                    </div>  
                    <span class="wait-member__name"><a href="{% url 'group:wait_member_detail' waitMemberId %}">${ waitsName[i] }</a></span>  
                </div>          
                <div class="wait__text--${ waitMemberId } wait-member__text"><span>가입을 기다리고 있어요!<span></div>
                <div class="wait-member__btnbox">
                    <input type="button" value="수락" name="accept" class="wait__accept--btn wait__accept--btn--${ waitMemberId } wait-accept__btn" id="accept-btn-${ waitMemberId }">
                    <input type="button" value="거절" name="reject" class="wait__reject--btn wait__reject--btn--${ waitMemberId } wait-reject__btn" id="reject-btn-${ waitMemberId }">
                </div>
            </form>
                            `;
        }

        // 수락, 거절 버튼 선택 이후
        // const waitAcceptBtn = document.querySelector(`.wait__accept--btn-${ waitMemberId }`);
        // const waitRejectBtn = document.querySelector(`.wait__reject--btn-${ waitMemberId }`);
        // const memberWaitAlertText = document.querySelector(`.wait__text--${ waitMemberId }`);

        // waitAcceptBtn.addEventListener('click', function(){
        //     onClickacceptWait(waitMemberId, group_id);
        // })
        // waitRejectBtn.addEventListener('click', function(){
        //     onClickrejectWait(waitMemberId, group_id);
        // })

    };
    flag = 1;
    
    groupWaitAlert.style.display = 'flex';

    const waitAcceptBtn = document.querySelectorAll('.wait__accept--btn');
    const waitRejectBtn = document.querySelectorAll('.wait__reject--btn');

    waitAcceptBtn.forEach(function(btn) {
        btn.addEventListener('click', function(){
            const [txt1, txt2, waitId] = btn.getAttribute('id').split('-');
            onClickacceptWait(waitId, group_id);
        })
    })

    waitRejectBtn.forEach(function(btn) {
        btn.addEventListener('click', function(){
            const [txt1, txt2, waitId] = btn.getAttribute('id').split('-');
            onClickrejectWait(waitId, group_id);
        })
    })

    const onClickacceptWait = async (userId, groupId) => {
        const url = "/group/group_join_accept/";
        const {data} = await axios.post(url, {
            userId, groupId
        });
        console.log('!')
        joinAcceptHandleResponse(
            data.userId
        )
    }

    joinAcceptHandleResponse = (userId) => {
        const memberWaitAlertText = document.querySelector(`.wait__text--${userId}`);

        memberWaitAlertText.innerHTML = '수락했습니다.'
    }


    const onClickrejectWait = async (userId, groupId) => {
        const url = "/group/group_join_reject/";
        const {data} = await axios.post(url, {
            userId, groupId
        });
        joinRejectHandleResponse(
            data.userId
        )
    }

    joinRejectHandleResponse = (userId) => {
        const memberWaitAlertText = document.querySelector(`.wait__text--${userId}`);

        memberWaitAlertText.innerHTML = '거절했습니다.'
    }
}

// alert(삭제 시, 탈퇴 시)
const groupOutBtn = document.querySelector('.btn-out');
groupOutBtn.addEventListener('click', function(){
    alert('탈퇴되었습니다.');
})

const groupDeleteBtn = document.querySelector('.btn__delete');
groupDeleteBtn.addEventListener('click', function(){
    alert('삭제되었습니다.');
})