import csv
import os
from rdflib import Graph, Literal, Namespace, RDF, URIRef, OWL
from rdflib.namespace import XSD, FOAF

# Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR) # Assuming script is in scripts/
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'accidents25.ttl')

# Define Namespaces
ONTO_NS = Namespace("http://www.semanticweb.org/ontologies/accidents-routiers-v2#")
# The IRI for the schema ontology (used for reference if needed, but we import by file)
SCHEMA_IRI = URIRef("http://www.semanticweb.org/ontologies/accidents-routiers-v2")
# The IRI for this specific data file (must be different to avoid collision in Protégé)
DATA_ONTO_IRI = URIRef("http://www.semanticweb.org/ontologies/accidents-routiers-v2/data")

GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

# Initialize Graph
g = Graph()
g.bind("", ONTO_NS) # Bind default prefix
g.bind("geo", GEO)
g.bind("foaf", FOAF)

# Declare Ontology and Import
g.add((DATA_ONTO_IRI, RDF.type, OWL.Ontology))
g.add((DATA_ONTO_IRI, OWL.imports, URIRef("file:ontology/ontologi25.ttl")))

# --- Reference Loading Functions ---
def load_ref_map(subdir, filename, key_col, val_col, delimiter=','):
    """Loads a reference CSV into a dictionary."""
    ref_map = {}
    path = os.path.join(DATA_DIR, subdir, filename)
    if not os.path.exists(path):
        print(f"Warning: Reference file not found: {path}")
        return ref_map
    
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                k = row.get(key_col)
                v = row.get(val_col)
                if k and v:
                    ref_map[k.strip()] = v.strip()
    except UnicodeDecodeError:
        # Fallback to latin-1
        try:
            with open(path, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for row in reader:
                    k = row.get(key_col)
                    v = row.get(val_col)
                    if k and v:
                        ref_map[k.strip()] = v.strip()
        except Exception as e:
            print(f"Error loading {filename} with latin-1: {e}")
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return ref_map

# Load References
print("Loading references...")

# ref-usag (Comma separated, Code/Description)
REF_SEXE = load_ref_map('ref-usag', 'sexe.csv', 'Code', 'Description', ',')
REF_GRAV = load_ref_map('ref-usag', 'grav.csv', 'Code', 'Description', ',')
REF_CATU = load_ref_map('ref-usag', 'catu.csv', 'Code', 'Description', ',')
REF_TRAJET = load_ref_map('ref-usag', 'trajet.csv', 'Code', 'Description', ',')
REF_SECU = load_ref_map('ref-usag', 'secu.csv', 'Code', 'Description', ',')
REF_LOCP = load_ref_map('ref-usag', 'locp.csv', 'Code', 'Description', ',')
REF_ACTP = load_ref_map('ref-usag', 'actp.csv', 'Code', 'Description', ',')
REF_ETATP = load_ref_map('ref-usag', 'etatp.csv', 'Code', 'Description', ',')
REF_PLACE = load_ref_map('ref-usag', 'place.csv', 'Code', 'Description', ',')

# ref-carac (Mixed)
REF_LUM = load_ref_map('ref-carac', 'lum.csv', 'id', 'lib', ';')
REF_ATM = load_ref_map('ref-carac', 'Conditions_atmo.csv', 'id', 'lib', ';')
REF_COL = load_ref_map('ref-carac', 'Type_col.csv', 'id', 'lib', ';')
REF_INT = load_ref_map('ref-carac', 'Intersection.csv', 'id', 'lib', ';')
REF_AGG = load_ref_map('ref-carac', 'Localisation.csv', 'id', 'lib', ';')

# ref_lieux (Comma separated)
REF_CATR = load_ref_map('ref_lieux', 'catr.csv', 'Code', 'Description', ',')
REF_CIRC = load_ref_map('ref_lieux', 'circ.csv', 'Code', 'Description', ',')
REF_PROF = load_ref_map('ref_lieux', 'prof.csv', 'Code', 'Description', ',')
REF_PLAN = load_ref_map('ref_lieux', 'plan.csv', 'Code', 'Description', ',')
REF_SURF = load_ref_map('ref_lieux', 'surf.csv', 'Code', 'Description', ',')
REF_INFRA = load_ref_map('ref_lieux', 'infra.csv', 'Code', 'Description', ',')
REF_SITU = load_ref_map('ref_lieux', 'situ.csv', 'Code', 'Description', ',')

# ref-veh (Comma separated)
REF_CATV = load_ref_map('ref-veh', 'Catv.csv', 'ID', 'Description', ',')
REF_OBS = load_ref_map('ref-veh', 'obs.csv', 'Code', 'Description', ',')
REF_OBSM = load_ref_map('ref-veh', 'obsm.csv', 'Code', 'Description', ',')
REF_CHOC = load_ref_map('ref-veh', 'choc.csv', 'Code', 'Description', ',')
REF_MANV = load_ref_map('ref-veh', 'manv.csv', 'Code', 'Description', ',')
REF_SENC = load_ref_map('ref-veh', 'senc.csv', 'Code', 'Description', ',')
REF_MOTOR = {} # Not provided in list, assuming integer or manual map if needed.

# Additional ref_lieux
REF_VOSP = load_ref_map('ref_lieux', 'vosp.csv', 'Code', 'Description', ',')

# Additional ref-usag (pedestrian fields)
REF_LOCP = load_ref_map('ref-usag', 'locp.csv', 'Code', 'Description', ',')
REF_ACTP = load_ref_map('ref-usag', 'actp.csv', 'Code', 'Description', ',')
REF_ETATP = load_ref_map('ref-usag', 'etatp.csv', 'Code', 'Description', ',')

# Department to DBpedia mapping
REF_DEPT = load_ref_map('ref-carac', 'Département-français.csv', 'DEP_CODE', 'DEP_NOM', ',')

# --- Helper Functions ---
def clean_id(value):
    if not value: return ""
    return value.replace(" ", "").replace("\xa0", "").strip()

def clean_int(value):
    if not value or value == "-1" or value == "N/A": return None
    try: return int(float(value.replace(",", ".")))
    except ValueError: return None

def clean_float(value):
    if not value or value == "-1" or value == "N/A": return None
    try: return float(value.replace(",", "."))
    except ValueError: return None

def get_label(value, ref_map):
    """Returns the label from the map if exists, else the original value."""
    if not value or value == "-1": return None
    # Try exact match first, then integer match
    if value in ref_map: return ref_map[value]
    try:
        int_val = str(int(float(value)))
        if int_val in ref_map: return ref_map[int_val]
    except:
        pass
    return value # Fallback to code if not found

# --- Property Declarations ---
def declare_property(prop_uri, prop_type):
    g.add((prop_uri, RDF.type, prop_type))

# Declare properties
declare_property(ONTO_NS.numAcc, OWL.DatatypeProperty)
declare_property(ONTO_NS.jour, OWL.DatatypeProperty)
declare_property(ONTO_NS.mois, OWL.DatatypeProperty)
declare_property(ONTO_NS.annee, OWL.DatatypeProperty)
declare_property(ONTO_NS.heure, OWL.DatatypeProperty)
declare_property(ONTO_NS.luminosite, OWL.DatatypeProperty)
declare_property(ONTO_NS.departement, OWL.DatatypeProperty)
declare_property(ONTO_NS.commune, OWL.DatatypeProperty)
declare_property(ONTO_NS.localisation, OWL.DatatypeProperty)
declare_property(ONTO_NS.intersection, OWL.DatatypeProperty)
declare_property(ONTO_NS.conditionAtmospherique, OWL.DatatypeProperty)
declare_property(ONTO_NS.typeCollision, OWL.DatatypeProperty)
declare_property(ONTO_NS.adresse, OWL.DatatypeProperty)
declare_property(ONTO_NS.latitude, OWL.DatatypeProperty)
declare_property(ONTO_NS.longitude, OWL.DatatypeProperty)

declare_property(ONTO_NS.categorieRoute, OWL.DatatypeProperty)
declare_property(ONTO_NS.numeroRoute, OWL.DatatypeProperty)
declare_property(ONTO_NS.regimeCirculation, OWL.DatatypeProperty)
declare_property(ONTO_NS.nbVoies, OWL.DatatypeProperty)
declare_property(ONTO_NS.profilLong, OWL.DatatypeProperty)
declare_property(ONTO_NS.tracePlan, OWL.DatatypeProperty)
declare_property(ONTO_NS.etatSurface, OWL.DatatypeProperty)
declare_property(ONTO_NS.infrastructure, OWL.DatatypeProperty)
declare_property(ONTO_NS.situation, OWL.DatatypeProperty)
declare_property(ONTO_NS.vitesseMax, OWL.DatatypeProperty)
declare_property(ONTO_NS.indiceNumero1, OWL.DatatypeProperty)
declare_property(ONTO_NS.indiceNumero2, OWL.DatatypeProperty)
declare_property(ONTO_NS.voieReservee, OWL.DatatypeProperty)
declare_property(ONTO_NS.pointRepere, OWL.DatatypeProperty)
declare_property(ONTO_NS.distancePointRepere, OWL.DatatypeProperty)
declare_property(ONTO_NS.largeurTerrePlein, OWL.DatatypeProperty)
declare_property(ONTO_NS.largeurRoute, OWL.DatatypeProperty)

declare_property(ONTO_NS.idVehicule, OWL.DatatypeProperty)
declare_property(ONTO_NS.sensCirculation, OWL.DatatypeProperty)
declare_property(ONTO_NS.categorieVehicule, OWL.DatatypeProperty)
declare_property(ONTO_NS.obstacleFixe, OWL.DatatypeProperty)
declare_property(ONTO_NS.obstacleMobile, OWL.DatatypeProperty)
declare_property(ONTO_NS.pointChoc, OWL.DatatypeProperty)
declare_property(ONTO_NS.manoeuvre, OWL.DatatypeProperty)
declare_property(ONTO_NS.motorisation, OWL.DatatypeProperty)
declare_property(ONTO_NS.numeroVehicule, OWL.DatatypeProperty)
declare_property(ONTO_NS.occupantsTransportCommun, OWL.DatatypeProperty)

declare_property(ONTO_NS.idUsager, OWL.DatatypeProperty)
declare_property(ONTO_NS.place, OWL.DatatypeProperty)
declare_property(ONTO_NS.categorieUsager, OWL.DatatypeProperty)
declare_property(ONTO_NS.gravite, OWL.DatatypeProperty)
declare_property(ONTO_NS.sexe, OWL.DatatypeProperty)
declare_property(ONTO_NS.anneeNaissance, OWL.DatatypeProperty)
declare_property(ONTO_NS.motifDeplacement, OWL.DatatypeProperty)
declare_property(ONTO_NS.equipementSecurite, OWL.DatatypeProperty)
declare_property(ONTO_NS.equipementSecurite2, OWL.DatatypeProperty)
declare_property(ONTO_NS.equipementSecurite3, OWL.DatatypeProperty)
declare_property(ONTO_NS.numeroVehiculeUsager, OWL.DatatypeProperty)
declare_property(ONTO_NS.localisationPieton, OWL.DatatypeProperty)
declare_property(ONTO_NS.actionPieton, OWL.DatatypeProperty)
declare_property(ONTO_NS.etatPieton, OWL.DatatypeProperty)

declare_property(ONTO_NS.aLieu, OWL.ObjectProperty)
declare_property(ONTO_NS.impliqueVehicule, OWL.ObjectProperty)
declare_property(ONTO_NS.impliqueUsager, OWL.ObjectProperty)
declare_property(ONTO_NS.occupationVehicule, OWL.ObjectProperty)
declare_property(ONTO_NS.departementDBpedia, OWL.ObjectProperty)


def process_caracteristiques():
    print("Processing CARACTERISTIQUES...")
    with open(os.path.join(DATA_DIR, 'caract-2024.csv'), 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            num_acc = clean_id(row['Num_Acc'])
            if not num_acc: continue
            
            accident_uri = ONTO_NS[f"Accident_{num_acc}"]
            g.add((accident_uri, RDF.type, ONTO_NS.Accident))
            g.add((accident_uri, ONTO_NS.numAcc, Literal(num_acc, datatype=XSD.string)))
            
            if row.get('jour'): g.add((accident_uri, ONTO_NS.jour, Literal(clean_int(row['jour']), datatype=XSD.integer)))
            if row.get('mois'): g.add((accident_uri, ONTO_NS.mois, Literal(clean_int(row['mois']), datatype=XSD.integer)))
            if row.get('an'): g.add((accident_uri, ONTO_NS.annee, Literal(clean_int(row['an']), datatype=XSD.integer)))
            if row.get('hrmn'): g.add((accident_uri, ONTO_NS.heure, Literal(row['hrmn'], datatype=XSD.string)))
            
            # Mapped Attributes
            lum_label = get_label(row.get('lum'), REF_LUM)
            if lum_label: g.add((accident_uri, ONTO_NS.luminosite, Literal(lum_label, datatype=XSD.string)))
            
            atm_label = get_label(row.get('atm'), REF_ATM)
            if atm_label: g.add((accident_uri, ONTO_NS.conditionAtmospherique, Literal(atm_label, datatype=XSD.string)))
            
            col_label = get_label(row.get('col'), REF_COL)
            if col_label: g.add((accident_uri, ONTO_NS.typeCollision, Literal(col_label, datatype=XSD.string)))
            
            agg_label = get_label(row.get('agg'), REF_AGG)
            if agg_label: g.add((accident_uri, ONTO_NS.localisation, Literal(agg_label, datatype=XSD.string)))
            
            int_label = get_label(row.get('int'), REF_INT)
            if int_label: g.add((accident_uri, ONTO_NS.intersection, Literal(int_label, datatype=XSD.string)))

            if row.get('dep'): g.add((accident_uri, ONTO_NS.departement, Literal(row['dep'], datatype=XSD.string)))
            if row.get('com'): g.add((accident_uri, ONTO_NS.commune, Literal(row['com'], datatype=XSD.string)))
            if row.get('adr'): g.add((accident_uri, ONTO_NS.adresse, Literal(row['adr'], datatype=XSD.string)))
            
            lat = clean_float(row.get('lat'))
            long = clean_float(row.get('long'))
            if lat: g.add((accident_uri, ONTO_NS.latitude, Literal(lat, datatype=XSD.decimal)))
            if long: g.add((accident_uri, ONTO_NS.longitude, Literal(long, datatype=XSD.decimal)))
            
            # DBpedia Integration
            dept_code = row.get('dep')
            if dept_code:
                # Normalize department code to 3 digits (matching format in REF_DEPT)
                dept_code_normalized = dept_code.strip().zfill(3)
                if dept_code_normalized in REF_DEPT:
                    dept_name = REF_DEPT[dept_code_normalized]
                    # Create DBpedia URI (French DBpedia)
                    # Clean department name for URI (replace spaces with underscores, remove special chars)
                    dept_uri_name = dept_name.replace(' ', '_').replace("'", '%27')
                    dbpedia_uri = URIRef(f"http://fr.dbpedia.org/resource/{dept_uri_name}")
                    g.add((accident_uri, ONTO_NS.departementDBpedia, dbpedia_uri))

def process_lieux():
    print("Processing LIEUX...")
    with open(os.path.join(DATA_DIR, 'lieux-2024.csv'), 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            num_acc = clean_id(row['Num_Acc'])
            if not num_acc: continue
            
            accident_uri = ONTO_NS[f"Accident_{num_acc}"]
            lieu_uri = ONTO_NS[f"Lieu_{num_acc}"]
            
            g.add((lieu_uri, RDF.type, ONTO_NS.Lieu))
            g.add((accident_uri, ONTO_NS.aLieu, lieu_uri))
            
            catr_label = get_label(row.get('catr'), REF_CATR)
            if catr_label: g.add((lieu_uri, ONTO_NS.categorieRoute, Literal(catr_label, datatype=XSD.string)))
            
            circ_label = get_label(row.get('circ'), REF_CIRC)
            if circ_label: g.add((lieu_uri, ONTO_NS.regimeCirculation, Literal(circ_label, datatype=XSD.string)))
            
            prof_label = get_label(row.get('prof'), REF_PROF)
            if prof_label: g.add((lieu_uri, ONTO_NS.profilLong, Literal(prof_label, datatype=XSD.string)))
            
            plan_label = get_label(row.get('plan'), REF_PLAN)
            if plan_label: g.add((lieu_uri, ONTO_NS.tracePlan, Literal(plan_label, datatype=XSD.string)))
            
            surf_label = get_label(row.get('surf'), REF_SURF)
            if surf_label: g.add((lieu_uri, ONTO_NS.etatSurface, Literal(surf_label, datatype=XSD.string)))
            
            infra_label = get_label(row.get('infra'), REF_INFRA)
            if infra_label: g.add((lieu_uri, ONTO_NS.infrastructure, Literal(infra_label, datatype=XSD.string)))
            
            situ_label = get_label(row.get('situ'), REF_SITU)
            if situ_label: g.add((lieu_uri, ONTO_NS.situation, Literal(situ_label, datatype=XSD.string)))
            
            if row.get('voie'): g.add((lieu_uri, ONTO_NS.numeroRoute, Literal(row['voie'], datatype=XSD.string)))
            if clean_int(row.get('nbv')): g.add((lieu_uri, ONTO_NS.nbVoies, Literal(clean_int(row['nbv']), datatype=XSD.integer)))
            if clean_int(row.get('vma')): g.add((lieu_uri, ONTO_NS.vitesseMax, Literal(clean_int(row['vma']), datatype=XSD.integer)))
            
            # Missing fields - now added
            if row.get('v1'): g.add((lieu_uri, ONTO_NS.indiceNumero1, Literal(row['v1'], datatype=XSD.string)))
            if row.get('v2'): g.add((lieu_uri, ONTO_NS.indiceNumero2, Literal(row['v2'], datatype=XSD.string)))
            
            vosp_label = get_label(row.get('vosp'), REF_VOSP)
            if vosp_label: g.add((lieu_uri, ONTO_NS.voieReservee, Literal(vosp_label, datatype=XSD.string)))
            
            if row.get('pr'): g.add((lieu_uri, ONTO_NS.pointRepere, Literal(row['pr'], datatype=XSD.string)))
            if clean_int(row.get('pr1')): g.add((lieu_uri, ONTO_NS.distancePointRepere, Literal(clean_int(row['pr1']), datatype=XSD.integer)))
            
            lartpc_val = clean_float(row.get('lartpc'))
            if lartpc_val: g.add((lieu_uri, ONTO_NS.largeurTerrePlein, Literal(lartpc_val, datatype=XSD.decimal)))
            
            larrout_val = clean_float(row.get('larrout'))
            if larrout_val: g.add((lieu_uri, ONTO_NS.largeurRoute, Literal(larrout_val, datatype=XSD.decimal)))

def process_vehicules():
    print("Processing VEHICULES...")
    with open(os.path.join(DATA_DIR, 'vehicules-2024.csv'), 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            num_acc = clean_id(row['Num_Acc'])
            id_veh = clean_id(row['id_vehicule'])
            if not num_acc or not id_veh: continue
            
            accident_uri = ONTO_NS[f"Accident_{num_acc}"]
            vehicule_uri = ONTO_NS[f"Vehicule_{id_veh}"]
            
            g.add((vehicule_uri, RDF.type, ONTO_NS.Vehicule))
            g.add((accident_uri, ONTO_NS.impliqueVehicule, vehicule_uri))
            g.add((vehicule_uri, ONTO_NS.idVehicule, Literal(id_veh, datatype=XSD.string)))
            
            catv_label = get_label(row.get('catv'), REF_CATV)
            if catv_label: g.add((vehicule_uri, ONTO_NS.categorieVehicule, Literal(catv_label, datatype=XSD.string)))
            
            obs_label = get_label(row.get('obs'), REF_OBS)
            if obs_label: g.add((vehicule_uri, ONTO_NS.obstacleFixe, Literal(obs_label, datatype=XSD.string)))
            
            obsm_label = get_label(row.get('obsm'), REF_OBSM)
            if obsm_label: g.add((vehicule_uri, ONTO_NS.obstacleMobile, Literal(obsm_label, datatype=XSD.string)))
            
            choc_label = get_label(row.get('choc'), REF_CHOC)
            if choc_label: g.add((vehicule_uri, ONTO_NS.pointChoc, Literal(choc_label, datatype=XSD.string)))
            
            manv_label = get_label(row.get('manv'), REF_MANV)
            if manv_label: g.add((vehicule_uri, ONTO_NS.manoeuvre, Literal(manv_label, datatype=XSD.string)))
            
            senc_label = get_label(row.get('senc'), REF_SENC)
            if senc_label: g.add((vehicule_uri, ONTO_NS.sensCirculation, Literal(senc_label, datatype=XSD.string)))
            
            if clean_int(row.get('motor')): g.add((vehicule_uri, ONTO_NS.motorisation, Literal(clean_int(row['motor']), datatype=XSD.integer)))
            
            # Missing fields - now added
            if row.get('num_veh'): g.add((vehicule_uri, ONTO_NS.numeroVehicule, Literal(row['num_veh'], datatype=XSD.string)))
            if clean_int(row.get('occutc')): g.add((vehicule_uri, ONTO_NS.occupantsTransportCommun, Literal(clean_int(row['occutc']), datatype=XSD.integer)))

def process_usagers():
    print("Processing USAGERS...")
    with open(os.path.join(DATA_DIR, 'usagers-2024.csv'), 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            num_acc = clean_id(row['Num_Acc'])
            id_usager = clean_id(row['id_usager'])
            id_veh = clean_id(row['id_vehicule'])
            
            if not num_acc or not id_usager: continue
            
            accident_uri = ONTO_NS[f"Accident_{num_acc}"]
            usager_uri = ONTO_NS[f"Usager_{id_usager}"]
            
            g.add((usager_uri, RDF.type, ONTO_NS.Usager))
            g.add((accident_uri, ONTO_NS.impliqueUsager, usager_uri))
            
            if id_veh:
                vehicule_uri = ONTO_NS[f"Vehicule_{id_veh}"]
                g.add((usager_uri, ONTO_NS.occupationVehicule, vehicule_uri))
            
            g.add((usager_uri, ONTO_NS.idUsager, Literal(id_usager, datatype=XSD.string)))
            
            catu_label = get_label(row.get('catu'), REF_CATU)
            if catu_label: g.add((usager_uri, ONTO_NS.categorieUsager, Literal(catu_label, datatype=XSD.string)))
            
            grav_label = get_label(row.get('grav'), REF_GRAV)
            if grav_label: g.add((usager_uri, ONTO_NS.gravite, Literal(grav_label, datatype=XSD.string)))
            
            sexe_label = get_label(row.get('sexe'), REF_SEXE)
            if sexe_label: g.add((usager_uri, ONTO_NS.sexe, Literal(sexe_label, datatype=XSD.string)))
            
            trajet_label = get_label(row.get('trajet'), REF_TRAJET)
            if trajet_label: g.add((usager_uri, ONTO_NS.motifDeplacement, Literal(trajet_label, datatype=XSD.string)))
            
            secu_label = get_label(row.get('secu1'), REF_SECU)
            if secu_label: g.add((usager_uri, ONTO_NS.equipementSecurite, Literal(secu_label, datatype=XSD.string)))
            
            place_label = get_label(row.get('place'), REF_PLACE)
            if place_label: g.add((usager_uri, ONTO_NS.place, Literal(place_label, datatype=XSD.string)))
            
            if clean_int(row.get('an_nais')): g.add((usager_uri, ONTO_NS.anneeNaissance, Literal(clean_int(row['an_nais']), datatype=XSD.integer)))
            
            # Missing fields - now added
            if row.get('num_veh'): g.add((usager_uri, ONTO_NS.numeroVehiculeUsager, Literal(row['num_veh'], datatype=XSD.string)))
            
            secu2_label = get_label(row.get('secu2'), REF_SECU)
            if secu2_label: g.add((usager_uri, ONTO_NS.equipementSecurite2, Literal(secu2_label, datatype=XSD.string)))
            
            secu3_label = get_label(row.get('secu3'), REF_SECU)
            if secu3_label: g.add((usager_uri, ONTO_NS.equipementSecurite3, Literal(secu3_label, datatype=XSD.string)))
            
            # Pedestrian-specific fields
            locp_label = get_label(row.get('locp'), REF_LOCP)
            if locp_label: g.add((usager_uri, ONTO_NS.localisationPieton, Literal(locp_label, datatype=XSD.string)))
            
            actp_label = get_label(row.get('actp'), REF_ACTP)
            if actp_label: g.add((usager_uri, ONTO_NS.actionPieton, Literal(actp_label, datatype=XSD.string)))
            
            etatp_label = get_label(row.get('etatp'), REF_ETATP)
            if etatp_label: g.add((usager_uri, ONTO_NS.etatPieton, Literal(etatp_label, datatype=XSD.string)))

if __name__ == "__main__":
    process_caracteristiques()
    process_lieux()
    process_vehicules()
    process_usagers()
    
    print(f"Saving graph to {OUTPUT_FILE}...")
    g.serialize(destination=OUTPUT_FILE, format='turtle')
    print("Done.")
