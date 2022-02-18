const groupClickBox = document.querySelector('.gridbox__item-group');

if(user_id == null) {
    groupClickBox.addEventListener('click', function(){
        alert('로그인 후 이용해주세요.');
    })

    const groupCreateBtn = document.querySelector('.right__makebtn');
    groupClickBox.addEventListener('click', function(){
        alert('로그인 후 이용해주세요.');
    })
}