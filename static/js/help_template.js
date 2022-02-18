const showCautionHover = document.querySelector('.modal__help-btn');
const cautionAlert = document.querySelector('.help__container');

function showCaution(){
    cautionAlert.style.display = 'flex';
}

function closeCaution(){
    cautionAlert.style.display = 'none';
}