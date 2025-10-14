import json, yaml, pathlib

CATALOG_PATH = pathlib.Path(__file__).resolve().parent.parent / 'catalogs' / 'ffe_catalog.yaml'
MAPPING_PATH = pathlib.Path(__file__).resolve().parent.parent / 'catalogs' / 'mapping_v1_to_v2.json'

class Node:
    __slots__ = ("id","level","parent","path","terminal","values","children")
    def __init__(self, meta):
        self.id = meta['id']
        self.level = meta['level']
        self.parent = meta.get('parent')
        self.path = meta['path']
        self.terminal = meta['terminal']
        self.values = meta.get('values', {})
        self.children = []
    def to_dict(self):
        return {k:getattr(self,k) for k in ("id","level","parent","path","terminal","values","children")}

def load_catalog():
    data = yaml.safe_load(CATALOG_PATH.read_text(encoding='utf-8'))
    axes = data['axes']
    nodes_by_id = {}

    def build(meta):
        node = Node(meta)
        nodes_by_id[node.id] = node
        for group_key in ('subdimensions','specs'):
            for child in meta.get(group_key, []) or []:
                child_node = build(child)
                node.children.append(child_node)
        return node

    roots = [build(a) for a in axes]
    return roots, nodes_by_id

def validate(nodes_by_id):
    errors = []
    # Level distribution
    levels = {}
    for n in nodes_by_id.values():
        levels.setdefault(n.level,0); levels[n.level]+=1
        # terminal consistency
        if n.level == 3 and not n.terminal:
            errors.append(f"Spec {n.id} should be terminal")
        if n.level < 3 and n.terminal:
            errors.append(f"Non-leaf {n.id} marked terminal")
        # value count
        if len(n.values) != 8:
            errors.append(f"Node {n.id} has {len(n.values)} values != 8")
    # Expected counts
    expected = {1:3,2:9,3:27}
    for lvl, exp in expected.items():
        if levels.get(lvl,0) != exp:
            errors.append(f"Level {lvl} count {levels.get(lvl,0)} != {exp}")
    return errors

def load_mapping():
    return json.loads(MAPPING_PATH.read_text(encoding='utf-8'))

if __name__ == '__main__':
    roots, nodes = load_catalog()
    errs = validate(nodes)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs: print(" -", e)
    else:
        print("Catalog v2 OK. Nodes:", len(nodes))
        lvl_counts = {}
        for n in nodes.values():
            lvl_counts[n.level] = lvl_counts.get(n.level,0)+1
        print("Level counts:", lvl_counts)
    mapping = load_mapping()
    print("Mapping entries:", len(mapping))
