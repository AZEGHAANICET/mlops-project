# 📖 Guide d'utilisation du Makefile

Ce guide explique comment utiliser le Makefile sur différents systèmes d'exploitation.

---

## 🪟 Windows

### Option 1: Installer Make pour Windows

#### Via Chocolatey (recommandé)
```powershell
# Installer Chocolatey si vous ne l'avez pas
# Puis installer Make
choco install make
```

#### Via GnuWin32
1. Télécharger GnuWin32 Make depuis : https://sourceforge.net/projects/gnuwin32/
2. Installer et ajouter au PATH
3. Redémarrer le terminal

#### Via WSL (Windows Subsystem for Linux)
```bash
# Dans WSL
sudo apt-get update
sudo apt-get install make
```

### Option 2: Utiliser les commandes directement (sans Make)

Si vous ne voulez pas installer Make, voici les équivalents directs :

| Commande Make | Commande équivalente |
|---------------|---------------------|
| `make help` | Voir la liste ci-dessous |
| `make install` | `pip install -r requirements.txt` |
| `make train` | `python src/train.py` |
| `make test` | `pytest` |
| `make test-cov` | `pytest --cov=app --cov=src --cov-report=html --cov-report=term-missing` |
| `make run` | `uvicorn app:app --reload --host 0.0.0.0 --port 8000` |
| `make docker-build` | `docker build -t iris-classifier .` |
| `make docker-run` | `docker run -p 8000:8080 iris-classifier` |
| `make docker-compose-up` | `docker-compose up -d` |
| `make docker-compose-down` | `docker-compose down` |
| `make clean` | Voir section "Nettoyage manuel" |
| `make lint` | `flake8 app.py schemas.py src/ tests/` |
| `make format` | `black app.py schemas.py src/ tests/` puis `isort app.py schemas.py src/ tests/` |
| `make dvc-pull` | `dvc pull` |
| `make dvc-status` | `dvc status` |

### Option 3: Utiliser un script PowerShell (recommandé pour Windows)

Créez un fichier `run.ps1` avec ces commandes :

```powershell
# run.ps1
param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

switch ($Command) {
    "help" {
        Write-Host "Available commands:"
        Write-Host "  install       - Install dependencies"
        Write-Host "  train         - Train the model"
        Write-Host "  test          - Run tests"
        Write-Host "  test-cov      - Run tests with coverage"
        Write-Host "  run           - Run the application"
        Write-Host "  docker-build  - Build Docker image"
        Write-Host "  docker-run    - Run Docker container"
        Write-Host "  docker-up     - Start with Docker Compose"
        Write-Host "  docker-down   - Stop Docker Compose"
        Write-Host "  clean         - Clean temporary files"
        Write-Host "  lint          - Lint code"
        Write-Host "  dvc-pull      - Pull data from DVC"
    }
    "install" {
        pip install -r requirements.txt
    }
    "train" {
        python src/train.py
    }
    "test" {
        pytest
    }
    "test-cov" {
        pytest --cov=app --cov=src --cov-report=html --cov-report=term-missing
    }
    "run" {
        uvicorn app:app --reload --host 0.0.0.0 --port 8000
    }
    "docker-build" {
        docker build -t iris-classifier .
    }
    "docker-run" {
        docker run -p 8000:8080 iris-classifier
    }
    "docker-up" {
        docker-compose up -d
    }
    "docker-down" {
        docker-compose down
    }
    "clean" {
        Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
        Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force
        Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force .coverage -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
        Write-Host "Cleaned temporary files"
    }
    "lint" {
        flake8 app.py schemas.py src/ tests/
    }
    "dvc-pull" {
        dvc pull
    }
    default {
        Write-Host "Unknown command: $Command"
        Write-Host "Run '.\run.ps1 help' for available commands"
    }
}
```

**Utilisation :**
```powershell
.\run.ps1 help
.\run.ps1 install
.\run.ps1 run
```

---

## 🐧 Linux / macOS

Make est généralement installé par défaut. Sinon :

### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install make
```

### macOS
```bash
# Avec Homebrew
brew install make
```

### Utilisation
```bash
# Voir toutes les commandes disponibles
make help

# Installer les dépendances
make install

# Lancer l'application
make run

# Lancer les tests
make test
```

---

## 📋 Liste des commandes disponibles

### `make help`
Affiche toutes les commandes disponibles avec leurs descriptions.

### `make install`
Installe toutes les dépendances Python listées dans `requirements.txt`.

### `make train`
Entraîne le modèle de classification Iris et sauvegarde les résultats.

### `make test`
Lance tous les tests avec pytest.

### `make test-cov`
Lance les tests avec un rapport de couverture de code.

### `make run`
Lance l'application FastAPI en mode développement (avec rechargement automatique).

### `make docker-build`
Construit l'image Docker de l'application.

### `make docker-run`
Lance un conteneur Docker avec l'application.

### `make docker-compose-up`
Démarre les services avec Docker Compose en mode détaché.

### `make docker-compose-down`
Arrête les services Docker Compose.

### `make clean`
Nettoie tous les fichiers temporaires (cache Python, fichiers de test, etc.).

### `make lint`
Vérifie la qualité du code avec flake8.

### `make format`
Formate le code avec black et isort (nécessite l'installation de ces outils).

### `make dvc-pull`
Télécharge les données et modèles versionnés avec DVC.

### `make dvc-status`
Vérifie le statut des fichiers trackés par DVC.

---

## 🧹 Nettoyage manuel (sans Make)

Si vous ne pouvez pas utiliser Make, voici comment nettoyer manuellement :

### Windows PowerShell
```powershell
# Supprimer les dossiers __pycache__
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Supprimer les fichiers .pyc
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force

# Supprimer les dossiers de cache
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .coverage -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue
```

### Linux/macOS
```bash
# Supprimer les dossiers __pycache__
find . -type d -name __pycache__ -exec rm -r {} +

# Supprimer les fichiers .pyc
find . -type f -name "*.pyc" -delete

# Supprimer les dossiers de cache
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov
rm -rf dist
rm -rf build
```

---

## 🚀 Workflow typique

### Développement local
```bash
# 1. Installer les dépendances
make install

# 2. Télécharger les données
make dvc-pull

# 3. Lancer l'application
make run
```

### Tests
```bash
# Lancer les tests
make test

# Tests avec couverture
make test-cov
```

### Déploiement
```bash
# Construire l'image Docker
make docker-build

# Lancer avec Docker Compose
make docker-compose-up
```

---

## ❓ Problèmes courants

### "make: command not found" (Windows)
- Installer Make via Chocolatey ou utiliser les commandes directes
- Ou utiliser le script PowerShell `run.ps1`

### "make: command not found" (Linux/macOS)
- Installer Make : `sudo apt-get install make` (Linux) ou `brew install make` (macOS)

### Les commandes ne fonctionnent pas
- Vérifier que vous êtes dans le bon répertoire (celui contenant le Makefile)
- Vérifier que les outils requis sont installés (Python, pip, etc.)

---

## 💡 Astuces

1. **Utilisez `make help`** pour voir toutes les commandes disponibles
2. **Sur Windows**, le script PowerShell `run.ps1` est plus pratique que Make
3. **Vérifiez les prérequis** avant d'exécuter les commandes (Python, Docker, etc.)
4. **Utilisez un environnement virtuel** avant d'installer les dépendances

