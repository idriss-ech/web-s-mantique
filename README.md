
# Projet Web Sémantique - Accidents Routiers en France

![UGA Logo](assets/uga_logo.png)

**Master 2 Génie Informatique - IM2AG**  
*Université Grenoble Alpes*

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/idriss-ech/web-s-mantique)
[![Branch](https://img.shields.io/badge/Branch-dev-green?style=for-the-badge&logo=git)](https://github.com/idriss-ech/web-s-mantique/tree/dev)


---


## Description


Ce projet implémente une **ontologie sémantique complète** pour l'analyse des accidents routiers en France. Il transforme les données BAAC (Bulletin d'Analyse des Accidents Corporels) en graphe RDF, permettant des requêtes SPARQL avancées et une intégration avec DBpedia.

---


## Objectifs du Projet


- Créer une ontologie OWL complète pour les accidents routiers
- Convertir les données CSV en format RDF/Turtle
- Intégrer les données géographiques avec DBpedia
- Permettre des requêtes SPARQL complexes sur les données d'accidents

---


## Technologies & Outils


![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Protégé](https://img.shields.io/badge/Protégé-OWL_Editor-orange?style=for-the-badge)
![GraphDB](https://img.shields.io/badge/GraphDB-SPARQL_Engine-blue?style=for-the-badge)
![RDFLib](https://img.shields.io/badge/RDFLib-Python_Library-green?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717?style=for-the-badge&logo=github)

### Stack Technique

- **Langage** : Python 3.8+
- **Bibliothèque RDF** : RDFLib
- **Éditeur d'ontologie** : Protégé 5.x
- **Triplestore** : GraphDB / Apache Jena Fuseki
- **IDE** : Visual Studio Code
- **Gestion de versions** : Git & GitHub

---


## Architecture du Projet


![Data Conception](assets/data_conception.png)

Le projet se compose de **4 classes principales** interconnectées :

### Accident
Caractéristiques temporelles et géographiques de l'événement

### Lieu
Détails de la localisation et infrastructure routière

### Véhicule
Informations sur les véhicules impliqués

### Usager
Données sur les personnes impliquées

---


## Structure du Projet


```bash
projet/
├── ontology/
│   └── ontologi25.ttl          # Ontologie OWL complète
├── scripts/
│   └── csv25.py                # Script de conversion CSV → RDF
├── data/
│   ├── caract-2024.csv         # Caractéristiques des accidents
│   ├── lieux-2024.csv          # Données de localisation
│   ├── vehicules-2024.csv      # Informations véhicules
│   ├── usagers-2024.csv        # Données usagers
│   ├── ref-carac/              # Référentiels caractéristiques
│   ├── ref_lieux/              # Référentiels lieux
│   ├── ref-veh/                # Référentiels véhicules
│   └── ref-usag/               # Référentiels usagers
├── output/
│   └── accidents25.ttl         # Graphe RDF généré (sortie)
├── resultats_sparql/           # Résultats des requêtes SPARQL (CSV)
├── assets/                     # Images et documentation
└── README.md                   # Ce fichier
```

---


## Source des Données

[![Data Source](https://img.shields.io/badge/Data-data.gouv.fr-blue?style=for-the-badge)](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)

Les données proviennent de la **[base BAAC (Bulletins d'Analyse des Accidents Corporels)](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)** mise à disposition par le gouvernement français sur data.gouv.fr.

**Dataset utilisé :** Bases de données annuelles des accidents corporels de la circulation routière - **Année 2024 uniquement**

> **Note :** Ce projet se concentre exclusivement sur les données de l'année 2024. Le dataset complet couvre les années 2005 à 2024, mais seules les données 2024 ont été utilisées pour cette analyse.

Les fichiers de référence permettent de convertir les codes BAAC en libellés lisibles (ex: code "1" → "Plein jour" pour la luminosité).

---


## Installation et Utilisation


### Prérequis
```bash
Python 3.8+
pip install rdflib
```

### Étapes d'exécution


**1. Cloner le projet**
```bash
git clone https://github.com/idriss-ech/web-s-mantique.git
cd web-s-mantique
git checkout dev
```

**2. Créer l'environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

**3. Installer les dépendances**
```bash
pip install rdflib
```


**4. Générer le graphe RDF**
```bash
python scripts/csv25.py
```


**Résultat :** Le fichier `output/accidents25.ttl` est créé avec le graphe RDF complet

---


## Ontologie


L'ontologie comprend **45 propriétés de données** couvrant **100%** des champs BAAC.

### Classes Principales

| Classe | Description | URI |
|--------|-------------|-----|
| `Accident` | Événement accidentel | `:Accident` |
| `Lieu` | Localisation et infrastructure | `:Lieu` |
| `Vehicule` | Véhicules impliqués | `:Vehicule` |
| `Usager` | Personnes impliquées | `:Usager` |

### Propriétés Objets

- `aLieu` : Accident → Lieu
- `impliqueVehicule` : Accident → Vehicule
- `impliqueUsager` : Accident → Usager
- `occupationVehicule` : Usager → Vehicule
- `departementDBpedia` : Accident → DBpedia Resource

### Namespaces Utilisés

```turtle
@prefix : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix dbo: <http://dbpedia.org/ontology/> .
```

---


## Exemples de Requêtes SPARQL


### Requête 1 : Accidents par département

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?accident ?dept (COUNT(?usager) as ?nbUsagers)
WHERE {
  ?accident a :Accident ;
            :departement ?dept ;
            :impliqueUsager ?usager .
}
GROUP BY ?accident ?dept
ORDER BY DESC(?nbUsagers)
LIMIT 10
```

📊 [Voir les résultats](resultats_sparql/accidents_par_departement.csv)

### Requête 2 : Données piétons

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?usager ?localisation ?action ?etat
WHERE {
  ?usager a :Usager ;
          :categorieUsager "Piéton" ;
          :localisationPieton ?localisation ;
          :actionPieton ?action ;
          :etatPieton ?etat .
}
LIMIT 50
```

📊 [Voir les résultats](resultats_sparql/donnees_pietons.csv)

### Requête 3 : Intégration DBpedia (URL Cliquable)

**Important :** Cette requête retourne l'**URI DBpedia cliquable** du département !

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?accident ?dbpediaDept ?deptName ?population ?superficie 
WHERE {
  ?accident a :Accident ;
            :departementDBpedia ?dbpediaDept .
  
  SERVICE <http://fr.dbpedia.org/sparql> {
    ?dbpediaDept rdfs:label ?deptName ;
                 dbo:populationTotal ?population ;
                 dbo:areaTotal ?superficie .
    FILTER(lang(?deptName) = "fr")
  }
}
LIMIT 20
```

> **Note :** La colonne `?dbpediaDept` contient l'URI cliquable (ex: `http://fr.dbpedia.org/resource/Guadeloupe`) que vous pouvez cliquer dans GraphDB/Protégé pour accéder aux données complètes du département sur DBpedia.

📊 [Voir les résultats](resultats_sparql/dbpedia_departements.csv)

### Requête 4 : Accidents mortels par condition météo

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?conditionAtmo (COUNT(?accident) as ?nbAccidents) 
       (COUNT(DISTINCT ?usagerDecede) as ?nbDeces)
WHERE {
  ?accident a :Accident ;
            :conditionAtmospherique ?conditionAtmo ;
            :impliqueUsager ?usagerDecede .
  ?usagerDecede :gravite "Tué" .
}
GROUP BY ?conditionAtmo
ORDER BY DESC(?nbDeces)
```

📊 [Voir les résultats](resultats_sparql/accidents_mortels_meteo.csv)

### Requête 5 : Types de véhicules impliqués

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?categorieVehicule (COUNT(?vehicule) as ?nombre)
WHERE {
  ?accident a :Accident ;
            :impliqueVehicule ?vehicule .
  ?vehicule :categorieVehicule ?categorieVehicule .
}
GROUP BY ?categorieVehicule
ORDER BY DESC(?nombre)
LIMIT 15
```

📊 [Voir les résultats](resultats_sparql/types_vehicules.csv)

### Requête 6 : Accidents selon la luminosité

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?luminosite (COUNT(?accident) as ?nbAccidents)
WHERE {
  ?accident a :Accident ;
            :luminosite ?luminosite .
}
GROUP BY ?luminosite
ORDER BY DESC(?nbAccidents)
```

📊 [Voir les résultats](resultats_sparql/accidents_luminosite.csv)

### Requête 7 : Accidents sur voies réservées (pistes cyclables)

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?accident ?voieReservee ?categorieRoute
WHERE {
  ?accident a :Accident ;
            :aLieu ?lieu .
  ?lieu :voieReservee ?voieReservee ;
        :categorieRoute ?categorieRoute .
  FILTER(?voieReservee != "")
}
LIMIT 50
```

📊 [Voir les résultats](resultats_sparql/accidents_voies_reservees.csv)

### Requête 8 : Profil des victimes (âge, sexe, gravité)

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?sexe ?gravite (COUNT(?usager) as ?nombre) 
       (AVG(2024 - ?anneeNaissance) as ?ageMoyen)
WHERE {
  ?accident a :Accident ;
            :impliqueUsager ?usager .
  ?usager :sexe ?sexe ;
          :gravite ?gravite ;
          :anneeNaissance ?anneeNaissance .
}
GROUP BY ?sexe ?gravite
ORDER BY ?sexe ?gravite
```

📊 [Voir les résultats](resultats_sparql/profil_victimes.csv)

### Requête 9 : Localisation et action des piétons

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/accidents-routiers-v2#>

SELECT ?localisationPieton ?actionPieton ?etatPieton (COUNT(?pieton) as ?nombre)
WHERE {
  ?accident a :Accident ;
            :impliqueUsager ?pieton .
  ?pieton :categorieUsager "Piéton" ;
          :localisationPieton ?localisationPieton ;
          :actionPieton ?actionPieton ;
          :etatPieton ?etatPieton .
}
GROUP BY ?localisationPieton ?actionPieton ?etatPieton
ORDER BY DESC(?nombre)
LIMIT 20
```

📊 [Voir les résultats](resultats_sparql/pietons_localisation.csv)

---


## Caractéristiques Principales



| Fonctionnalité | Status |
|:---------------|:------:|
| Couverture complète des champs CSV | 100% |
| Architecture OWL solide | Validée |
| Intégration DBpedia | Opérationnelle |
| Conversion codes → libellés | Complète |
| Requêtes SPARQL avancées | Supportées |
| Documentation complète | Fournie |


---


## Statistiques du Projet


| Métrique | Valeur |
|:---------|:-------|
| **Propriétés de données** | 45 |
| **Classes principales** | 4 |
| **Propriétés objets** | 5 |
| **Fichiers CSV sources** | 4 |
| **Fichiers de référence** | 17 |
| **Triples RDF générés** | ~2M+ |
| **Taille fichier RDF** | ~200 MB |

---


## Documentation


- [Ontologie](ontology/ontologi25.ttl) - Fichier OWL complet
- [Script Python](scripts/csv25.py) - Code de conversion
- [Description des données](description%20de%20jeu%20de%20donnees.pdf) - Documentation BAAC
- [Relations](relations.pdf) - Schéma des relations

---


## Réalisé par

- **Idriss Echakouki**  
- **Beandapa Yannick**  

Master 2 Génie Informatique - IM2AG  
Université Grenoble Alpes

[![GitHub](https://img.shields.io/badge/GitHub-idriss--ech-181717?style=for-the-badge&logo=github)](https://github.com/idriss-ech)


---

## Licence

Projet académique - M2 GI IM2AG 2024-2025

---


### Liens Utiles

[![Repository](https://img.shields.io/badge/Repository-Main-blue?style=for-the-badge)](https://github.com/idriss-ech/web-s-mantique)
[![Dev Branch](https://img.shields.io/badge/Branch-dev-green?style=for-the-badge)](https://github.com/idriss-ech/web-s-mantique/tree/dev)
[![Data Source](https://img.shields.io/badge/Data-data.gouv.fr-orange?style=for-the-badge)](https://www.data.gouv.fr)
[![DBpedia](https://img.shields.io/badge/DBpedia-Integration-red?style=for-the-badge)](http://fr.dbpedia.org)

---

**Web Sémantique** • **Ontologies OWL** • **RDF/SPARQL** • **Linked Data**

*Projet réalisé dans le cadre du cours de Web Sémantique*

