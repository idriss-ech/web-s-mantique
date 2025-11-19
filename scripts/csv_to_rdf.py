#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de transformation des données d'accidents routiers CSV vers RDF
Auteur: Projet Web Sémantique
Date: 2024
"""

import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD, OWL
from rdflib.namespace import FOAF
from datetime import datetime
import os

# =====================================================================
# CONFIGURATION
# =====================================================================

# Chemins des fichiers
DATA_DIR = "data"
OUTPUT_DIR = "output"
ONTOLOGY_FILE = "ontologie/accidents_routiers.ttl"

# Fichiers CSV principaux
CARAC_FILE = os.path.join(DATA_DIR, "caract-2024.csv")
LIEUX_FILE = os.path.join(DATA_DIR, "lieux-2024.csv")
USAGERS_FILE = os.path.join(DATA_DIR, "usagers-2024.csv")
VEHICULES_FILE = os.path.join(DATA_DIR, "vehicules-2024.csv")

# Fichiers de référence (mappings)
REF_DIR = os.path.join(DATA_DIR, "ref-carac")
REF_LIEUX_DIR = os.path.join(DATA_DIR, "ref_lieux")
REF_USAG_DIR = os.path.join(DATA_DIR, "ref-usag")
REF_VEH_DIR = os.path.join(DATA_DIR, "ref-veh")

# Namespaces RDF
ONTO = Namespace("http://www.semanticweb.org/ontologies/accidents-routiers#")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
DBO = Namespace("http://dbpedia.org/ontology/")
DBR = Namespace("http://dbpedia.org/resource/")
SCHEMA = Namespace("http://schema.org/")

# =====================================================================
# FONCTIONS UTILITAIRES
# =====================================================================

def clean_value(value):
    """Nettoie une valeur CSV"""
    if pd.isna(value) or value in ['N/A', '', ' ', '-1', -1]:
        return None
    if isinstance(value, str):
        return value.strip()
    return value

def create_uri(base, id_value):
    """Crée une URI RDF"""
    clean_id = str(id_value).replace(" ", "_").replace("/", "_")
    return URIRef(f"{base}{clean_id}")

def load_csv_safe(filepath, sep=';', encoding='utf-8'):
    """Charge un CSV avec gestion d'erreurs"""
    try:
        df = pd.read_csv(filepath, sep=sep, encoding=encoding, low_memory=False)
        print(f"✅ Chargé : {filepath} ({len(df)} lignes)")
        return df
    except FileNotFoundError:
        print(f"⚠️  Fichier non trouvé : {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erreur lecture {filepath} : {e}")
        return pd.DataFrame()

def load_reference_mapping(filepath, code_col='Code', desc_col='Description'):
    """Charge un fichier de référence et retourne un dictionnaire"""
    try:
        df = pd.read_csv(filepath, sep=',', encoding='utf-8')
        return dict(zip(df[code_col].astype(str), df[desc_col]))
    except Exception as e:
        print(f"⚠️  Erreur mapping {filepath}: {e}")
        return {}

# =====================================================================
# CHARGEMENT DES DONNÉES
# =====================================================================

def load_all_data():
    """Charge tous les fichiers CSV"""
    print("\n" + "="*60)
    print("📂 CHARGEMENT DES DONNÉES")
    print("="*60)
    
    # Données principales
    df_carac = load_csv_safe(CARAC_FILE)
    df_lieux = load_csv_safe(LIEUX_FILE)
    df_usagers = load_csv_safe(USAGERS_FILE)
    df_vehicules = load_csv_safe(VEHICULES_FILE)
    
    # Mappings de référence
    mappings = {
        'lum': load_reference_mapping(os.path.join(REF_DIR, 'lum.csv'), 'id', 'lib'),
        'atm': load_reference_mapping(os.path.join(REF_DIR, 'Conditions_atmo.csv'), 'id', 'lib'),
        'col': load_reference_mapping(os.path.join(REF_DIR, 'Type_col.csv'), 'id', 'lib'),
        'int': load_reference_mapping(os.path.join(REF_DIR, 'Intersection.csv'), 'id', 'lib'),
        'grav': load_reference_mapping(os.path.join(REF_USAG_DIR, 'grav.csv')),
        'catu': load_reference_mapping(os.path.join(REF_USAG_DIR, 'catu.csv')),
        'sexe': load_reference_mapping(os.path.join(REF_USAG_DIR, 'sexe.csv')),
        'catv': load_reference_mapping(os.path.join(REF_VEH_DIR, 'Catv.csv'), 'ID', 'Description'),
        'catr': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'catr.csv')),
    }
    
    return df_carac, df_lieux, df_usagers, df_vehicules, mappings

