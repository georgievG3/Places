document.addEventListener('DOMContentLoaded', function () {
    const formsetContainer = document.getElementById('image-formset-container');
    const addBtn = document.getElementById('add-image-btn');
    const totalFormsInput = document.getElementById('id_images-TOTAL_FORMS');
    const maxFormsInput = document.getElementById('id_images-MAX_NUM_FORMS');

    let totalForms = parseInt(totalFormsInput.value, 10);
    const maxForms = parseInt(maxFormsInput.value, 10);

    const forms = formsetContainer.querySelectorAll('.image-form');
    for (let i = 1; i < forms.length; i++) {
        forms[i].remove();
        totalForms--;
    }
    totalFormsInput.value = totalForms;

    function createImageForm(index) {
        const div = document.createElement('div');
        div.classList.add('image-form');
        div.id = `image-form-${index}`;

        const label = document.createElement('label');
        label.setAttribute('for', `id_images-${index}-image`);
        label.textContent = 'Image:';

        const input = document.createElement('input');
        input.type = 'file';
        input.name = `images-${index}-image`;
        input.id = `id_images-${index}-image`;
        input.accept = 'image/*';

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('remove-image-btn');
        removeBtn.textContent = 'Премахни';
        removeBtn.addEventListener('click', function () {
            div.remove();
            totalForms--;
            totalFormsInput.value = totalForms;
            updateFormIndexes();
        });

        div.appendChild(label);
        div.appendChild(input);
        div.appendChild(removeBtn);

        return div;
    }

    function updateFormIndexes() {
        const forms = formsetContainer.querySelectorAll('.image-form');
        forms.forEach((form, idx) => {
            form.id = `image-form-${idx}`;
            const label = form.querySelector('label');
            const input = form.querySelector('input[type="file"]');
            label.setAttribute('for', `id_images-${idx}-image`);
            input.name = `images-${idx}-image`;
            input.id = `id_images-${idx}-image`;
        });
    }

    const existingRemoveBtn = formsetContainer.querySelector('.remove-image-btn');
    if (existingRemoveBtn) {
        existingRemoveBtn.addEventListener('click', function () {
            const formDiv = existingRemoveBtn.closest('.image-form');
            formDiv.remove();
            totalForms--;
            totalFormsInput.value = totalForms;
            updateFormIndexes();
        });
    }

    addBtn.addEventListener('click', function () {
        if (totalForms >= maxForms) {
            alert(`Не може да добавите повече от ${maxForms} снимки.`);
            return;
        }
        const newForm = createImageForm(totalForms);
        formsetContainer.appendChild(newForm);
        totalForms++;
        totalFormsInput.value = totalForms;
    });
});
