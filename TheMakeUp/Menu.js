const toggleButton = document.querySelector('.menu-toggle');
const closeButton = document.querySelector('.close-button');
const closeInfoButton = document.querySelector('.close-Info');
const sidebar = document.querySelector('.sidebar');
const infotab = document.querySelector('.infotab');
const InfoButton = document.querySelector('.infoExer');

toggleButton.addEventListener('click', () => {
    sidebar.classList.add('open');
});

closeButton.addEventListener('click', () => {
    sidebar.classList.remove('open');
});

InfoButton.addEventListener('click', () => {
    infotab.classList.add('open');
});

closeInfoButton.addEventListener('click', () => {
    infotab.classList.remove('open');
});