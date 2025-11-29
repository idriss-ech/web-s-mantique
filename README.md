# Web Sémantique — Fusion de données via Ontologie

## Objectifs du projet
- Trouver plusieurs sources de données, analyser leur structure, construire une ontologie, puis orienter ces données et l’ontologie vers une liste de questions ciblant la fusion.
- Partir d’une ontologie existante, rechercher des jeux de données pour la peupler, observer ses limites et étendre le modèle si nécessaire.
- À partir d’un système avec ontologie et données déjà présentes, réaliser une fusion dans un même graphe.

## Données
Nous avons identifié deux sources de données sur les accidents routiers et procédé à une analyse structurelle avant modélisation.

### Qualité et nettoyage
- Hétérogénéités de codage des valeurs manquantes: `-1`, `0`, chaîne vide `""` ou parfois absence de colonne avaient la même sémantique (valeur inconnue). Nous avons uniformisé en valeur nulle (absence de triplet) pour éviter des faux signaux.
- Normalisation des types: conversion explicite des entiers (ex. `jour`, `mois`, `an`, `grav`) et des chaînes (ex. `hrmn`, `adr`, coordonnées géographiques).
- Réduction de la data:  Nous avons garndé que 1/3 de données pour les tests et avoir des requetes plus rapides

### Limites de la fusion inter‑sources
La fusion automatique des deux bases n’a pas été possible car:
- Les identifiants d'accident (`Num_Acc`) ne correspondaient pas entre les sources.
- Des attributs discriminants manquaient dans la deuxième source (heure précise, géolocalisation fine), empêchant toute stratégie de rapprochement fiable.
- Aucun quasi-identifiant stable (combinaison date + lieu + véhicule) n’était simultanément présent et suffisamment complet dans les deux fichiers.

Conséquence: nous avons choisi une seule des deux bases de données.

## Construction Ontologie
Nous avons suivi deux approches parallèles:

1. Approche « data‑driven »: dériver les classes et propriétés directement des colonnes observées (groupement sémantique des attributs et identification des relations). Cette approche assure une couverture maximale des données mais peut sur‑spécialiser l’ontologie aux structures tabulaires initiales.
2. Approche « ontology‑driven »: partir d’une ontologie existante liée au domaine des accidents et procéder à un élagage (suppression des classes/propriétés non utilisées) puis enrichissement ciblé (ajout de `RoadAccident`, spécialisation des entités humaines en `Man` / `Woman`, intégration des localisations via `Commune` et `Department`).

### Critères de choix retenus
- Lisibilité et maintenabilité: l'ontologie dérivée d'un modèle existant offrait une hiérarchie claire (`Location` > `Commune` / `Department`).
- Parcimonie: remplacement de structures trop fines (anciennes classes spécifiques) par des `datatype properties` quand la granularité ne justifiait pas une instanciation séparée.
- Alignabilité: possibilité future de lier `Department` à des référentiels externes.

### Décisions de modélisation
- Utilisation de `RoadAccident` comme classe centrale liant personnes (`Person` / `Man` / `Woman`), véhicules (`Vehicle`) et localisation (`Location`).
- Les caractéristiques contextuelles (luminosité `lum`, gravité `grav`, catégorie véhicule `catv`) sont des `datatype properties` pour faciliter l’agrégation SPARQL (pas d’explosion du graphe).
- Les relations dynamiques (`hasLocation`, `driverOf`, `occupantOf`, `vehicleInvolvedIn`, `involvedIn`) sont des `object properties` permettant d'étendre ultérieurement avec des règles ou de l'inférence.

Conclusion: nous avons conservé et étendu l’ontologie existante, ce qui offre un meilleur point de départ pour l’interopérabilité et l’évolution (ajout futur de météo, infrastructure, conditions réglementaires).

### Intégration de DBpedia
- Nous avons fait lier `Department` à des référentiels sur les princiapxu precturecues des departmeent sur DBpedia. 
- Nous avons voulu aussi lié les coordonnées de localitaion avec geo mais nous avons manquez malheuressement de temps.




## Structure du dépôt
- `data/`: fichiers CSV sources (caract-2024, lieux-2024, usagers-2024, vehicules-2024, vehicules-immatricule-2024)
- `protege/ontology.ttl`: ontologie au format Turtle (TTL) développée avec Protégé
- `scripts/csv_to_ttl.py`: script de transformation CSV → Turtle
- `output/instances.ttl`: triplestore RDF généré à partir des CSV

