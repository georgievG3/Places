const sliderContainer = [...document.querySelectorAll('.slider-container')];
const nextBtn = [...document.querySelectorAll('.next-btn')];
const preBtn = [...document.querySelectorAll('.pre-btn')];

sliderContainer.forEach((item, i) => {
    let containerDimensions = item.getBoundingClientRect();
    let containerWidth = containerDimensions.width;

    nextBtn[i].addEventListener('click', () => {
        item.scrollLeft += containerWidth
    })

    preBtn[i].addEventListener('click', () => {
        item.scrollLeft -= containerWidth
    })
})