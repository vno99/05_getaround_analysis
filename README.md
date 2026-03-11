---
title: Projet Getaround
pinned: false
---

# Projet Getaround

## Description du Projet

Getaround est une plateforme d'autopartage permettant de louer des véhicules pour quelques heures ou quelques jours.
Ce projet répond à 2 problématiques:
* Gestion des retards: les retards lors de la restitution des véhicules créent des frictions pour les locataires suivants
* Optimisation des revenus: aider les propriétaires à fixer des prix optimaux grâce au Machine learning

## Objectifs

* Analyse de données: Evaluer l'impact d'un délai minimum sur les revenus des propriétaires et sur la résolution des problèmes de retard
* Dashboard interactif: Créer un tableau de bord pour explorer différents scénarios de seuils et de périmètres
* API: Déployer une API capable de prédire le prix de location journalier d'un véhicule

## Données

* get_around_delay_analysis.xlsx: Dataset des délais
21 310 lignes, 7 colonnes
* get_around_pricing_project.csv: Dataset des prix de location
4 843 lignes, 15 colonnes

## Méthodologie

* Analyse exploratoire
* Dashboard Streamlit
* Prédiction de prix

## Structure du projet

* ```api/```: Code de l'API
* ```dashboard/```: Code du dashboard Streamlit
* ```data/```: Jeux de données
* ```images/```: Images utilisées dans les notebooks
* ```mlflow/```: Fichiers pour le déploiement de Mlflow pour le suivi des expériences
* ```notebook/```: Notebooks Jypiter

## Installation locale et utilisation

### Prérequis

* Python 3.x
* pip, conda
* Bibliothèques contenus dans `requirements.txt`

### Dashboard
Dans le dossier ```dashboard/```

Création de l'image Docker
```docker build . -t getaround_dashboard```

Lancement
```docker run -it -v "$(pwd):/home/app" -e PORT=80 -p 4001:80 getaround_dashboard```

Url
```http://localhost:4001/```

### API
Dans le dossier ```api/```

Création de l'image Docker
```docker build . -t getaround_api```

Lancement
```docker run -it -v "$(pwd):/home/user/app" -e PORT=4000 -p 4000:4000 getaround_api uvicorn app:app --host 0.0.0.0 --port 4000 --reload```

Url de l'API
```http://localhost:4000/```

Url de la doc
```http://localhost:4000/docs```

#### Fichier .env à compléter pour l'API local
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
MLFLOW_URI=
```

## Production

### Github
https://github.com/vno99/05_getaround_analysis

### Dashboard
https://jiro99-getaround-dashboard.hf.space/

### API
https://jiro99-getaround-api.hf.space
https://jiro99-getaround-api.hf.space/docs

### Mlflow
https://jiro99-mlflow2.hf.space/
