const searchButton = document.querySelector('.group_post__search__submit')

const searchInput = document.querySelector('.group_post__search__input')

const pattern =  /^\s+|\s+$/g;

searchButton.addEventListener('click', function(){
    if(searchInput.value.replace(pattern, "") === ''){
        alert('검색어를 입력해주세요. 🙄')
    }
})