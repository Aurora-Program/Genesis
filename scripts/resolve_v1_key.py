import json, pathlib, sys

MAPPING_PATH = pathlib.Path(__file__).resolve().parent.parent / 'catalogs' / 'mapping_v1_to_v2.json'

mapping = json.loads(MAPPING_PATH.read_text(encoding='utf-8'))

def resolve(old_key: str):
    try:
        return mapping[old_key]
    except KeyError:
        raise SystemExit(f"Key not found: {old_key}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python resolve_v1_key.py <old.key.path>")
        raise SystemExit(1)
    print(resolve(sys.argv[1]))
