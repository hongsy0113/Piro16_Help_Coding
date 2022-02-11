const showGroupWaitBtn = document.querySelector('.group__wait--btn');
const closeGroupWaitBtn = document.querySelector('.group__wait--close');

function closeGroupWait() {
    const groupWaitAlert = document.querySelector('.group__member--all');
    groupWaitAlert.style.display = 'block';
}

showGroupWaitBtn.addEventListener('click', function() {
    onClickGroupWait(group_id);
})

const onClickGroupWait = async(id) => {
    console.log('!')
    const url = '/group/wait_list_ajax/';
    const { data } = await axios.post(url, {
        id
    });
    groupWaitHandleResponse(
        data.groupName,
        data.waits,
        data.waits_img,
    );
}

const groupWaitHandleResponse = (groupName, waits, waits_img, members) => {
    const groupWaitName = document.querySelector('.group__wait-name');
    const groupWaitAlert = document.querySelector('.group__member--all');
    const groupWaitAlertText = document.querySelector('.group__wait--member-list');

    groupWaitName.innerHTML = `${groupName}`

    for(wait in waits){
        groupWaitAlertText.innerHTML = `
        <form method="GET" class="group-wait__one d-flex flex-row">
            <div class="d-flex flex-row align-items-center">
                <img src="${ waits_img }" height="50" width="50" style="border-radius: 50px;"/>
                <h6>${ wait }</h6>
                <input type="submit" value="수락" name="accept">
                <input type="submit" value="거절" name="reject">
            </div>  
        </form>
        `;
    }
    groupWaitAlert.style.display = 'block';
}