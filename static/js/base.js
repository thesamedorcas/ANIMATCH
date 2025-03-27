document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
      
            const message = this.parentElement;
            message.style.display = 'none';
        });
    });
    //close message after 6 seconds
    setTimeout(function() {
        const messages = document.querySelectorAll('.message');
        messages.forEach(message => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.6s'; //fade design
            setTimeout(function() {
                message.style.display = 'none';
            }, 600); 
        });
    }, 6000); 
});