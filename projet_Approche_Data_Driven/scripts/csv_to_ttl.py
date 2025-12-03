#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to TTL Converter for Road Accidents Data
Converts caract-2024.csv, lieux-2024.csv, usagers-2024.csv, and vehicules-2024.csv
into RDF Turtle format (instances.ttl)
"""

import csv
import os
from pathlib import Path


class CSVToTTLConverter:
    def __init__(self, data_dir, output_file):
        self.data_dir = Path(data_dir)
        self.output_file = Path(output_file)
        self.namespace = "http://www.w3.org/2012/7/ra3.owl#"
        
        # Store data for relationships
        self.accidents = {}
        self.lieux = {}
        self.vehicules = {}
        self.usagers = {}
        
    def clean_value(self, value):
        """Clean and format CSV values"""
        if value in ['N/A', '', ' -1', '-1', None]:
            return None
        return value.strip().strip('"')
    
    def is_valid_accident_number(self, num_acc):
        """Check if accident number is in valid range (202400000001 to 202400009999)"""
        if not num_acc:
            return False
        try:
            num = int(num_acc)
            return 202400000001 <= num <= 202400009999
        except ValueError:
            return False
    
    def write_header(self, f):
        """Write TTL file header with prefixes"""
        f.write("@prefix ra: <http://www.w3.org/2012/7/ra3.owl#> .\n")
        f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
        f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        f.write("@prefix dbo: <http://dbpedia.org/ontology/> .\n")
        f.write("@prefix xsd: <http://www.w3.org/2001/XMLowl#> .\n")
        f.write("@prefix dbpedia: <http://dbpedia.org/resource/> .\n\n")
    
    
    def write_departements(self, f):
        """Write French departments mapping to TTL file"""
        
        f.write("#################################################################\n")
        f.write("# Departments\n")
        f.write("#################################################################\n\n")
        
   
        f.write("ra:Dep_01 dbo:capital dbpedia:Bourg-en-Bresse .\n")
        f.write("ra:Dep_02 dbo:capital dbpedia:Laon .\n")
        f.write("ra:Dep_03 dbo:capital dbpedia:Moulins .\n")
        f.write("ra:Dep_04 dbo:capital dbpedia:Digne-les-Bains .\n")
        f.write("ra:Dep_05 dbo:capital dbpedia:Gap .\n")
        f.write("ra:Dep_06 dbo:capital dbpedia:Nice .\n")
        f.write("ra:Dep_07 dbo:capital dbpedia:Privas .\n")
        f.write("ra:Dep_08 dbo:capital dbpedia:Charleville-Mézières .\n")
        f.write("ra:Dep_09 dbo:capital dbpedia:Foix .\n")

        f.write("ra:Dep_10 dbo:capital dbpedia:Troyes .\n")
        f.write("ra:Dep_11 dbo:capital dbpedia:Carcassonne .\n")
        f.write("ra:Dep_12 dbo:capital dbpedia:Rodez .\n")
        f.write("ra:Dep_13 dbo:capital dbpedia:Marseille .\n")
        f.write("ra:Dep_14 dbo:capital dbpedia:Caen .\n")
        f.write("ra:Dep_15 dbo:capital dbpedia:Aurillac .\n")
        f.write("ra:Dep_16 dbo:capital dbpedia:Angoulême .\n")
        f.write("ra:Dep_17 dbo:capital dbpedia:La_Rochelle .\n")
        f.write("ra:Dep_18 dbo:capital dbpedia:Bourges .\n")
        f.write("ra:Dep_19 dbo:capital dbpedia:Tulle .\n")

        f.write("ra:Dep_2A dbo:capital dbpedia:Ajaccio .\n")
        f.write("ra:Dep_2B dbo:capital dbpedia:Bastia .\n")

        f.write("ra:Dep_21 dbo:capital dbpedia:Dijon .\n")
        f.write("ra:Dep_22 dbo:capital dbpedia:Saint-Brieuc .\n")
        f.write("ra:Dep_23 dbo:capital dbpedia:Guéret .\n")
        f.write("ra:Dep_24 dbo:capital dbpedia:Périgueux .\n")
        f.write("ra:Dep_25 dbo:capital dbpedia:Besançon .\n")
        f.write("ra:Dep_26 dbo:capital dbpedia:Valence .\n")
        f.write("ra:Dep_27 dbo:capital dbpedia:Évreux .\n")
        f.write("ra:Dep_28 dbo:capital dbpedia:Chartres .\n")
        f.write("ra:Dep_29 dbo:capital dbpedia:Quimper .\n")

        f.write("ra:Dep_30 dbo:capital dbpedia:Nîmes .\n")
        f.write("ra:Dep_31 dbo:capital dbpedia:Toulouse .\n")
        f.write("ra:Dep_32 dbo:capital dbpedia:Auch .\n")
        f.write("ra:Dep_33 dbo:capital dbpedia:Bordeaux .\n")
        f.write("ra:Dep_34 dbo:capital dbpedia:Montpellier .\n")
        f.write("ra:Dep_35 dbo:capital dbpedia:Rennes .\n")
        f.write("ra:Dep_36 dbo:capital dbpedia:Châteauroux .\n")
        f.write("ra:Dep_37 dbo:capital dbpedia:Tours .\n")
        f.write("ra:Dep_38 dbo:capital dbpedia:Grenoble .\n")
        f.write("ra:Dep_39 dbo:capital dbpedia:Lons-le-Saunier .\n")
        f.write("ra:Dep_40 dbo:capital dbpedia:Mont-de-Marsan .\n")
        f.write("ra:Dep_41 dbo:capital dbpedia:Blois .\n")
        f.write("ra:Dep_42 dbo:capital dbpedia:Saint-Étienne .\n")
        f.write("ra:Dep_43 dbo:capital dbpedia:Le_Puy-en-Velay .\n")
        f.write("ra:Dep_44 dbo:capital dbpedia:Nantes .\n")
        f.write("ra:Dep_45 dbo:capital dbpedia:Orléans .\n")
        f.write("ra:Dep_46 dbo:capital dbpedia:Cahors .\n")
        f.write("ra:Dep_47 dbo:capital dbpedia:Agen .\n")
        f.write("ra:Dep_48 dbo:capital dbpedia:Mende .\n")
        f.write("ra:Dep_49 dbo:capital dbpedia:Angers .\n")

        f.write("ra:Dep_50 dbo:capital dbpedia:Saint-Lô .\n")
        f.write("ra:Dep_51 dbo:capital dbpedia:Châlons-en-Champagne .\n")
        f.write("ra:Dep_52 dbo:capital dbpedia:Chaumont .\n")
        f.write("ra:Dep_53 dbo:capital dbpedia:Laval .\n")
        f.write("ra:Dep_54 dbo:capital dbpedia:Nancy .\n")
        f.write("ra:Dep_55 dbo:capital dbpedia:Bar-le-Duc .\n")
        f.write("ra:Dep_56 dbo:capital dbpedia:Vannes .\n")
        f.write("ra:Dep_57 dbo:capital dbpedia:Metz .\n")
        f.write("ra:Dep_58 dbo:capital dbpedia:Nevers .\n")
        f.write("ra:Dep_59 dbo:capital dbpedia:Lille .\n")

        f.write("ra:Dep_60 dbo:capital dbpedia:Beauvais .\n")
        f.write("ra:Dep_61 dbo:capital dbpedia:Alençon .\n")
        f.write("ra:Dep_62 dbo:capital dbpedia:Arras .\n")
        f.write("ra:Dep_63 dbo:capital dbpedia:Clermont-Ferrand .\n")
        f.write("ra:Dep_64 dbo:capital dbpedia:Pau .\n")
        f.write("ra:Dep_65 dbo:capital dbpedia:Tarbes .\n")
        f.write("ra:Dep_66 dbo:capital dbpedia:Perpignan .\n")
        f.write("ra:Dep_67 dbo:capital dbpedia:Strasbourg .\n")
        f.write("ra:Dep_68 dbo:capital dbpedia:Colmar .\n")
        f.write("ra:Dep_69 dbo:capital dbpedia:Lyon .\n")

        f.write("ra:Dep_70 dbo:capital dbpedia:Vesoul .\n")
        f.write("ra:Dep_71 dbo:capital dbpedia:Mâcon .\n")
        f.write("ra:Dep_72 dbo:capital dbpedia:Le_Mans .\n")
        f.write("ra:Dep_73 dbo:capital dbpedia:Chambéry .\n")
        f.write("ra:Dep_74 dbo:capital dbpedia:Annecy .\n")
        f.write("ra:Dep_75 dbo:capital dbpedia:Paris .\n")
        f.write("ra:Dep_76 dbo:capital dbpedia:Rouen .\n")
        f.write("ra:Dep_77 dbo:capital dbpedia:Melun .\n")
        f.write("ra:Dep_78 dbo:capital dbpedia:Versailles .\n")
        f.write("ra:Dep_79 dbo:capital dbpedia:Niort .\n")

        f.write("ra:Dep_80 dbo:capital dbpedia:Amiens .\n")
        f.write("ra:Dep_81 dbo:capital dbpedia:Albi .\n")
        f.write("ra:Dep_82 dbo:capital dbpedia:Montauban .\n")
        f.write("ra:Dep_83 dbo:capital dbpedia:Toulon .\n")
        f.write("ra:Dep_84 dbo:capital dbpedia:Avignon .\n")
        f.write("ra:Dep_85 dbo:capital dbpedia:La_Roche-sur-Yon .\n")
        f.write("ra:Dep_86 dbo:capital dbpedia:Poitiers .\n")
        f.write("ra:Dep_87 dbo:capital dbpedia:Limoges .\n")
        f.write("ra:Dep_88 dbo:capital dbpedia:Épinal .\n")
        f.write("ra:Dep_89 dbo:capital dbpedia:Auxerre .\n")
        f.write("ra:Dep_90 dbo:capital dbpedia:Belfort .\n")
        f.write("ra:Dep_91 dbo:capital dbpedia:Évry .\n")
        f.write("ra:Dep_92 dbo:capital dbpedia:Nanterre .\n")
        f.write("ra:Dep_93 dbo:capital dbpedia:Bobigny .\n")
        f.write("ra:Dep_94 dbo:capital dbpedia:Créteil .\n")
        f.write("ra:Dep_95 dbo:capital dbpedia:Pontoise .\n")

        
        f.write("\n")

        
    def read_caract(self):
        """Read caract-2024.csv and store accident characteristics"""
        caract_file = self.data_dir / "caract-2024.csv"
        print(f"Reading {caract_file}...")
        
        with open(caract_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                num_acc = self.clean_value(row['Num_Acc'])
                if num_acc and self.is_valid_accident_number(num_acc):
                    self.accidents[num_acc] = {
                        'jour': self.clean_value(row.get('jour')),
                        'mois': self.clean_value(row.get('mois')),
                        'an': self.clean_value(row.get('an')),
                        'hrmn': self.clean_value(row.get('hrmn')),
                        'lum': self.clean_value(row.get('lum')),
                        'dep': self.clean_value(row.get('dep')),
                        'com': self.clean_value(row.get('com')),
                        'agg': self.clean_value(row.get('agg')),
                        'int': self.clean_value(row.get('int')),
                        'atm': self.clean_value(row.get('atm')),
                        'col': self.clean_value(row.get('col')),
                        'adr': self.clean_value(row.get('adr')),
                        'lat': self.clean_value(row.get('lat')),
                        'long': self.clean_value(row.get('long'))
                    }
        print(f"  Loaded {len(self.accidents)} accidents")
    
    def read_lieux(self):
        """Read lieux-2024.csv and store location details"""
        lieux_file = self.data_dir / "lieux-2024.csv"
        print(f"Reading {lieux_file}...")

        with open(lieux_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                num_acc = self.clean_value(row.get('Num_Acc'))
                if not num_acc or not self.is_valid_accident_number(num_acc):
                    continue
                if num_acc not in self.lieux:
                    self.lieux[num_acc] = []
                self.lieux[num_acc].append({
                    'catr': self.clean_value(row.get('catr')),
                    'voie': self.clean_value(row.get('voie')),
                    'v1': self.clean_value(row.get('v1')),
                    'v2': self.clean_value(row.get('v2')),
                    'circ': self.clean_value(row.get('circ')),
                    'nbv': self.clean_value(row.get('nbv')),
                    'vosp': self.clean_value(row.get('vosp')),
                    'prof': self.clean_value(row.get('prof')),
                    'pr': self.clean_value(row.get('pr')),
                    'pr1': self.clean_value(row.get('pr1')),
                    'plan': self.clean_value(row.get('plan')),
                    'lartpc': self.clean_value(row.get('lartpc')),
                    'larrout': self.clean_value(row.get('larrout')),
                    'surf': self.clean_value(row.get('surf')),
                    'infra': self.clean_value(row.get('infra')),
                    'situ': self.clean_value(row.get('situ')),
                    'vma': self.clean_value(row.get('vma'))
                })
        print(f"  Loaded location data for {len(self.lieux)} accidents")
    
    def read_vehicules(self):
        """Read vehicules-2024.csv and store vehicle information"""
        vehicules_file = self.data_dir / "vehicules-2024.csv"
        print(f"Reading {vehicules_file}...")
        
        with open(vehicules_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                num_acc = self.clean_value(row['Num_Acc'])
                id_vehicule = self.clean_value(row['id_vehicule'])
                
                if num_acc and id_vehicule and self.is_valid_accident_number(num_acc):
                    if num_acc not in self.vehicules:
                        self.vehicules[num_acc] = []
                    
                    self.vehicules[num_acc].append({
                        'id_vehicule': id_vehicule,
                        'num_veh': self.clean_value(row.get('num_veh')),
                        'senc': self.clean_value(row.get('senc')),
                        'catv': self.clean_value(row.get('catv')),
                        'obs': self.clean_value(row.get('obs')),
                        'obsm': self.clean_value(row.get('obsm')),
                        'choc': self.clean_value(row.get('choc')),
                        'manv': self.clean_value(row.get('manv')),
                        'motor': self.clean_value(row.get('motor')),
                        'occutc': self.clean_value(row.get('occutc'))
                    })
        print(f"  Loaded vehicle data for {len(self.vehicules)} accidents")
    
    def read_usagers(self):
        """Read usagers-2024.csv and store user information"""
        usagers_file = self.data_dir / "usagers-2024.csv"
        print(f"Reading {usagers_file}...")
        
        with open(usagers_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                num_acc = self.clean_value(row['Num_Acc'])
                id_usager = self.clean_value(row['id_usager'])
                
                if num_acc and id_usager and self.is_valid_accident_number(num_acc):
                    if num_acc not in self.usagers:
                        self.usagers[num_acc] = []
                    
                    self.usagers[num_acc].append({
                        'id_usager': id_usager,
                        'id_vehicule': self.clean_value(row.get('id_vehicule')),
                        'num_veh': self.clean_value(row.get('num_veh')),
                        'place': self.clean_value(row.get('place')),
                        'catu': self.clean_value(row.get('catu')),
                        'grav': self.clean_value(row.get('grav')),
                        'sexe': self.clean_value(row.get('sexe')),
                        'an_nais': self.clean_value(row.get('an_nais')),
                        'trajet': self.clean_value(row.get('trajet')),
                        'secu1': self.clean_value(row.get('secu1')),
                        'secu2': self.clean_value(row.get('secu2')),
                        'secu3': self.clean_value(row.get('secu3')),
                        'locp': self.clean_value(row.get('locp')),
                        'actp': self.clean_value(row.get('actp')),
                        'etatp': self.clean_value(row.get('etatp'))
                    })
        print(f"  Loaded user data for {len(self.usagers)} accidents")
    
    def write_accidents(self, f):
        """Write accident instances to TTL file"""
        f.write("#################################################################\n")
        f.write("# Road Accidents\n")
        f.write("#################################################################\n\n")
        
        for num_acc, data in self.accidents.items():
            f.write(f"ra:Acc_{num_acc} a ra:RoadAccident ;\n")
            
            if data['dep']:
                f.write(f"  ra:inDepartment ra:Dep_{data['dep']} ;\n")
            
            if data['jour']:
                f.write(f"  ra:jour {data['jour']} ;\n")
            if data['mois']:
                f.write(f"  ra:mois {data['mois']} ;\n")
            if data['an']:
                f.write(f"  ra:an {data['an']} ;\n")
            if data['hrmn']:
                f.write(f'  ra:hrmn "{data["hrmn"]}" ;\n')
            if data['lum']:
                f.write(f"  ra:lum {data['lum']} ;\n")
            # if data['dep']:
            #     f.write(f"  ra:dep {data['dep']} ;\n")
            if data['com']:
                f.write(f"  ra:com {data['com']} ;\n")
            if data['agg']:
                f.write(f"  ra:agg {data['agg']} ;\n")
            if data['int']:
                f.write(f"  ra:int {data['int']} ;\n")
            if data['atm']:
                f.write(f"  ra:atm {data['atm']} ;\n")
            if data['col']:
                f.write(f"  ra:col {data['col']} ;\n")
            if data['adr']:
                adr_escaped = data['adr'].replace('\\', '\\\\').replace('"', '\\"')
                f.write(f'  ra:adr "{adr_escaped}" ;\n')
            if data['lat']:
                f.write(f'  ra:lat "{data["lat"]}" ;\n')
            if data['long']:
                f.write(f'  ra:long "{data["long"]}" ;\n')
            
            # Link to location if exists
            if num_acc in self.lieux:
                f.write(f"  ra:hasLocation ra:Lieu_{num_acc} ;\n")
            
            f.write("  .\n\n")
    
    def write_lieux(self, f):
        """Write location instances to TTL file"""
        f.write("#################################################################\n")
        f.write("# Locations\n")
        f.write("#################################################################\n\n")
        
        for num_acc, locations in self.lieux.items():
            for idx, lieu in enumerate(locations):
                lieu_id = f"{num_acc}_{idx}" if len(locations) > 1 else num_acc
                f.write(f"ra:Lieu_{lieu_id} a ra:Location ;\n")
                
                if lieu['catr']:
                    f.write(f"  ra:catr {lieu['catr']} ;\n")
                if lieu['voie']:
                    voie_escaped = lieu['voie'].replace('\\', '\\\\').replace('"', '\\"')
                    f.write(f'  ra:voie "{voie_escaped}" ;\n')
                if lieu['v1']:
                    f.write(f'  ra:v1 "{lieu["v1"]}" ;\n')
                if lieu['v2']:
                    f.write(f'  ra:v2 "{lieu["v2"]}" ;\n')
                if lieu['circ']:
                    f.write(f"  ra:circ {lieu['circ']} ;\n")
                if lieu['nbv']:
                    f.write(f"  ra:nbv {lieu['nbv']} ;\n")
                if lieu['vosp']:
                    f.write(f"  ra:vosp {lieu['vosp']} ;\n")
                if lieu['prof']:
                    f.write(f"  ra:prof {lieu['prof']} ;\n")
                if lieu['pr']:
                    f.write(f'  ra:pr "{lieu["pr"]}" ;\n')
                if lieu['pr1']:
                    f.write(f'  ra:pr1 "{lieu["pr1"]}" ;\n')
                if lieu['plan']:
                    f.write(f"  ra:plan {lieu['plan']} ;\n")
                if lieu['lartpc']:
                    f.write(f'  ra:lartpc "{lieu["lartpc"]}" ;\n')
                if lieu['larrout']:
                    f.write(f'  ra:larrout "{lieu["larrout"]}" ;\n')
                if lieu['surf']:
                    f.write(f"  ra:surf {lieu['surf']} ;\n")
                if lieu['infra']:
                    f.write(f"  ra:infra {lieu['infra']} ;\n")
                if lieu['situ']:
                    f.write(f"  ra:situ {lieu['situ']} ;\n")
                if lieu['vma']:
                    f.write(f'  ra:vma "{lieu["vma"]}" ;\n')
                
                f.write("  .\n\n")
    
    def write_vehicules(self, f):
        """Write vehicle instances to TTL file"""
        f.write("#################################################################\n")
        f.write("# Vehicles\n")
        f.write("#################################################################\n\n")
        
        for num_acc, vehicles in self.vehicules.items():
            for veh in vehicles:
                veh_id = veh['id_vehicule'].replace(' ', '')
                f.write(f"ra:Veh_{veh_id} a ra:Vehicle ;\n")
                
                if veh['num_veh']:
                    f.write(f'  ra:numVeh "{veh["num_veh"]}" ;\n')
                if veh['senc']:
                    f.write(f"  ra:senc {veh['senc']} ;\n")
                if veh['catv']:
                    f.write(f"  ra:catv {veh['catv']} ;\n")
                if veh['obs']:
                    f.write(f"  ra:obs {veh['obs']} ;\n")
                if veh['obsm']:
                    f.write(f"  ra:obsm {veh['obsm']} ;\n")
                if veh['choc']:
                    f.write(f"  ra:choc {veh['choc']} ;\n")
                if veh['manv']:
                    f.write(f"  ra:manv {veh['manv']} ;\n")
                if veh['motor']:
                    f.write(f"  ra:motor {veh['motor']} ;\n")
                if veh['occutc']:
                    f.write(f'  ra:occutc "{veh["occutc"]}" ;\n')
                
                # Link to accident
                f.write(f"  ra:vehicleInvolvedIn ra:Acc_{num_acc} ;\n")
                
                f.write("  .\n\n")
    
    def write_usagers(self, f):
        """Write user/person instances to TTL file"""
        f.write("#################################################################\n")
        f.write("# Persons/Users\n")
        f.write("#################################################################\n\n")
        
        for num_acc, users in self.usagers.items():
            for user in users:
                user_id = user['id_usager'].replace(' ', '')
                
                # Determine if Man or Woman based on sexe field
                sexe = user.get('sexe')
                if sexe == '1':
                    person_type = "ra:Man"
                elif sexe == '2':
                    person_type = "ra:Woman"
                else:
                    person_type = "ra:Person"

                
       
                
                f.write(f"ra:Person_{user_id} a {person_type} ;\n")

                
                if user['id_vehicule']:
                    veh_id = user['id_vehicule'].replace(' ', '')
                    # Determine if driver or occupant based on catu field
                    catu = user.get('catu')
                    if catu == '1':
                        f.write(f"  ra:driverOf ra:Veh_{veh_id} ;\n")
                    if catu == '2':
                        f.write(f"  ra:occupantOf ra:Veh_{veh_id} ;\n")
                
                if user['num_veh']:
                    f.write(f'  ra:numVehPers "{user["num_veh"]}" ;\n')
                if user['place']:
                    f.write(f"  ra:place {user['place']} ;\n")
                if user['catu']:
                    f.write(f"  ra:catu {user['catu']} ;\n")
                if user['grav']:
                    f.write(f"  ra:grav {user['grav']} ;\n")
                if user['an_nais']:
                    f.write(f"  ra:anNais {user['an_nais']} ;\n")
                if user['trajet']:
                    f.write(f"  ra:trajet {user['trajet']} ;\n")
                if user['secu1']:
                    f.write(f"  ra:secu1 {user['secu1']} ;\n")
                if user['secu2']:
                    f.write(f"  ra:secu2 {user['secu2']} ;\n")
                if user['secu3']:
                    f.write(f"  ra:secu3 {user['secu3']} ;\n")
                if user['locp']:
                    f.write(f"  ra:locp {user['locp']} ;\n")
                if user['actp']:
                    f.write(f'  ra:actp "{user["actp"]}" ;\n')
                if user['etatp']:
                    f.write(f"  ra:etatp {user['etatp']} ;\n")
                
                # Link to accident
                f.write(f"  ra:involvedIn ra:Acc_{num_acc} ;\n")
                
                f.write("  .\n\n")
    
    def convert(self):
        """Main conversion process"""
        print("Starting CSV to TTL conversion...")
        
        # Read all CSV files
        self.read_caract()
        self.read_lieux()
        self.read_vehicules()
        self.read_usagers()
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write TTL file
        print(f"\nWriting TTL file to {self.output_file}...")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            self.write_header(f)
            self.write_departements(f)
            self.write_accidents(f)
            self.write_lieux(f)
            self.write_vehicules(f)
            self.write_usagers(f)
        
        print(f"\nConversion complete!")
        print(f"  Total accidents: {len(self.accidents)}")
        print(f"  Total locations: {sum(len(v) for v in self.lieux.values())}")
        print(f"  Total vehicles: {sum(len(v) for v in self.vehicules.values())}")
        print(f"  Total persons: {sum(len(v) for v in self.usagers.values())}")
        print(f"\nOutput saved to: {self.output_file}")


def main():
    """Main entry point"""
    # Define paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    data_dir = project_dir / "data"
    output_file = project_dir / "output" / "instances.ttl"
    
    # Create converter and run
    converter = CSVToTTLConverter(data_dir, output_file)
    converter.convert()


if __name__ == "__main__":
    main()
