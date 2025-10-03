// JavaScript principal pour GUDLFT
// Version simplifiée mais fonctionnelle

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 GUDLFT JavaScript chargé avec succès !');

    // Initialiser les fonctionnalités
    initializeAnimations();
    initializeForms();
    initializeAlerts();

    // Marquer que JS fonctionne
    showJSStatus();
});

function initializeAnimations() {
    // Ajouter des animations d'entrée à tous les éléments principaux
    const elements = document.querySelectorAll('.card, .btn, .alert, .header');
    elements.forEach((element, index) => {
        element.classList.add('fade-in');
        element.style.animationDelay = `${index * 0.1}s`;
    });
}

function initializeForms() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        // Gestionnaire de soumission
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Chargement...';
            }
        });

        // Validation en temps réel des emails
        const emailInputs = form.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateEmailField(this);
            });

            input.addEventListener('input', function() {
                clearFieldValidation(this);
            });
        });

        // Validation des nombres
        const numberInputs = form.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateNumberField(this);
            });

            input.addEventListener('input', function() {
                clearFieldValidation(this);
            });
        });
    });
}

function validateEmailField(input) {
    const value = input.value.trim();
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

    if (value && !isValid) {
        showFieldError(input, 'Adresse email invalide');
        input.style.borderColor = '#dc3545';
    } else if (value && isValid) {
        input.style.borderColor = '#28a745';
    }
}

function validateNumberField(input) {
    const value = input.value.trim();
    const numValue = parseInt(value);
    const min = input.min ? parseInt(input.min) : null;
    const max = input.max ? parseInt(input.max) : null;

    if (value && isNaN(numValue)) {
        showFieldError(input, 'Valeur numérique requise');
        input.style.borderColor = '#dc3545';
    } else if (min !== null && numValue < min) {
        showFieldError(input, `Minimum: ${min}`);
        input.style.borderColor = '#dc3545';
    } else if (max !== null && numValue > max) {
        showFieldError(input, `Maximum: ${max}`);
        input.style.borderColor = '#dc3545';
    } else if (value) {
        input.style.borderColor = '#28a745';
    }
}

function showFieldError(input, message) {
    clearFieldValidation(input);

    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error';
    errorDiv.textContent = message;
    errorDiv.style.fontSize = '0.9rem';
    errorDiv.style.marginTop = '5px';
    errorDiv.style.padding = '8px 12px';

    input.parentNode.appendChild(errorDiv);
}

function clearFieldValidation(input) {
    const errorDiv = input.parentNode.querySelector('.alert-error');
    if (errorDiv) {
        errorDiv.remove();
    }
    input.style.borderColor = '#e9ecef';
}

function initializeAlerts() {
    // Auto-disparition des messages d'alerte après 5 secondes
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        }, 5000);

        // Fermeture manuelle au clic
        alert.addEventListener('click', function() {
            this.style.display = 'none';
        });
    });
}

function showJSStatus() {
    // Ajouter un indicateur visuel que JS fonctionne
    const body = document.querySelector('body');
    const jsIndicator = document.createElement('div');
    jsIndicator.id = 'js-status';
    jsIndicator.innerHTML = '✅ JavaScript actif';
    jsIndicator.style.position = 'fixed';
    jsIndicator.style.bottom = '10px';
    jsIndicator.style.right = '10px';
    jsIndicator.style.background = '#28a745';
    jsIndicator.style.color = 'white';
    jsIndicator.style.padding = '5px 10px';
    jsIndicator.style.borderRadius = '4px';
    jsIndicator.style.fontSize = '12px';
    jsIndicator.style.zIndex = '1000';
    jsIndicator.style.opacity = '0.8';

    body.appendChild(jsIndicator);

    // Masquer après 3 secondes
    setTimeout(() => {
        jsIndicator.style.display = 'none';
    }, 3000);
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

// Calcul automatique des points (si applicable)
function updatePointsCalculation() {
    const placesInput = document.querySelector('input[name="places"]');
    const pointsDisplay = document.querySelector('.points-info');

    if (placesInput && pointsDisplay) {
        placesInput.addEventListener('input', function() {
            const places = parseInt(this.value) || 0;
            const pointsNeeded = places;

            // Simuler un calcul de points disponibles
            const availablePoints = 15; // Exemple
            const remainingPoints = availablePoints - pointsNeeded;

            if (remainingPoints >= 0) {
                pointsDisplay.innerHTML = `<strong>Points restants après réservation: ${remainingPoints}</strong>`;
                pointsDisplay.style.color = '#28a745';
            } else {
                pointsDisplay.innerHTML = `<strong>Points insuffisants ! Manque: ${Math.abs(remainingPoints)} points</strong>`;
                pointsDisplay.style.color = '#dc3545';
            }
        });
    }
}

// Initialiser le calcul des points
updatePointsCalculation();

console.log('✅ Toutes les fonctionnalités JavaScript initialisées');