## Ontologie (OWL/Turtle)
- L'ontologie est fournie en `TTL` (fichier `protege/ontology.ttl`).
- Elle définit les classes (ex. `RoadAccident`, `Location`, `Person`, `Man`, `Woman`, `Vehicle`, `Department`, `Commune`) et les propriétés d'objet/données :
  - **Object Properties** : `hasLocation`, `inDepartment`, `inCommune`, `driverOf`, `occupantOf`, `involvedIn`, `vehicleInvolvedIn`
  - **Datatype Properties** : `an`, `mois`, `jour`, `hrmn`, `lum`, `agg`, `com`, `dep`, `lat`, `long`, `adr`, `catv`, `catu`, `grav`, `anNais`, `numVeh`, `numVehPers`
- Le choix de `TTL` permet une édition rapide sous Protégé et une sérialisation lisible; elle reste convertible en `OWL/RDF/XML` si nécessaire.
- Les détails des Datatype Properties sont accesible dans le fichier pdf nommné **description-des-bases-de-donnees.pdf**

## Mapping entre données et ontologie
- Le script `scripts/csv_to_ttl.py` fait le **mapping** des colonnes CSV vers les classes/propriétés de l’ontologie.
- Approche adoptée:
  - Normalisation des identifiants (IRIs stables par ligne/clé primaire).
  - Typage RDF (`rdf:type`) basé sur la table source (ex. lignes de `usagers-2024.csv` → instances de `Usager`).
  - Alignement des colonnes avec des `datatype properties` (ex. `age`, `sexe`, `categorieUsager`).
  - Relations entre tables via `object properties` (ex. `Usager` → `Accident`, `Accident` → `Lieu`, `Accident` → `Vehicule`).
- Le résultat est écrit dans `output/instances.ttl`, compatible avec tout triplestore RDF (GraphDB, Fuseki, etc.).

## SPARQL: questions de fusion et d’analyse
Quelques requêtes représentatives à exécuter sur `instances.ttl` + ontologie:
- Distribution des accidents par type de **lieu**:
  - Objectif: détecter des biais géographiques et préparer une agrégation spatiale.
- Corrélation **usagers × gravité × type de véhicule**:
  - Objectif: relier profils d’usagers à la sévérité et aux véhicules impliqués.
- Détection de **doublons** (fusion d’entités) via clés composites (ex. date+lieu+immatriculation):
  - Objectif: fusionner occurrences multi-sources pour une même entité réelle.
- Enrichissement par **référentiels externes** (alignements `owl:sameAs`/`skos:exactMatch`).

> Remarque: si vous utilisez Apache Jena/Fuseki, chargez `protege/ontology.ttl` puis `output/instances.ttl`, et exécutez les requêtes SPARQL dans l’UI.




## Workflow d’exécution
### Prérequis
- Python 3.10+

### Génération des triplets
Dans PowerShell à la racine du projet:
```powershell
py .\scripts\csv_to_ttl.py
```
- Le script lit `data/*.csv` et produit `output/instances.ttl`.
- Re-exécutez après toute mise à jour des CSV ou du mapping.





## Exemples de requêtes SPARQL
À exécuter sur un triplestore après avoir chargé `protege/ontology.ttl` puis `output/instances.ttl`.

- **COUNT des accidents par département** (agrégation basique):

```sparql
PREFIX ra: <http://www.w3.org/2012/7/ra3.owl#>
SELECT ?dep (COUNT(?acc) AS ?nbAcc)
WHERE {
  ?acc a ra:RoadAccident ;
       ra:inDepartment ?dep .
}
GROUP BY ?dep
ORDER BY DESC(?nbAcc)
```

- **GROUP BY gravité**:

```sparql
PREFIX ra: <http://www.w3.org/2012/7/ra3.owl#>
SELECT ?grav (COUNT(*) AS ?nb)
WHERE {
  ?veh a ra:Vehicle ; ra:catv ?catv ; ra:vehicleInvolvedIn ?acc .
  ?pers a ?t ; ra:grav ?grav ; ra:involvedIn ?acc .
}
GROUP BY ?grav
ORDER BY DESC(?nb)
```

- **Accidents= par date** (date):

```sparql
PREFIX ra: <http://www.w3.org/2012/7/ra3.owl#>
SELECT (CONCAT(STR(?an), "-", STR(?mois)) AS ?dedupKey)
       (COUNT(DISTINCT ?acc) AS ?occurrences)
WHERE {
  ?acc a ra:RoadAccident ; ra:an ?an ; ra:mois ?mois ; ra:jour ?jour ; ra:com ?com .
  OPTIONAL {
    ?veh a ra:Vehicle ; ra:vehicleInvolvedIn ?acc ; ra:numVeh ?num .
  }
}
GROUP BY ?an ?mois
HAVING(COUNT(DISTINCT ?acc) > 1)
ORDER BY DESC(?occurrences)
```






