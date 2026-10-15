# 💼 Morocco Job Finder — Système de Recommandation d'Emploi

Système intelligent de recommandation d'offres d'emploi pour le marché marocain, combinant l'API **JSearch** (recherche d'offres en temps réel) et un algorithme de matching **TF-IDF + similarité cosinus**. L'utilisateur peut saisir ses compétences manuellement ou uploader son CV en PDF, et reçoit en retour une liste d'offres classées par score de pertinence.

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [Endpoints API](#endpoints-api)
- [Structure du projet](#structure-du-projet)
- [Évaluation des performances](#évaluation-des-performances)
- [Équipe](#équipe)

## Fonctionnalités

- 🔍 **Recherche par compétences** : saisie manuelle (compétences, expérience, formation) et recommandation des 10 offres les plus pertinentes
- 📄 **Upload CV PDF** : extraction automatique du texte du CV, détection de mots-clés techniques, et recommandation sans saisie manuelle
- 🎯 **Scoring intelligent** : algorithme TF-IDF + similarité cosinus pour classer les offres par pertinence
- 🛡️ **Robustesse** : bascule automatique sur un jeu de données local (`offres_backup.csv`) si l'API JSearch est indisponible ou en quota dépassé
- 🇲🇦 **Marché marocain** : recherche ciblée sur le Maroc (`country=ma`)

## Architecture

```
┌─────────────────┐      HTTP       ┌──────────────────┐      HTTP       ┌─────────────┐
│  Streamlit       │ ──────────────> │  FastAPI          │ ──────────────> │  JSearch API │
│  (app.py)         │ <────────────── │  (main.py)         │ <────────────── │  (RapidAPI)   │
└─────────────────┘                 └──────────────────┘                 └─────────────┘
                                              │
                                              ├──> recommender.py  (TF-IDF + cosine similarity)
                                              ├──> Extractor.py    (extraction PDF, nettoyage texte)
                                              └──> offres_backup.csv (fallback si API indisponible)
```

## Prérequis

- Python 3.11 ou supérieur
- Un compte [RapidAPI](https://rapidapi.com) avec un abonnement à l'API **JSearch**
- Git

## Installation

```bash
git clone https://github.com/fatidevt/pfa-recommandation-emploi.git
cd pfa-recommandation-emploi/frontend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r ../requirements.txt
```

## Configuration

Créez un fichier `.env` **à la racine du projet** (`pfa-recommandation-emploi/.env`, pas dans `frontend/`) avec votre clé JSearch :

```
JSEARCH_API_KEY=votre_cle_rapidapi
```

⚠️ Ne jamais commiter ce fichier — il est exclu via `.gitignore`.

## Lancement

Le projet nécessite **deux serveurs lancés simultanément**, dans deux terminaux séparés.

**Terminal 1 — Backend FastAPI**
```bash
cd frontend
uvicorn main:app --reload
```
Disponible sur `http://127.0.0.1:8000` — documentation interactive Swagger sur `http://127.0.0.1:8000/docs`

**Terminal 2 — Frontend Streamlit**
```bash
cd frontend
streamlit run app.py
```
Disponible sur `http://localhost:8501`

## Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/recommandations` | POST | Recommandation d'offres à partir d'un profil de compétences (JSON) |
| `/upload-cv` | POST | Recommandation d'offres à partir d'un CV PDF uploadé |

### Exemple de requête `/recommandations`

```json
{
  "competences": "python django sql",
  "experience": "2 ans backend developer",
  "formation": "master informatique",
  "location": "Morocco"
}
```

## Structure du projet

```
pfa-recommandation-emploi/
├── .env                      # Cle API (non versionne)
├── .gitignore
├── README.md
├── requirements.txt
└── frontend/
    ├── main.py                # API FastAPI (endpoints, orchestration)
    ├── app.py                 # Interface Streamlit
    ├── recommender.py         # Algorithme TF-IDF + similarite cosinus
    ├── Extractor.py           # Extraction et nettoyage du texte PDF
    ├── jsearch.py             # Client API JSearch
    ├── evaluation.py          # Script d'evaluation Precision@K
    ├── offres_backup.csv      # Jeu de donnees de secours (fallback)
    └── resultats_precision_k.txt  # Resultats de l'evaluation
```

## Évaluation des performances

L'algorithme de recommandation a été évalué avec la métrique **Precision@K** sur 10 profils de test variés (Python, JavaScript, Data Science, DevOps, Java, Réseaux, PHP, Data Analyst, QA, Mobile), avec des offres réelles récupérées via JSearch.

| Métrique | Résultat |
|----------|----------|
| Precision@5 (moyenne) | 90.0% |
| Precision@10 (moyenne) | 83.0% |

Le détail complet par profil est disponible dans `frontend/resultats_precision_k.txt`, généré par :
```bash
python evaluation.py
```

**Limite identifiée** : la couverture de l'API JSearch varie selon les métiers recherchés sur le marché marocain ; certains profils retournent moins d'offres disponibles, ce qui peut limiter mécaniquement le Precision@10. Ce n'est pas un défaut de l'algorithme TF-IDF lui-même, mais une contrainte de la source de données externe — d'où l'intérêt du fallback CSV.

## Équipe

Projet réalisé dans le cadre du **PFA (Projet de Fin d'Année) — Master 1 Ingénierie des Systèmes Informatiques (ISI)**.

| Membre | Rôle principal |
|--------|----------------|
| **Fatima Zahra Fridi** | Algorithme de recommandation (TF-IDF), extraction PDF, évaluation Precision@K |
| **Najib** | API FastAPI, endpoints, gestion d'erreurs, fallback CSV |
| **Nouhaila** | Interface Streamlit, expérience utilisateur, intégration JSearch |

**Établissement** : SUP MTI Rabat — Master 1 ISI — Année universitaire 2025-2026