# =====================================================================
# GÉNÉRATION DU GRAPHE RDF
# =====================================================================

def create_accident_triples(g, row, mappings):
    """Crée les triplets RDF pour un accident"""
    num_acc = clean_value(row['Num_Acc'])
    if not num_acc:
        return
    
    # URI de l'accident
    accident_uri = create_uri(ONTO, f"Accident_{num_acc}")
    
    # Type
    g.add((accident_uri, RDF.type, ONTO.Accident))
    
    # Propriétés basiques
    g.add((accident_uri, ONTO.numeroAccident, Literal(num_acc, datatype=XSD.string)))
    
    # Date
    jour = clean_value(row['jour'])
    mois = clean_value(row['mois'])
    an = clean_value(row['an'])
    
    if jour and mois and an:
        try:
            date_str = f"{an}-{mois.zfill(2)}-{jour.zfill(2)}"
            g.add((accident_uri, ONTO.dateAccident, Literal(date_str, datatype=XSD.date)))
            g.add((accident_uri, ONTO.jour, Literal(int(jour), datatype=XSD.integer)))
            g.add((accident_uri, ONTO.mois, Literal(int(mois), datatype=XSD.integer)))
            g.add((accident_uri, ONTO.annee, Literal(int(an), datatype=XSD.integer)))
        except:
            pass
    
    # Heure
    hrmn = clean_value(row['hrmn'])
    if hrmn:
        g.add((accident_uri, ONTO.heureAccident, Literal(hrmn, datatype=XSD.string)))
    
    # Luminosité
    lum = clean_value(row['lum'])
    if lum and lum in mappings['lum']:
        lum_label = mappings['lum'][lum]
        lum_uri = create_uri(ONTO, f"Luminosite_{lum}")
        g.add((lum_uri, RDF.type, ONTO.ConditionLuminosite))
        g.add((lum_uri, RDFS.label, Literal(lum_label, lang='fr')))
        g.add((accident_uri, ONTO.aConditionLuminosite, lum_uri))
    
    # Conditions atmosphériques
    atm = clean_value(row['atm'])
    if atm and atm in mappings['atm']:
        atm_label = mappings['atm'][atm]
        atm_uri = create_uri(ONTO, f"Atmosphere_{atm}")
        g.add((atm_uri, RDF.type, ONTO.ConditionAtmospherique))
        g.add((atm_uri, RDFS.label, Literal(atm_label, lang='fr')))
        g.add((accident_uri, ONTO.aConditionAtmospherique, atm_uri))
    
    # Type de collision
    col = clean_value(row['col'])
    if col and col in mappings['col']:
        col_label = mappings['col'][col]
        col_uri = create_uri(ONTO, f"Collision_{col}")
        g.add((col_uri, RDF.type, ONTO.TypeCollision))
        g.add((col_uri, RDFS.label, Literal(col_label, lang='fr')))
        g.add((accident_uri, ONTO.aTypeCollision, col_uri))
    
    # Département
    dep = clean_value(row['dep'])
    if dep:
        dep_uri = create_uri(ONTO, f"Departement_{dep}")
        g.add((dep_uri, RDF.type, ONTO.Departement))
        g.add((dep_uri, ONTO.codeDepartement, Literal(dep, datatype=XSD.string)))
    
    # Agglomération
    agg = clean_value(row['agg'])
    if agg:
        is_agg = (agg == '2')
        g.add((accident_uri, ONTO.enAgglomeration, Literal(is_agg, datatype=XSD.boolean)))
    
    # Coordonnées GPS
    lat = clean_value(row['lat'])
    lon = clean_value(row['long'])
    if lat and lon:
        try:
            lieu_uri = create_uri(ONTO, f"Lieu_{num_acc}")
            g.add((lieu_uri, RDF.type, ONTO.Lieu))
            g.add((lieu_uri, ONTO.latitude, Literal(float(lat), datatype=XSD.decimal)))
            g.add((lieu_uri, ONTO.longitude, Literal(float(lon), datatype=XSD.decimal)))
            g.add((lieu_uri, GEO.lat, Literal(float(lat), datatype=XSD.decimal)))
            g.add((lieu_uri, GEO.long, Literal(float(lon), datatype=XSD.decimal)))
            g.add((accident_uri, ONTO.aLieu, lieu_uri))
            
            # Lien département
            if dep:
                g.add((lieu_uri, ONTO.dansDepartement, dep_uri))
        except:
            pass
    
    return accident_uri

