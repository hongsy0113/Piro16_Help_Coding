const searchButton = document.querySelector('.qna__search__submit')

const searchInput = document.querySelector('.qna__search__input')

const pattern =  /^\s+|\s+$/g;

searchButton.addEventListener('click', function(){
    if(searchInput.value.replace(pattern, "") === ''){
        alert('검색어를 입력해주세요. 🙄')
    }
})