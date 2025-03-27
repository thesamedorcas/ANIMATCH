document.addEventListener('DOMContentLoaded', function() {
    
    const adoptButton = document.getElementById('adopt-button');
    const adoptionForm = document.getElementById('adoption-form');
    const cancelAdoption = document.getElementById('cancel-adoption');
    
    if (adoptButton) {
        adoptButton.addEventListener('click', function() {
            adoptionForm.style.display = 'block';
            adoptButton.style.display = 'none';
        });
    }
    
    if (cancelAdoption) {
        cancelAdoption.addEventListener('click', function() {
            adoptionForm.style.display = 'none';
            adoptButton.style.display = 'inline-block';
        });
    }
    
    // Edit form 
    const editButton = document.getElementById('edit-button');
    const editForm = document.getElementById('edit-form');
    const cancelEdit = document.getElementById('cancel-edit');
    
    if (editButton) {
        editButton.addEventListener('click', function() {
            editForm.style.display = 'block';
            editButton.style.display = 'none';
        });
    }
    
    if (cancelEdit) {
        cancelEdit.addEventListener('click', function() {
            editForm.style.display = 'none';
            editButton.style.display = 'inline-block';
        });
    }
});