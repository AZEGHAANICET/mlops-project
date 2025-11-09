# PowerShell script pour remplacer Make sur Windows
# Usage: .\run.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host ""
    Write-Host "🌸 Iris Classifier - Commandes disponibles" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  install         - Install dependencies"
    Write-Host "  train           - Train the model"
    Write-Host "  test            - Launch tests"
    Write-Host "  test-cov        - Test with coverage"
    Write-Host "  run             - Start the application"
    Write-Host "  docker-build    - Build the Docker image"
    Write-Host "  docker-run      - Start the Docker container"
    Write-Host "  docker-up       - Start with Docker Compose"
    Write-Host "  docker-down     - Stop Docker Compose"
    Write-Host "  clean           - Clean temporary files"
    Write-Host "  lint            - Check code quality"
    Write-Host "  dvc-pull        - Download data from DVC"
    Write-Host "  dvc-status      - Check DVC status"
    Write-Host "  help            - Show this help"
    Write-Host ""
}

switch ($Command.ToLower()) {
    "help" {
        Show-Help
    }
    "install" {
        Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
    "train" {
        Write-Host "🎯 Entraînement du modèle..." -ForegroundColor Yellow
        python src/train.py
    }
    "test" {
        Write-Host "🧪 Lancement des tests..." -ForegroundColor Yellow
        pytest
    }
    "test-cov" {
        Write-Host "🧪 Lancement des tests avec couverture..." -ForegroundColor Yellow
        pytest --cov=app --cov=src --cov-report=html --cov-report=term-missing
    }
    "run" {
        Write-Host "🚀 Lancement de l'application..." -ForegroundColor Green
        Write-Host "📍 Application disponible sur http://localhost:8000" -ForegroundColor Cyan
        uvicorn app:app --reload --host 0.0.0.0 --port 8000
    }
    "docker-build" {
        Write-Host "🐳 Construction de l'image Docker..." -ForegroundColor Yellow
        docker build -t iris-classifier .
    }
    "docker-run" {
        Write-Host "🐳 Lancement du conteneur Docker..." -ForegroundColor Yellow
        docker run -p 8000:8080 iris-classifier
    }
    "docker-up" {
        Write-Host "🐳 Démarrage des services Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d
    }
    "docker-down" {
        Write-Host "🐳 Arrêt des services Docker Compose..." -ForegroundColor Yellow
        docker-compose down
    }
    "clean" {
        Write-Host "🧹 Nettoyage des fichiers temporaires..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Directory -Filter "*.egg-info" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force .coverage -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
        Write-Host "✅ Nettoyage terminé!" -ForegroundColor Green
    }
    "lint" {
        Write-Host "🔍 Vérification de la qualité du code..." -ForegroundColor Yellow
        flake8 app.py schemas.py src/ tests/
    }
    "dvc-pull" {
        Write-Host "📥 Téléchargement des données DVC..." -ForegroundColor Yellow
        dvc pull
    }
    "dvc-status" {
        Write-Host "📊 Statut DVC..." -ForegroundColor Yellow
        dvc status
    }
    default {
        Write-Host "❌ Commande inconnue: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
        exit 1
    }
}

