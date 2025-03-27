document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggle-filters');
    const filterForm = document.getElementById('filter-form');
    
    toggleButton.addEventListener('click', function() {
        if (filterForm.style.display === 'none') {
            filterForm.style.display = 'block';
        } else {
            filterForm.style.display = 'none';
        }
    });
    
    if ("{{ filter_applied }}" === "True") {
        filterForm.style.display = 'block';
    }
});