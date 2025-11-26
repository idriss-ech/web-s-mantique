import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_ref_map(subdir, filename, key_col, val_col, delimiter=','):
    ref_map = {}
    path = os.path.join(DATA_DIR, subdir, filename)
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                k = row.get(key_col)
                v = row.get(val_col)
                if k and v:
                    ref_map[k.strip()] = v.strip()
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return ref_map

print("--- Checking Vehicules CSV ---")
with open(os.path.join(DATA_DIR, 'vehicules-2024.csv'), 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    print(f"Fieldnames: {reader.fieldnames}")
    for i, row in enumerate(reader):
        if i > 0: break
        print(f"Row 0: {row}")
        print(f"catv value: '{row.get('catv')}'")

print("\n--- Checking REF_CATV ---")
REF_CATV = load_ref_map('ref-veh', 'Catv.csv', 'Code', 'Description', ',')
print(f"REF_CATV size: {len(REF_CATV)}")
print(f"Sample keys: {list(REF_CATV.keys())[:5]}")
