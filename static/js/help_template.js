const showCautionHover = document.querySelector('.modal__help-btn');
const cautionAlert = document.querySelector('.help__container');

showCautionHover.addEventListener('mouseover', (event) => {
    cautionAlert.style.display = 'flex';
})

showCautionHover.addEventListener('mouseout', (event) => {
    cautionAlert.style.display = 'none';
})