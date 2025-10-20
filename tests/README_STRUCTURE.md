# Structure des Tests - Application de Réservation Régionale

## Organisation des Tests

Selon le guide de développement, les tests sont organisés en trois catégories distinctes dans des dossiers séparés :

### 📁 tests/unit/
**Tests unitaires pour les fonctions pures**

- `test_load_functions.py` : Tests pytest pour loadClubs() et loadCompetitions()
- `test_load_functions_unittest.py` : Tests unittest pour les mêmes fonctions (démonstration de compatibilité)

**Objectif** : Tester les fonctions isolées avec mocking, sans dépendances externes.

**Ratio** : 2x plus de tests unitaires que d'intégration/fonctionnels (selon guide)

### 📁 tests/integration/
**Tests d'intégration pour les routes Flask**

- `test_routes.py` : Tests de toutes les routes HTTP de l'application
  - GET / (index)
  - POST /showSummary (authentification)
  - GET /book/<competition>/<club> (page de réservation)
  - POST /purchasePlaces (réservation)
  - GET /points (affichage des points)
  - GET /logout (déconnexion)

**Objectif** : Tester l'intégration entre les routes Flask et la logique métier.

### 📁 tests/functional/
**Tests fonctionnels end-to-end**

- `test_scenarios.py` : Tests des scénarios complets utilisateur
  - Parcours utilisateur complet (Phase 1)
  - Règles métier (max 12 places, éviter surréservation)
  - Transparence des points (Phase 2)
  - Performance (< 5s pour liste, < 2s pour mise à jour)
  - Gestion des erreurs et cas limites

**Objectif** : Valider les parcours utilisateurs complets et les exigences métier.

## Frameworks de Test

### pytest (principal)
- Configuration dans `pytest.ini`
- Marqueurs : `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.functional`, `@pytest.mark.slow`
- Coverage configuré pour 60% minimum (selon guide)

### unittest (complémentaire)
- Tests dans `test_load_functions_unittest.py`
- Compatible avec pytest (peut être exécuté par pytest)
- Utilise `unittest.TestCase`

## Fixtures

### Fichier principal : `conftest.py`
Contient toutes les fixtures partagées :
- `test_clubs` : Charge les données de clubs de test depuis fixtures/test_clubs.json
- `test_competitions` : Charge les données de compétitions depuis fixtures/test_competitions.json
- `app` : Instance Flask configurée pour les tests
- `client` : Client de test Flask
- `sample_club` : Un club de test unique
- `sample_competition` : Une compétition de test unique
- `reset_test_data` : Réinitialise les données après chaque test (autouse)

### Données de test : `fixtures/`
- `test_clubs.json` : 3 clubs de test avec différents points
- `test_competitions.json` : 3 compétitions de test avec différentes disponibilités

## Exécution des Tests

### Tous les tests
```bash
pytest
```

### Tests unitaires uniquement
```bash
pytest tests/unit/
pytest -m unit
```

### Tests d'intégration uniquement
```bash
pytest tests/integration/
pytest -m integration
```

### Tests fonctionnels uniquement
```bash
pytest tests/functional/
pytest -m functional
```

### Avec couverture
```bash
pytest --cov=. --cov-report=html
```

### Tests unittest spécifiquement
```bash
python -m pytest tests/unit/test_load_functions_unittest.py
python -m unittest tests.unit.test_load_functions_unittest
```

## Couverture de Code

**Objectif** : ≥ 60% (selon guide de développement)

Les fichiers exclus de la couverture :
- tests/*
- venv/*
- static/*
- templates/*
- setup.py

## Logging

Tous les tests utilisent le logging configuré selon les règles :
- Format : `YYYY-MM-DD HH:MM:SS - [LEVEL] - message`
- Sortie console : INFO
- Fichier log : `tests_log.txt` (DEBUG)

## Performance

Les tests marqués `@pytest.mark.slow` testent les exigences de performance :
- Chargement de la liste de compétitions : < 5 secondes
- Mise à jour des points : < 2 secondes
- Tests de performance exécutés avec 6 utilisateurs par défaut (selon guide)

## Bonnes Pratiques

1. **Isolation** : Chaque test est indépendant grâce à `reset_test_data`
2. **Logging** : Chaque test log son statut (PASSED/FAILED)
3. **Assertions claires** : Messages descriptifs pour chaque assertion
4. **Documentation** : Docstrings pour chaque classe et méthode de test
5. **Nommage** : `test_<what>_<condition>` pour clarté

## Scénarios de Test Couverts

### Phase 0 (Démonstration)
- ✅ Connexion par email
- ✅ Visualisation du solde de points
- ✅ Utilisation des points pour acheter des places
- ✅ Éviter la surréservation
- ✅ Tableau des points

### Phase 1 (MVP)
- ✅ Connexion et consultation des compétitions
- ✅ Sélection d'une compétition
- ✅ Achat de places avec points
- ✅ Messages de confirmation/erreur
- ✅ Déduction des points
- ✅ Limite de places disponibles
- ✅ Maximum 12 places par club
- ✅ Déconnexion

### Phase 2 (Public et Performance)
- ✅ Tableau public des points (lecture seule)
- ✅ Accessible sans connexion
- ✅ Temps de chargement < 5s
- ✅ Mise à jour < 2s

## Rapport de Test

Le plan de test complet avec tous les scénarios se trouve dans `PLAN_DE_TEST.md`