def create_lieu_triples(g, row, mappings):
    """Crée les triplets RDF pour un lieu"""
    num_acc = clean_value(row['Num_Acc'])
    if not num_acc:
        return
    
    lieu_uri = create_uri(ONTO, f"Lieu_{num_acc}")
    g.add((lieu_uri, RDF.type, ONTO.Lieu))
    
    # Nom de la voie
    voie = clean_value(row['voie'])
    if voie:
        g.add((lieu_uri, ONTO.nomVoie, Literal(voie, datatype=XSD.string)))
    
    # Catégorie de route
    catr = clean_value(row['catr'])
    if catr and catr in mappings['catr']:
        catr_label = mappings['catr'][catr]
        catr_uri = create_uri(ONTO, f"CategorieRoute_{catr}")
        g.add((catr_uri, RDF.type, ONTO.CategorieRoute))
        g.add((catr_uri, RDFS.label, Literal(catr_label, lang='fr')))
        g.add((lieu_uri, ONTO.aCategorieRoute, catr_uri))
    
    # Nombre de voies
    nbv = clean_value(row['nbv'])
    if nbv:
        try:
            g.add((lieu_uri, ONTO.nombreVoies, Literal(int(nbv), datatype=XSD.integer)))
        except:
            pass
    
    # Vitesse max autorisée
    vma = clean_value(row['vma'])
    if vma:
        try:
            g.add((lieu_uri, ONTO.vitesseMaxAutorisee, Literal(int(vma), datatype=XSD.integer)))
        except:
            pass

def create_usager_triples(g, row, mappings):
    """Crée les triplets RDF pour un usager"""
    num_acc = clean_value(row['Num_Acc'])
    id_usager = clean_value(row['id_usager'])
    
    if not num_acc or not id_usager:
        return
    
    # URI de l'usager
    usager_uri = create_uri(ONTO, f"Usager_{id_usager}")
    g.add((usager_uri, RDF.type, ONTO.Usager))
    g.add((usager_uri, ONTO.identifiantUsager, Literal(id_usager, datatype=XSD.string)))
    
    # Lien avec l'accident
    accident_uri = create_uri(ONTO, f"Accident_{num_acc}")
    g.add((accident_uri, ONTO.implique_usager, usager_uri))
    
    # Sexe
    sexe = clean_value(row['sexe'])
    if sexe and sexe in mappings['sexe']:
        sexe_label = mappings['sexe'][sexe]
        g.add((usager_uri, ONTO.sexe, Literal(sexe_label, datatype=XSD.string)))
        g.add((usager_uri, FOAF.gender, Literal(sexe_label, datatype=XSD.string)))
    
    # Année de naissance et âge
    an_nais = clean_value(row['an_nais'])
    if an_nais:
        try:
            an_nais_int = int(an_nais)
            g.add((usager_uri, ONTO.anneeNaissance, Literal(an_nais_int, datatype=XSD.integer)))
            age = 2024 - an_nais_int
            g.add((usager_uri, ONTO.age, Literal(age, datatype=XSD.integer)))
        except:
            pass
    
    # Gravité
    grav = clean_value(row['grav'])
    if grav and grav in mappings['grav']:
        grav_label = mappings['grav'][grav]
        grav_uri = create_uri(ONTO, f"Gravite_{grav}")
        g.add((grav_uri, RDF.type, ONTO.Gravite))
        g.add((grav_uri, RDFS.label, Literal(grav_label, lang='fr')))
        g.add((usager_uri, ONTO.aGravite, grav_uri))
    
    # Catégorie usager (conducteur/passager)
    catu = clean_value(row['catu'])
    if catu and catu in mappings['catu']:
        catu_label = mappings['catu'][catu]
        catu_uri = create_uri(ONTO, f"CategorieUsager_{catu}")
        g.add((catu_uri, RDF.type, ONTO.CategorieUsager))
        g.add((catu_uri, RDFS.label, Literal(catu_label, lang='fr')))
        g.add((usager_uri, ONTO.aCategorieUsager, catu_uri))
    
    # Lien avec le véhicule
    id_vehicule = clean_value(row['id_vehicule'])
    if id_vehicule:
        vehicule_uri = create_uri(ONTO, f"Vehicule_{id_vehicule}")
        if catu == '1':  # Conducteur
            g.add((usager_uri, ONTO.conduisait, vehicule_uri))
        else:  # Passager
            g.add((usager_uri, ONTO.passagerDe, vehicule_uri))

