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

// Fonctionnalités spécifiques à la page de connexion
function initializeLoginPage() {
    const emailInput = document.getElementById('email');
    const submitButton = document.querySelector('.btn-primary');

    if (emailInput && submitButton) {
        // Validation en temps réel pour la page de connexion
        emailInput.addEventListener('input', function() {
            const email = this.value.trim();
            const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

            if (email) {
                if (isValid) {
                    this.style.borderColor = '#28a745';
                    this.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                    submitButton.disabled = false;
                    submitButton.textContent = ' Accéder à mon compte';
                } else {
                    this.style.borderColor = '#dc3545';
                    this.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';
                    submitButton.disabled = true;
                    submitButton.textContent = '❌ Adresse email invalide';
                }
            } else {
                this.style.borderColor = '#e9ecef';
                this.style.boxShadow = 'none';
                submitButton.disabled = false;
                submitButton.textContent = ' Accéder à mon compte';
            }
        });

        // Gestionnaire de soumission du formulaire
        const loginForm = document.querySelector('.login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                const email = emailInput.value.trim();
                const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

                if (!isValid) {
                    e.preventDefault();
                    showAlert('Veuillez saisir une adresse email valide.', 'error');
                    emailInput.focus();
                    return false;
                }

                // Animation de chargement
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="loading"></span> Connexion en cours...';
            });
        }
    }
}

// Fonction pour afficher des alertes temporaires
function showAlert(message, type = 'info') {
    // Supprimer les alertes existantes
    const existingAlerts = document.querySelectorAll('.alert-temp');
    existingAlerts.forEach(alert => alert.remove());

    // Créer la nouvelle alerte
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-temp fade-in`;
    alertDiv.innerHTML = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '10000';
    alertDiv.style.maxWidth = '400px';

    // Ajouter un bouton de fermeture
    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = ' ×';
    closeBtn.style.float = 'right';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.fontWeight = 'bold';
    closeBtn.onclick = function() {
        alertDiv.style.display = 'none';
    };
    alertDiv.insertBefore(closeBtn, alertDiv.firstChild);

    document.body.appendChild(alertDiv);

    // Auto-disparition après 5 secondes
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.transition = 'opacity 0.5s ease';
            alertDiv.style.opacity = '0';
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 500);
        }
    }, 5000);
}

// Initialiser les fonctionnalités de la page de connexion
initializeLoginPage();

// Fonctionnalités spécifiques à la page welcome (tableau de bord)
function initializeWelcomePage() {
    // Animation des cartes de compétition au scroll
    const competitionCards = document.querySelectorAll('.competition-card');

    if (competitionCards.length > 0) {
        // Intersection Observer pour les animations au scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                }
            });
        }, observerOptions);

        competitionCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    }

    // Tooltip informatif sur les points
    const pointsNumber = document.querySelector('.points-number');
    if (pointsNumber) {
        pointsNumber.title = 'Ces points peuvent être utilisés pour réserver des places dans les compétitions';
    }

    // Animation des statuts de compétition
    const statusElements = document.querySelectorAll('.status');
    statusElements.forEach(status => {
        status.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.2s ease';
        });

        status.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Gestion des boutons de réservation
    const bookButtons = document.querySelectorAll('a[href*="book"]');
    bookButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Indicateur de chargement pour les actions
    const actionButtons = document.querySelectorAll('.competition-actions a, .header-actions a');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.hasAttribute('disabled')) {
                // Ajouter un indicateur visuel de chargement
                const originalText = this.textContent;
                this.innerHTML = '<span class="loading"></span> Chargement...';
                this.style.pointerEvents = 'none';

                // Remettre le texte original après un court délai
                // (la navigation se fera normalement)
                setTimeout(() => {
                    if (this.parentNode) { // Vérifier si l'élément existe encore
                        this.innerHTML = originalText;
                        this.style.pointerEvents = 'auto';
                    }
                }, 1000);
            }
        });
    });

    // Message de bienvenue personnalisé
    const clubName = document.querySelector('.club-info h1');
    if (clubName) {
        console.log(`🏆 Bienvenue sur le tableau de bord ${clubName.textContent.trim()}`);
    }
}

// Initialiser les fonctionnalités de la page welcome
initializeWelcomePage();

console.log('✅ Toutes les fonctionnalités JavaScript initialisées');
