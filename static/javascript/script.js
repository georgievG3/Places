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

document.addEventListener("DOMContentLoaded", function () {
        const openBtn = document.getElementById("open-gallery-btn");
        const modal = document.getElementById("image-modal");
        const closeBtn = document.getElementById("close-modal");

        openBtn.addEventListener("click", function () {
            modal.style.display = "block";
        });

        closeBtn.addEventListener("click", function () {
            modal.style.display = "none";
        });

        window.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });

    });

document.addEventListener('DOMContentLoaded', () => {
    const priceRange = document.getElementById('price-range');
    const priceValue = document.getElementById('price-value');

    if(priceRange && priceValue){
        priceRange.addEventListener('input', () => {
            priceValue.textContent = priceRange.value;
        });
    }
});

document.getElementById('add-block').addEventListener('click', function () {
        const formsetDiv = document.getElementById('blocks-formset');
        const totalForms = document.getElementById('id_blocks-TOTAL_FORMS');
        const currentForms = parseInt(totalForms.value);

        const newForm = formsetDiv.querySelector('.block-form').cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/blocks-(\d+)-/g, `blocks-${currentForms}-`);
        formsetDiv.appendChild(newForm);

        totalForms.value = currentForms + 1;
    });

