// JavaScript principal pour GUDLFT

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 GUDLFT JavaScript chargé');

    // Initialiser les animations
    initializeAnimations();

    // Initialiser les formulaires
    initializeForms();

    // Initialiser les messages flash
    initializeFlashMessages();

    // Initialiser la validation en temps réel
    initializeValidation();
});

// Animations d'entrée
function initializeAnimations() {
    const elements = document.querySelectorAll('.card, .form-group, .btn');
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';

        setTimeout(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Gestion des formulaires
function initializeForms() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        // Validation avant soumission
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }

            // Afficher un indicateur de chargement
            showLoading(this);
        });

        // Validation en temps réel
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    });
}

// Validation de formulaire
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });

    return isValid;
}

// Validation d'un champ individuel
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';

    // Vérifications spécifiques selon le type
    switch (field.type) {
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (value && !emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Adresse email invalide';
            }
            break;

        case 'number':
            const numValue = parseInt(value);
            const min = field.min ? parseInt(field.min) : null;
            const max = field.max ? parseInt(field.max) : null;

            if (value && isNaN(numValue)) {
                isValid = false;
                errorMessage = 'Valeur numérique requise';
            } else if (min !== null && numValue < min) {
                isValid = false;
                errorMessage = `Minimum: ${min}`;
            } else if (max !== null && numValue > max) {
                isValid = false;
                errorMessage = `Maximum: ${max}`;
            }
            break;

        default:
            if (field.hasAttribute('required') && !value) {
                isValid = false;
                errorMessage = 'Ce champ est requis';
            }
            break;
    }

    // Afficher/cacher les erreurs
    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }

    return isValid;
}

// Afficher une erreur sur un champ
function showFieldError(field, message) {
    clearFieldError(field);

    field.style.borderColor = '#dc3545';

    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '5px';

    field.parentNode.appendChild(errorDiv);
}

// Effacer l'erreur d'un champ
function clearFieldError(field) {
    field.style.borderColor = '#28a745';

    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Messages flash avec auto-disparition
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message, .messages');

    flashMessages.forEach(message => {
        // Auto-disparition après 5 secondes
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 500);
        }, 5000);

        // Fermeture manuelle
        message.addEventListener('click', function() {
            this.style.display = 'none';
        });
    });
}

// Indicateur de chargement
function showLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Chargement...';
    }
}

// Validation en temps réel
function initializeValidation() {
    // Validation des emails en temps réel
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('input', function() {
            const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.value);
            this.style.borderColor = isValid ? '#28a745' : '#ffc107';
        });
    });

    // Calcul automatique pour les réservations
    const placesInputs = document.querySelectorAll('input[name="places"]');
    placesInputs.forEach(input => {
        input.addEventListener('input', function() {
            const pointsNeeded = parseInt(this.value) || 0;
            const pointsDisplay = document.querySelector('.points-info');

            if (pointsDisplay) {
                const currentPoints = parseInt(pointsDisplay.textContent.match(/(\d+)/)?.[1] || '0');
                const remainingPoints = currentPoints - pointsNeeded;

                // Mettre à jour l'affichage
                if (remainingPoints >= 0) {
                    pointsDisplay.style.color = '#28a745';
                    pointsDisplay.innerHTML = `Points restants après réservation: <strong>${remainingPoints}</strong>`;
                } else {
                    pointsDisplay.style.color = '#dc3545';
                    pointsDisplay.innerHTML = `Points insuffisants ! Il manque: <strong>${Math.abs(remainingPoints)}</strong> points`;
                }
            }
        });
    });
}

// Fonctions utilitaires
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Gestion des erreurs AJAX (si besoin futur)
function handleAjaxError(xhr, status, error) {
    console.error('Erreur AJAX:', status, error);
    showGlobalMessage('Une erreur réseau s\'est produite. Veuillez réessayer.', 'error');
}

// Message global
function showGlobalMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message flash-${type}`;
    messageDiv.textContent = message;

    const container = document.querySelector('.container') || document.body;
    container.insertBefore(messageDiv, container.firstChild);

    // Auto-disparition
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Export pour utilisation globale
window.GUDLFT = {
    showGlobalMessage,
    validateField,
    showLoading
};

console.log('✅ GUDLFT JavaScript initialisé avec succès');
