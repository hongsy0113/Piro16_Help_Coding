const groupClickBox = document.querySelector('.gridbox__item-group');

if(user_id == null) {
    groupClickBox.addEventListener('click', function(){
        alert('로그인 후 이용해주세요. 😄');
    })

    const groupCreateBtn = document.querySelector('.right__makebtn');
    groupClickBox.addEventListener('click', function(){
        alert('로그인 후 이용해주세요. 😄');
    })
}

const searchButton = document.querySelector('.group__search__submit')

const searchInput = document.querySelector('.group__search__input')

const pattern =  /^\s+|\s+$/g;

searchButton.addEventListener('click', function(){
    if(searchInput.value.replace(pattern, "") === ''){
        alert('검색어를 입력해주세요. 🙄')
    }
})