def create_vehicule_triples(g, row, mappings):
    """Crée les triplets RDF pour un véhicule"""
    num_acc = clean_value(row['Num_Acc'])
    id_vehicule = clean_value(row['id_vehicule'])
    
    if not num_acc or not id_vehicule:
        return
    
    # URI du véhicule
    vehicule_uri = create_uri(ONTO, f"Vehicule_{id_vehicule}")
    g.add((vehicule_uri, RDF.type, ONTO.Vehicule))
    g.add((vehicule_uri, ONTO.identifiantVehicule, Literal(id_vehicule, datatype=XSD.string)))
    
    # Lien avec l'accident
    accident_uri = create_uri(ONTO, f"Accident_{num_acc}")
    g.add((accident_uri, ONTO.implique_vehicule, vehicule_uri))
    
    # Catégorie de véhicule
    catv = clean_value(row['catv'])
    if catv and catv in mappings['catv']:
        catv_label = mappings['catv'][catv]
        catv_uri = create_uri(ONTO, f"CategorieVehicule_{catv}")
        g.add((catv_uri, RDF.type, ONTO.CategorieVehicule))
        g.add((catv_uri, RDFS.label, Literal(catv_label, lang='fr')))
        g.add((vehicule_uri, ONTO.aCategorieVehicule, catv_uri))

# =====================================================================
# FONCTION PRINCIPALE
# =====================================================================

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🚀 TRANSFORMATION CSV → RDF")
    print("="*60)
    
    # Créer le dossier de sortie
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Charger les données
    df_carac, df_lieux, df_usagers, df_vehicules, mappings = load_all_data()
    
    # Créer le graphe RDF
    print("\n" + "="*60)
    print("🔨 GÉNÉRATION DU GRAPHE RDF")
    print("="*60)
    
    g = Graph()
    
    # Bind namespaces
    g.bind("", ONTO)
    g.bind("geo", GEO)
    g.bind("dbo", DBO)
    g.bind("dbr", DBR)
    g.bind("schema", SCHEMA)
    g.bind("foaf", FOAF)
    g.bind("owl", OWL)
    
    # Charger l'ontologie
    try:
        g.parse(ONTOLOGY_FILE, format="turtle")
        print(f"✅ Ontologie chargée : {ONTOLOGY_FILE}")
    except Exception as e:
        print(f"⚠️  Impossible de charger l'ontologie : {e}")
    
    # Traiter les accidents
    print("\n📍 Traitement des accidents...")
    for idx, row in df_carac.iterrows():
        create_accident_triples(g, row, mappings)
        if (idx + 1) % 100 == 0:
            print(f"   ➜ {idx + 1} accidents traités")
    
    # Traiter les lieux
    print("\n📍 Traitement des lieux...")
    for idx, row in df_lieux.iterrows():
        create_lieu_triples(g, row, mappings)
    
    # Traiter les usagers
    print("\n👤 Traitement des usagers...")
    for idx, row in df_usagers.iterrows():
        create_usager_triples(g, row, mappings)
    
    # Traiter les véhicules
    print("\n🚗 Traitement des véhicules...")
    for idx, row in df_vehicules.iterrows():
        create_vehicule_triples(g, row, mappings)
    
    # Sauvegarder le graphe
    output_file = os.path.join(OUTPUT_DIR, "accidents_rdf.ttl")
    g.serialize(destination=output_file, format='turtle')
    
    print("\n" + "="*60)
    print("✅ GÉNÉRATION TERMINÉE")
    print("="*60)
    print(f"📊 Nombre de triplets : {len(g)}")
    print(f"💾 Fichier généré : {output_file}")
    print(f"📏 Taille : {os.path.getsize(output_file) / 1024:.2f} KB")
    print("\n🎯 Prochaine étape : Charger ce fichier dans GraphDB !")

if __name__ == "__main__":
    main()