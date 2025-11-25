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
        f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        f.write("@prefix dbpedia: <http://dbpedia.org/resource/> .\n\n")
        
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
            if data['dep']:
                f.write(f"  ra:dep {data['dep']} ;\n")
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
    output_file = project_dir / "protege" / "instances.ttl"
    
    # Create converter and run
    converter = CSVToTTLConverter(data_dir, output_file)
    converter.convert()


if __name__ == "__main__":
    main()
