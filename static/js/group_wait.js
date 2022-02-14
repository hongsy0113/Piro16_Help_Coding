const showGroupWaitBtn = document.querySelector('.group__wait--btn');
const closeGroupWaitBtn = document.querySelector('.group__wait--close');
const groupWaitAlert = document.querySelector('.group__member--all');


function closeGroupWait() {
    groupWaitAlert.style.display = 'none';
}

if(showGroupWaitBtn) {
    showGroupWaitBtn.addEventListener('click', function() {
        console.log('!')
        groupWaitAlert.style.display='block'
        onClickGroupWait(group_id);
    })
}

const onClickGroupWait = async(id) => {
    const url = '/group/wait_list_ajax/';
    const { data } = await axios.post(url, {
        id
    });
    console.log("@@")
    groupWaitHandleResponse(
        data.groupName,
        data.waits,
    );
}

const groupWaitHandleResponse = (groupName, waits) => {
    const groupWaitName = document.querySelector('.group__wait-name');
    const groupWaitAlertText = document.querySelector('.group__wait--member-list');
    console.log("!")
    groupWaitName.innerHTML = `<h2>${groupName}</h2>`;

    groupWaitAlertText.innerHTML = `
    <form method="GET" class="group-wait__one d-flex flex-row">
        <div class="d-flex flex-row align-items-center">
            <img src="${ waits.img }" height="50" width="50" style="border-radius: 50px;"/>
            <h6>${ waits.nickname }</h6>
            <input type="submit" value="수락" name="accept">
            <input type="submit" value="거절" name="reject">
        </div>  
    </form>
    `;
    
    groupWaitAlert.style.display = 'block';
}