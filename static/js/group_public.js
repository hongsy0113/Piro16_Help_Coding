const user_id = JSON.parse(document.getElementById('user_id').textContent);
const group_id = JSON.parse(document.getElementById('group_id').textContent);

const onClickLike = async(id) => {
    const url = '/group/interest_ajax';
    const {data} = await axios.post(url,{
        id 
    });
    likeHandleResponse(data.id);
}

const heartBtn = document.querySelectorAll('.all-group__heart');
heartBtn.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const [txt1, txt2, groupId] = btn.getAttribute('id').split('-');
        // const groupLike = document.querySelector(`.all-group__heart--${groupId}`);

        onClickLike(groupId);
    })
})


const likeHandleResponse = (id) => {
    const element = document.querySelector(`.all-group__heart--${id}`)
    const num = element.innerHTML;
    const count = Number(num) + 1;

    element.innerHTML = `${count}`
};