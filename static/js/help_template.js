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
const modalOverlay = document.querySelector('.modal__overlay');

detailGuideBtn.addEventListener('click', showGuide);
closeGuideBtn.addEventListener('click', closeGuide);
modalOverlay.addEventListener('click', closeGuide);

function showGuide() {
    detailGuideModal.style.display = 'flex';
}

function closeGuide() {
    detailGuideModal.style.display = 'none';
}

// 링크 설명 모달
const linkGuideEntryBtn = document.querySelector('.link-help__entry-btn');
const linkGuideScratchBtn = document.querySelector('.link-help__scratch-btn');

const linkGuideEntry = document.querySelector('.link-help__entry-cont');
const linkGuideScratch = document.querySelector('.link-help__scratch-cont');

function showGuideEntry() {
    linkGuideEntry.style.display = 'flex';
    linkGuideScratch.style.display = 'none';
    linkGuideScratchBtn.setAttribute('class', 'link-help__scratch-btn link-help__disabled-btn');
    linkGuideEntryBtn.setAttribute('class', 'link-help__entry-btn');
}

function showGuideScratch() {
    linkGuideEntry.style.display = 'none';
    linkGuideScratch.style.display = 'flex';
    linkGuideEntryBtn.setAttribute('class', 'link-help__entry-btn link-help__disabled-btn');
    linkGuideScratchBtn.setAttribute('class', 'link-help__scratch-btn');
}

linkGuideScratchBtn.addEventListener('click', showGuideScratch);
linkGuideEntryBtn.addEventListener('click', showGuideEntry);