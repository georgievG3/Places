document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('image-formset-container');
    const addBtn = document.getElementById('add-image-btn');
    const totalForms = document.getElementById('id_images-TOTAL_FORMS');

    addBtn.addEventListener('click', function () {
        const formCount = parseInt(totalForms.value, 10);
        const newForm = document.createElement('div');
        newForm.classList.add('image-form');
        newForm.innerHTML = `
            <input type="file" name="images-${formCount}-image" id="id_images-${formCount}-image" accept="image/*">
            <button type="button" class="remove-image-btn">Премахни</button>
            <input type="hidden" name="images-${formCount}-DELETE" id="id_images-${formCount}-DELETE" value="false">
        `;
        container.appendChild(newForm);

        totalForms.value = formCount + 1;
    });

    container.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-image-btn')) {
            const formDiv = e.target.closest('.image-form');
            const deleteInput = formDiv.querySelector('input[type="hidden"][name$="-DELETE"]');
            if (deleteInput) {
                deleteInput.value = 'on';
                formDiv.style.display = 'none';
            } else {
                formDiv.remove();
            }
        }
    });
});
