document.addEventListener('DOMContentLoaded', () => {
    let peekButton = document.getElementById('peek-button');
    if (peekButton) {
        peekButton.addEventListener('click', (e) => {
            let offensiveFields = document.querySelectorAll('[class*="offensive-word"]');
            for (let field of offensiveFields) {
                if (field.className === 'offensive-word') {
                    field.className = field.className + '-enabled';
                    peekButton.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
                } else {
                    field.className = 'offensive-word';
                    peekButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
                }
            }
        });
    }
});