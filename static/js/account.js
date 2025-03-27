document.addEventListener('DOMContentLoaded', function() {
    // Profile edit form 
    const editProfileButton = document.getElementById('edit-profile-button');
    const editProfileForm = document.getElementById('edit-profile-form');
    const cancelProfileEdit = document.getElementById('cancel-profile-edit');
    
    editProfileButton.addEventListener('click', function() {
        editProfileForm.style.display = 'block';
        editProfileButton.style.display = 'none';
    });
    
    cancelProfileEdit.addEventListener('click', function() {
        editProfileForm.style.display = 'none';
        editProfileButton.style.display = 'inline-block';
    });
    
    // Add animal form toggle
    const addAnimalButton = document.getElementById('add-animal-button');
    const addAnimalForm = document.getElementById('add-animal-form');
    const cancelAddAnimal = document.getElementById('cancel-add-animal');
    
    addAnimalButton.addEventListener('click', function() {
        addAnimalForm.style.display = 'block';
        addAnimalButton.style.display = 'none';
    });
    
    cancelAddAnimal.addEventListener('click', function() {
        addAnimalForm.style.display = 'none';
        addAnimalButton.style.display = 'inline-block';
    });
});