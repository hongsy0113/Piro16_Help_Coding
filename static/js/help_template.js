// 글 작성 유의사항 모달
const showCautionHover = document.querySelector('.modal__help-btn');
const cautionAlert = document.querySelector('.help__container');

function showCaution(){
    cautionAlert.style.display = 'flex';
}

function closeCaution(){
    cautionAlert.style.display = 'none';
}

// 글 작성 태그, 링크 설명 모달
const detailGuideBtn = document.querySelector('.detail-guide__btn');
const detailGuideModal = document.querySelector('.detail-guide__container');
const closeGuideBtn = document.querySelector('.detail-guide__close--btn');

detailGuideBtn.addEventListener('click', showGuide);
closeGuideBtn.addEventListener('click', closeGuide);

function showGuide() {
    detailGuideModal.style.display = 'flex';
}

function closeGuide() {
    detailGuideModal.style.display = 'none';
}