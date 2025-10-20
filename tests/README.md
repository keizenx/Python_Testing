# Documentation des Tests - Flask Booking App

## 📋 Vue d'ensemble

Ce dossier contient tous les tests pour l'application Flask de réservation de compétitions. Les tests sont divisés en **tests unitaires** et **tests d'intégration**, avec un coverage de **79%** du code.

## 🏗️ Structure

```
tests/
├── __init__.py                  # Package de tests
├── conftest.py                  # Fixtures partagées et configuration
├── test_unit.py                 # Tests unitaires (9 tests)
├── test_integration.py          # Tests d'intégration (17 tests)
├── fixtures/                    # Données de test
│   ├── test_clubs.json         # Clubs de test
│   └── test_competitions.json  # Compétitions de test
└── README.md                    # Cette documentation
```

## 🚀 Installation des dépendances

```bash
# Activer le venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Installer les dépendances de test
pip install -r requirements.txt
```

## 🧪 Exécution des tests

### Tous les tests

```bash
pytest
```

### Tests avec verbosité

```bash
pytest -v
```

### Tests unitaires uniquement

```bash
pytest -m unit
```

### Tests d'intégration uniquement

```bash
pytest -m integration
```

### Tests avec coverage

```bash
pytest --cov=. --cov-report=html
```

Puis ouvrir `htmlcov/index.html` dans un navigateur pour voir le rapport détaillé.

### Tests spécifiques

```bash
# Un fichier
pytest tests/test_unit.py

# Une classe
pytest tests/test_unit.py::TestLoadClubs

# Un test spécifique
pytest tests/test_unit.py::TestLoadClubs::test_load_clubs_success
```

## 📊 Configuration pytest

La configuration est définie dans `pytest.ini` à la racine du projet :

- **Découverte automatique** : `tests/` directory
- **Coverage minimum** : 79%
- **Logging détaillé** : Format `YYYY-MM-DD HH:MM:SS - [LEVEL] - message`
- **Rapports** : HTML + terminal
- **Marqueurs** : `unit`, `integration`, `slow`

## 📝 Tests Unitaires (test_unit.py)

Teste les fonctions pures avec mocking :

- `loadClubs()` : 4 tests
  - Chargement réussi
  - Liste vide
  - Fichier introuvable
  - JSON invalide

- `loadCompetitions()` : 5 tests
  - Chargement réussi
  - Liste vide
  - Fichier introuvable
  - JSON invalide
  - Structure des données

## 🌐 Tests d'Intégration (test_integration.py)

Teste les routes Flask complètes :

### Routes testées
- `GET /` : Page d'accueil
- `POST /showSummary` : Login
- `GET /book/<competition>/<club>` : Page de réservation
- `POST /purchasePlaces` : Réservation
- `GET /points` : Affichage des points
- `GET /logout` : Déconnexion

### Workflow complet
Test end-to-end simulant un parcours utilisateur complet (marqueur `@slow`)

## 🔧 Fixtures (conftest.py)

### Fixtures disponibles

- `test_clubs` : Charge les clubs de test depuis `fixtures/test_clubs.json`
- `test_competitions` : Charge les compétitions de test depuis `fixtures/test_competitions.json`
- `app` : Instance Flask configurée pour les tests
- `client` : Client de test Flask
- `sample_club` : Un club de test unique
- `sample_competition` : Une compétition de test unique
- `reset_test_data` : Réinitialise les données après chaque test (autouse)

## 📈 Coverage actuel

| Fichier | Statements | Missing | Coverage |
|---------|-----------|---------|----------|
| server.py | 73 | 4 | **95%** |
| tests/conftest.py | 92 | 22 | 76% |
| tests/test_unit.py | 122 | 27 | 78% |
| tests/test_integration.py | 206 | 51 | 75% |
| **TOTAL** | **493** | **104** | **79%** |

## 📋 Logging

Les tests génèrent des logs détaillés :

- **Console** : Niveau INFO
- **Fichier** : `tests_log.txt` (niveau DEBUG)
- **Format** : `YYYY-MM-DD HH:MM:SS - [LEVEL] - message`

## ✅ Bonnes pratiques

1. **Isolation** : Chaque test est isolé avec `reset_test_data`
2. **Fixtures** : Utiliser les fixtures pour les données de test
3. **Marqueurs** : Marquer les tests (`@pytest.mark.unit`, `@pytest.mark.integration`)
4. **Docstrings** : Toutes les fonctions documentées
5. **Assertions** : Messages d'assertion explicites
6. **Try/Except** : Gestion des erreurs avec logging

## 🐛 Dépannage

### Les tests échouent avec "TemplateNotFound"
Vérifier que `conftest.py` configure correctement le `template_folder` de Flask.

### Coverage trop bas
Exécuter avec `--cov-report=html` pour identifier les lignes non couvertes.

### Erreur de fixture
Vérifier que les fichiers `fixtures/*.json` existent et sont valides.

## 📚 Commandes utiles

```bash
# Lister tous les tests sans les exécuter
pytest --collect-only

# Exécuter seulement les tests qui ont échoué la dernière fois
pytest --lf

# Arrêter à la première erreur
pytest -x

# Afficher les variables locales en cas d'échec
pytest -l

# Mode verbose avec traceback complet
pytest -vv --tb=long

# Générer un rapport JUnit (CI/CD)
pytest --junitxml=report.xml
```

## 🔄 Intégration Continue

Pour utiliser dans un pipeline CI/CD :

```yaml
# Exemple GitHub Actions
- name: Run tests
  run: |
    pytest --cov=. --cov-report=xml --junitxml=junit.xml
```

## 📞 Support

Pour toute question ou amélioration des tests, consulter :
- Documentation pytest : https://docs.pytest.org/
- pytest-flask : https://pytest-flask.readthedocs.io/
- pytest-cov : https://pytest-cov.readthedocs.io/

