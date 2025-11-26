#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de transformation des données d'accidents routiers CSV vers RDF (VERSION CORRIGÉE)
Corrections: gestion des colonnes, mappings complets, normalisation des types
"""

import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD, OWL
from rdflib.namespace import FOAF
from datetime import datetime
import os

# =====================================================================
# CONFIGURATION
# =====================================================================

DATA_DIR = "data"
OUTPUT_DIR = "output"
ONTOLOGY_FILE = "ontologie/accidents_routiers.ttl"

# Fichiers CSV principaux
CARAC_FILE = os.path.join(DATA_DIR, "caract-2024.csv")
LIEUX_FILE = os.path.join(DATA_DIR, "lieux-2024.csv")
USAGERS_FILE = os.path.join(DATA_DIR, "usagers-2024.csv")
VEHICULES_FILE = os.path.join(DATA_DIR, "vehicules-2024.csv")

# Fichiers de référence
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
    """Nettoie une valeur CSV avec gestion robuste"""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip().strip('"').strip("'")
        if value in ['N/A', '', ' ', '-1', 'nan']:
            return None
    if value == -1:
        return None
    return value

def normalize_code(code):
    """Normalise un code pour le matching (string sans espaces)"""
    if code is None:
        return None
    return str(code).strip()

def create_uri(base, id_value):
    """Crée une URI RDF valide"""
    if id_value is None:
        return None
    clean_id = str(id_value).replace(" ", "_").replace("/", "_").replace("'", "")
    return URIRef(f"{base}{clean_id}")

def load_csv_safe(filepath, sep=';', encoding='utf-8'):
    """Charge un CSV avec nettoyage des noms de colonnes"""
    try:
        df = pd.read_csv(filepath, sep=sep, encoding=encoding, low_memory=False)
        # IMPORTANT: Nettoyer les noms de colonnes (enlever guillemets et espaces)
        df.columns = df.columns.str.strip().str.strip('"').str.strip("'")
        print(f"✅ Chargé : {filepath} ({len(df)} lignes, {len(df.columns)} colonnes)")
        print(f"   Colonnes: {list(df.columns)[:5]}...")
        return df
    except FileNotFoundError:
        print(f"⚠️  Fichier non trouvé : {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erreur lecture {filepath} : {e}")
        return pd.DataFrame()

def load_reference_mapping(filepath, code_col='Code', desc_col='Description', sep=','):
    """Charge un fichier de référence avec normalisation des clés"""
    try:
        df = pd.read_csv(filepath, sep=sep, encoding='utf-8')
        df.columns = df.columns.str.strip().str.strip('"')
        # Normaliser les codes en string
        mapping = {}
        for _, row in df.iterrows():
            code = normalize_code(row[code_col])
            desc = clean_value(row[desc_col])
            if code and desc:
                mapping[code] = desc
        print(f"   ✓ {filepath}: {len(mapping)} entrées")
        return mapping
    except Exception as e:
        print(f"⚠️  Erreur mapping {filepath}: {e}")
        return {}

# =====================================================================
# CHARGEMENT DES DONNÉES
# =====================================================================

def load_all_data():
    """Charge tous les fichiers CSV avec mappings complets"""
    print("\n" + "="*60)
    print("📂 CHARGEMENT DES DONNÉES")
    print("="*60)
    
    # Données principales
    df_carac = load_csv_safe(CARAC_FILE, sep=';')
    df_lieux = load_csv_safe(LIEUX_FILE, sep=';')
    df_usagers = load_csv_safe(USAGERS_FILE, sep=';')
    df_vehicules = load_csv_safe(VEHICULES_FILE, sep=';')
    
    print("\n📋 Chargement des mappings de référence...")
    
    # Mappings de référence COMPLETS
    mappings = {
        # Caractéristiques accident
        'lum': load_reference_mapping(os.path.join(REF_DIR, 'lum.csv'), 'id', 'lib', ';'),
        'atm': load_reference_mapping(os.path.join(REF_DIR, 'Conditions_atmo.csv'), 'id', 'lib', ';'),
        'col': load_reference_mapping(os.path.join(REF_DIR, 'Type_col.csv'), 'id', 'lib', ';'),
        'int': load_reference_mapping(os.path.join(REF_DIR, 'Intersection.csv'), 'id', 'lib', ';'),
        'agg': load_reference_mapping(os.path.join(REF_DIR, 'Localisation.csv'), 'id', 'lib', ';'),
        
        # Caractéristiques lieu
        'catr': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'catr.csv'), sep=','),
        'circ': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'circ.csv'), sep=','),
        'infra': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'infra.csv'), sep=','),
        'plan': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'plan.csv'), sep=','),
        'prof': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'prof.csv'), sep=','),
        'situ': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'situ.csv'), sep=','),
        'surf': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'surf.csv'), sep=','),
        'vosp': load_reference_mapping(os.path.join(REF_LIEUX_DIR, 'vosp.csv'), sep=','),
        
        # Caractéristiques usager
        'grav': load_reference_mapping(os.path.join(REF_USAG_DIR, 'grav.csv'), sep=','),
        'catu': load_reference_mapping(os.path.join(REF_USAG_DIR, 'catu.csv'), sep=','),
        'sexe': load_reference_mapping(os.path.join(REF_USAG_DIR, 'sexe.csv'), sep=','),
        'trajet': load_reference_mapping(os.path.join(REF_USAG_DIR, 'trajet.csv'), sep=','),
        'secu': load_reference_mapping(os.path.join(REF_USAG_DIR, 'secu.csv'), sep=','),
        'place': load_reference_mapping(os.path.join(REF_USAG_DIR, 'place.csv'), sep=','),
        'etatp': load_reference_mapping(os.path.join(REF_USAG_DIR, 'etatp.csv'), sep=','),
        'actp': load_reference_mapping(os.path.join(REF_USAG_DIR, 'actp.csv'), sep=','),
        'locp': load_reference_mapping(os.path.join(REF_USAG_DIR, 'locp.csv'), sep=','),
        
        # Caractéristiques véhicule
        'catv': load_reference_mapping(os.path.join(REF_VEH_DIR, 'Catv.csv'), 'ID', 'Description', ','),
        'choc': load_reference_mapping(os.path.join(REF_VEH_DIR, 'choc.csv'), sep=','),
        'manv': load_reference_mapping(os.path.join(REF_VEH_DIR, 'manv.csv'), sep=','),
        'obs': load_reference_mapping(os.path.join(REF_VEH_DIR, 'obs.csv'), sep=','),
        'obsm': load_reference_mapping(os.path.join(REF_VEH_DIR, 'obsm.csv'), sep=','),
        'senc': load_reference_mapping(os.path.join(REF_VEH_DIR, 'senc.csv'), sep=','),
    }
    
    print(f"\n✅ {len(mappings)} types de mappings chargés")
    
    return df_carac, df_lieux, df_usagers, df_vehicules, mappings

# =====================================================================
# GÉNÉRATION DU GRAPHE RDF
# =====================================================================

def create_accident_triples(g, row, mappings):
    """Crée les triplets RDF pour un accident (VERSION AMÉLIORÉE)"""
    num_acc = clean_value(row.get('Num_Acc'))
    if not num_acc:
        return None
    
    accident_uri = create_uri(ONTO, f"Accident_{num_acc}")
    g.add((accident_uri, RDF.type, ONTO.Accident))
    g.add((accident_uri, ONTO.numeroAccident, Literal(num_acc, datatype=XSD.string)))
    
    # Date et heure
    jour = clean_value(row.get('jour'))
    mois = clean_value(row.get('mois'))
    an = clean_value(row.get('an'))
    
    if jour and mois and an:
        try:
            date_str = f"{an}-{str(mois).zfill(2)}-{str(jour).zfill(2)}"
            g.add((accident_uri, ONTO.dateAccident, Literal(date_str, datatype=XSD.date)))
            g.add((accident_uri, ONTO.jour, Literal(int(jour), datatype=XSD.integer)))
            g.add((accident_uri, ONTO.mois, Literal(int(mois), datatype=XSD.integer)))
            g.add((accident_uri, ONTO.annee, Literal(int(an), datatype=XSD.integer)))
        except Exception as e:
            print(f"   ⚠️ Erreur date pour {num_acc}: {e}")
    
    hrmn = clean_value(row.get('hrmn'))
    if hrmn:
        g.add((accident_uri, ONTO.heureAccident, Literal(str(hrmn), datatype=XSD.string)))
    
    # Luminosité avec normalisation de code
    lum = normalize_code(row.get('lum'))
    if lum and lum in mappings['lum']:
        lum_uri = create_uri(ONTO, f"Luminosite_{lum}")
        g.add((lum_uri, RDF.type, ONTO.ConditionLuminosite))
        g.add((lum_uri, RDFS.label, Literal(mappings['lum'][lum], lang='fr')))
        g.add((accident_uri, ONTO.aConditionLuminosite, lum_uri))
    
    # Conditions atmosphériques
    atm = normalize_code(row.get('atm'))
    if atm and atm in mappings['atm']:
        atm_uri = create_uri(ONTO, f"Atmosphere_{atm}")
        g.add((atm_uri, RDF.type, ONTO.ConditionAtmospherique))
        g.add((atm_uri, RDFS.label, Literal(mappings['atm'][atm], lang='fr')))
        g.add((accident_uri, ONTO.aConditionAtmospherique, atm_uri))
    
    # Type de collision
    col = normalize_code(row.get('col'))
    if col and col in mappings['col']:
        col_uri = create_uri(ONTO, f"Collision_{col}")
        g.add((col_uri, RDF.type, ONTO.TypeCollision))
        g.add((col_uri, RDFS.label, Literal(mappings['col'][col], lang='fr')))
        g.add((accident_uri, ONTO.aTypeCollision, col_uri))
    
    # Type d'intersection
    int_code = normalize_code(row.get('int'))
    if int_code and int_code in mappings['int']:
        int_uri = create_uri(ONTO, f"Intersection_{int_code}")
        g.add((int_uri, RDF.type, ONTO.TypeIntersection))
        g.add((int_uri, RDFS.label, Literal(mappings['int'][int_code], lang='fr')))
        g.add((accident_uri, ONTO.aTypeIntersection, int_uri))
    
    # Département
    dep = clean_value(row.get('dep'))
    if dep:
        dep_uri = create_uri(ONTO, f"Departement_{dep}")
        g.add((dep_uri, RDF.type, ONTO.Departement))
        g.add((dep_uri, ONTO.codeDepartement, Literal(str(dep), datatype=XSD.string)))
    
    # Agglomération
    agg = normalize_code(row.get('agg'))
    if agg:
        is_agg = (agg == '2')
        g.add((accident_uri, ONTO.enAgglomeration, Literal(is_agg, datatype=XSD.boolean)))
    
    # Coordonnées GPS et lieu
    lat = clean_value(row.get('lat'))
    lon = clean_value(row.get('long'))
    
    if lat and lon:
        try:
            lat_float = float(str(lat).replace(',', '.'))
            lon_float = float(str(lon).replace(',', '.'))
            
            lieu_uri = create_uri(ONTO, f"Lieu_{num_acc}")
            g.add((lieu_uri, RDF.type, ONTO.Lieu))
            g.add((lieu_uri, ONTO.latitude, Literal(lat_float, datatype=XSD.decimal)))
            g.add((lieu_uri, ONTO.longitude, Literal(lon_float, datatype=XSD.decimal)))
            g.add((lieu_uri, GEO.lat, Literal(lat_float, datatype=XSD.decimal)))
            g.add((lieu_uri, GEO.long, Literal(lon_float, datatype=XSD.decimal)))
            g.add((accident_uri, ONTO.aLieu, lieu_uri))
            
            if dep:
                g.add((lieu_uri, ONTO.dansDepartement, dep_uri))
        except Exception as e:
            print(f"   ⚠️ Erreur GPS pour {num_acc}: {e}")
    
    # Adresse
    adr = clean_value(row.get('adr'))
    if adr and lat and lon:
        lieu_uri = create_uri(ONTO, f"Lieu_{num_acc}")
        g.add((lieu_uri, ONTO.adresse, Literal(adr, datatype=XSD.string)))
    
    return accident_uri

def create_lieu_triples(g, row, mappings):
    """Crée les triplets RDF pour un lieu (VERSION COMPLÈTE)"""
    num_acc = clean_value(row.get('Num_Acc'))
    if not num_acc:
        return
    
    lieu_uri = create_uri(ONTO, f"Lieu_{num_acc}")
    g.add((lieu_uri, RDF.type, ONTO.Lieu))
    
    # Nom de la voie
    voie = clean_value(row.get('voie'))
    if voie:
        g.add((lieu_uri, ONTO.nomVoie, Literal(voie, datatype=XSD.string)))
    
    # Catégorie de route
    catr = normalize_code(row.get('catr'))
    if catr and catr in mappings['catr']:
        catr_uri = create_uri(ONTO, f"CategorieRoute_{catr}")
        g.add((catr_uri, RDF.type, ONTO.CategorieRoute))
        g.add((catr_uri, RDFS.label, Literal(mappings['catr'][catr], lang='fr')))
        g.add((lieu_uri, ONTO.aCategorieRoute, catr_uri))
    
    # Type de circulation
    circ = normalize_code(row.get('circ'))
    if circ and circ in mappings['circ']:
        circ_uri = create_uri(ONTO, f"TypeCirculation_{circ}")
        g.add((circ_uri, RDF.type, ONTO.TypeCirculation))
        g.add((circ_uri, RDFS.label, Literal(mappings['circ'][circ], lang='fr')))
        g.add((lieu_uri, ONTO.aTypeCirculation, circ_uri))
    
    # Infrastructure
    infra = normalize_code(row.get('infra'))
    if infra and infra in mappings['infra']:
        infra_uri = create_uri(ONTO, f"Infrastructure_{infra}")
        g.add((infra_uri, RDF.type, ONTO.Infrastructure))
        g.add((infra_uri, RDFS.label, Literal(mappings['infra'][infra], lang='fr')))
        g.add((lieu_uri, ONTO.aInfrastructure, infra_uri))
    
    # État de surface
    surf = normalize_code(row.get('surf'))
    if surf and surf in mappings['surf']:
        surf_uri = create_uri(ONTO, f"EtatSurface_{surf}")
        g.add((surf_uri, RDF.type, ONTO.EtatSurface))
        g.add((surf_uri, RDFS.label, Literal(mappings['surf'][surf], lang='fr')))
        g.add((lieu_uri, ONTO.aEtatSurface, surf_uri))
    
    # Nombre de voies
    nbv = clean_value(row.get('nbv'))
    if nbv:
        try:
            g.add((lieu_uri, ONTO.nombreVoies, Literal(int(nbv), datatype=XSD.integer)))
        except:
            pass
    
    # Largeur route
    larrout = clean_value(row.get('larrout'))
    if larrout:
        try:
            g.add((lieu_uri, ONTO.largeurRoute, Literal(float(larrout), datatype=XSD.decimal)))
        except:
            pass
    
    # Vitesse max autorisée
    vma = clean_value(row.get('vma'))
    if vma:
        try:
            g.add((lieu_uri, ONTO.vitesseMaxAutorisee, Literal(int(vma), datatype=XSD.integer)))
        except:
            pass

def create_usager_triples(g, row, mappings):
    """Crée les triplets RDF pour un usager (VERSION COMPLÈTE)"""
    num_acc = clean_value(row.get('Num_Acc'))
    id_usager = clean_value(row.get('id_usager'))
    
    if not num_acc or not id_usager:
        return
    
    usager_uri = create_uri(ONTO, f"Usager_{id_usager}")
    g.add((usager_uri, RDF.type, ONTO.Usager))
    g.add((usager_uri, ONTO.identifiantUsager, Literal(id_usager, datatype=XSD.string)))
    
    # Lien avec l'accident
    accident_uri = create_uri(ONTO, f"Accident_{num_acc}")
    g.add((accident_uri, ONTO.implique_usager, usager_uri))
    
    # Sexe
    sexe = normalize_code(row.get('sexe'))
    if sexe and sexe in mappings['sexe']:
        sexe_label = mappings['sexe'][sexe]
        g.add((usager_uri, ONTO.sexe, Literal(sexe_label, datatype=XSD.string)))
        g.add((usager_uri, FOAF.gender, Literal(sexe_label, datatype=XSD.string)))
    
    # Année de naissance et âge
    an_nais = clean_value(row.get('an_nais'))
    if an_nais:
        try:
            an_nais_int = int(an_nais)
            g.add((usager_uri, ONTO.anneeNaissance, Literal(an_nais_int, datatype=XSD.integer)))
            age = 2024 - an_nais_int
            if 0 <= age <= 120:
                g.add((usager_uri, ONTO.age, Literal(age, datatype=XSD.integer)))
        except:
            pass
    
    # Gravité
    grav = normalize_code(row.get('grav'))
    if grav and grav in mappings['grav']:
        grav_uri = create_uri(ONTO, f"Gravite_{grav}")
        g.add((grav_uri, RDF.type, ONTO.Gravite))
        g.add((grav_uri, RDFS.label, Literal(mappings['grav'][grav], lang='fr')))
        g.add((usager_uri, ONTO.aGravite, grav_uri))
    
    # Catégorie usager
    catu = normalize_code(row.get('catu'))
    if catu and catu in mappings['catu']:
        catu_uri = create_uri(ONTO, f"CategorieUsager_{catu}")
        g.add((catu_uri, RDF.type, ONTO.CategorieUsager))
        g.add((catu_uri, RDFS.label, Literal(mappings['catu'][catu], lang='fr')))
        g.add((usager_uri, ONTO.aCategorieUsager, catu_uri))
    
    # Type de trajet
    trajet = normalize_code(row.get('trajet'))
    if trajet and trajet in mappings['trajet']:
        trajet_uri = create_uri(ONTO, f"TypeTrajet_{trajet}")
        g.add((trajet_uri, RDF.type, ONTO.TypeTrajet))
        g.add((trajet_uri, RDFS.label, Literal(mappings['trajet'][trajet], lang='fr')))
        g.add((usager_uri, ONTO.aTypeTrajet, trajet_uri))
    
    # Place dans le véhicule
    place = normalize_code(row.get('place'))
    if place and place in mappings['place']:
        g.add((usager_uri, ONTO.placeVehicule, Literal(mappings['place'][place], datatype=XSD.string)))
    
    # Ceinture de sécurité (secu1)
    secu1 = normalize_code(row.get('secu1'))
    if secu1 and secu1 in mappings['secu']:
        ceinture = (secu1 == '11')  # 11 = Ceinture - Oui
        g.add((usager_uri, ONTO.ceinture, Literal(ceinture, datatype=XSD.boolean)))
    
    # Lien avec le véhicule
    id_vehicule = clean_value(row.get('id_vehicule'))
    if id_vehicule:
        vehicule_uri = create_uri(ONTO, f"Vehicule_{id_vehicule}")
        if catu == '1':  # Conducteur
            g.add((usager_uri, ONTO.conduisait, vehicule_uri))
        else:  # Passager
            g.add((usager_uri, ONTO.passagerDe, vehicule_uri))

def create_vehicule_triples(g, row, mappings):
    """Crée les triplets RDF pour un véhicule (VERSION COMPLÈTE)"""
    num_acc = clean_value(row.get('Num_Acc'))
    id_vehicule = clean_value(row.get('id_vehicule'))
    
    if not num_acc or not id_vehicule:
        return
    
    vehicule_uri = create_uri(ONTO, f"Vehicule_{id_vehicule}")
    g.add((vehicule_uri, RDF.type, ONTO.Vehicule))
    g.add((vehicule_uri, ONTO.identifiantVehicule, Literal(id_vehicule, datatype=XSD.string)))
    
    # Lien avec l'accident
    accident_uri = create_uri(ONTO, f"Accident_{num_acc}")
    g.add((accident_uri, ONTO.implique_vehicule, vehicule_uri))
    
    # Numéro véhicule (A01, B01...)
    num_veh = clean_value(row.get('num_veh'))
    if num_veh:
        g.add((vehicule_uri, ONTO.numeroVehicule, Literal(num_veh, datatype=XSD.string)))
    
    # Catégorie de véhicule
    catv = normalize_code(row.get('catv'))
    if catv and catv in mappings['catv']:
        catv_uri = create_uri(ONTO, f"CategorieVehicule_{catv}")
        g.add((catv_uri, RDF.type, ONTO.CategorieVehicule))
        g.add((catv_uri, RDFS.label, Literal(mappings['catv'][catv], lang='fr')))
        g.add((vehicule_uri, ONTO.aCategorieVehicule, catv_uri))
    
    # Sens de circulation
    senc = normalize_code(row.get('senc'))
    if senc and senc in mappings['senc']:
        g.add((vehicule_uri, ONTO.sensCirculation, Literal(mappings['senc'][senc], datatype=XSD.string)))
    
    # Point de choc
    choc = normalize_code(row.get('choc'))
    if choc and choc in mappings['choc']:
        g.add((vehicule_uri, ONTO.pointChoc, Literal(mappings['choc'][choc], datatype=XSD.string)))
    
    # Manœuvre
    manv = normalize_code(row.get('manv'))
    if manv and manv in mappings['manv']:
        g.add((vehicule_uri, ONTO.manoeuvre, Literal(mappings['manv'][manv], datatype=XSD.string)))
    
    # Obstacle fixe
    obs = normalize_code(row.get('obs'))
    if obs and obs in mappings['obs']:
        g.add((vehicule_uri, ONTO.obstacle, Literal(mappings['obs'][obs], datatype=XSD.string)))
    
    # Obstacle mobile
    obsm = normalize_code(row.get('obsm'))
    if obsm and obsm in mappings['obsm']:
        g.add((vehicule_uri, ONTO.obstacleMobile, Literal(mappings['obsm'][obsm], datatype=XSD.string)))

# =====================================================================
# FONCTION PRINCIPALE
# =====================================================================

def main():
    """Fonction principale avec statistiques détaillées"""
    print("\n" + "="*60)
    print("🚀 TRANSFORMATION CSV → RDF (VERSION CORRIGÉE)")
    print("="*60)
    
    # Créer le dossier de sortie
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Charger les données
    df_carac, df_lieux, df_usagers, df_vehicules, mappings = load_all_data()
    
    # Vérifier que les données sont chargées
    if df_carac.empty:
        print("❌ ERREUR: Impossible de charger les données principales")
        return
    
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
        print(f"   Triplets dans l'ontologie : {len(g)}")
    except Exception as e:
        print(f"⚠️  Impossible de charger l'ontologie : {e}")
        print("   Continuation sans ontologie...")
    
    initial_triples = len(g)
    
    # Compteurs statistiques
    stats = {
        'accidents': 0,
        'lieux': 0,
        'usagers': 0,
        'vehicules': 0,
        'errors': 0
    }
    
    # Traiter les accidents
    print("\n📍 Traitement des accidents...")
    for idx, row in df_carac.iterrows():
        try:
            if create_accident_triples(g, row, mappings):
                stats['accidents'] += 1
            if (idx + 1) % 100 == 0:
                print(f"   ➜ {idx + 1}/{len(df_carac)} accidents traités ({len(g) - initial_triples} triplets)")
        except Exception as e:
            stats['errors'] += 1
            if stats['errors'] < 5:  # Afficher seulement les 5 premières erreurs
                print(f"   ❌ Erreur accident {idx}: {e}")
    
    print(f"✅ {stats['accidents']} accidents traités")
    
    # Traiter les lieux
    if not df_lieux.empty:
        print("\n🗺️  Traitement des lieux...")
        for idx, row in df_lieux.iterrows():
            try:
                create_lieu_triples(g, row, mappings)
                stats['lieux'] += 1
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] < 5:
                    print(f"   ❌ Erreur lieu {idx}: {e}")
        print(f"✅ {stats['lieux']} lieux traités")
    
    # Traiter les usagers
    if not df_usagers.empty:
        print("\n👤 Traitement des usagers...")
        for idx, row in df_usagers.iterrows():
            try:
                create_usager_triples(g, row, mappings)
                stats['usagers'] += 1
                if (idx + 1) % 500 == 0:
                    print(f"   ➜ {idx + 1}/{len(df_usagers)} usagers traités")
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] < 5:
                    print(f"   ❌ Erreur usager {idx}: {e}")
        print(f"✅ {stats['usagers']} usagers traités")
    
    # Traiter les véhicules
    if not df_vehicules.empty:
        print("\n🚗 Traitement des véhicules...")
        for idx, row in df_vehicules.iterrows():
            try:
                create_vehicule_triples(g, row, mappings)
                stats['vehicules'] += 1
                if (idx + 1) % 500 == 0:
                    print(f"   ➜ {idx + 1}/{len(df_vehicules)} véhicules traités")
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] < 5:
                    print(f"   ❌ Erreur véhicule {idx}: {e}")
        print(f"✅ {stats['vehicules']} véhicules traités")
    
    # Sauvegarder le graphe
    output_file = os.path.join(OUTPUT_DIR, "accidents_rdf.ttl")
    print("\n💾 Sauvegarde du graphe RDF...")
    
    try:
        g.serialize(destination=output_file, format='turtle', encoding='utf-8')
        file_size_kb = os.path.getsize(output_file) / 1024
        
        print("\n" + "="*60)
        print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS")
        print("="*60)
        print(f"\n📊 STATISTIQUES:")
        print(f"   • Accidents traités    : {stats['accidents']}")
        print(f"   • Lieux traités        : {stats['lieux']}")
        print(f"   • Usagers traités      : {stats['usagers']}")
        print(f"   • Véhicules traités    : {stats['vehicules']}")
        print(f"   • Erreurs rencontrées  : {stats['errors']}")
        print(f"\n📈 GRAPHE RDF:")
        print(f"   • Nombre total de triplets : {len(g):,}")
        print(f"   • Triplets données (hors ontologie) : {len(g) - initial_triples:,}")
        print(f"   • Fichier généré       : {output_file}")
        print(f"   • Taille du fichier    : {file_size_kb:,.2f} KB")
        
        # Statistiques détaillées sur les types d'entités
        print(f"\n🔍 ANALYSE DU GRAPHE:")
        
        # Compter les instances par classe
        classes_count = {}
        for s, p, o in g.triples((None, RDF.type, None)):
            class_name = str(o).split('#')[-1]
            classes_count[class_name] = classes_count.get(class_name, 0) + 1
        
        print(f"   Classes instanciées:")
        for class_name, count in sorted(classes_count.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"      • {class_name:30s} : {count:5d} instances")
        
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("   1. Ouvrez GraphDB")
        print("   2. Créez un nouveau repository")
        print("   3. Importez le fichier: " + output_file)
        print("   4. Lancez des requêtes SPARQL pour explorer vos données!")
        
    except Exception as e:
        print(f"\n❌ ERREUR lors de la sauvegarde: {e}")
        print("Tentative de diagnostic...")
        print(f"   Nombre de triplets à sauvegarder: {len(g)}")
        print(f"   Type du graphe: {type(g)}")

if __name__ == "__main__":
    main()