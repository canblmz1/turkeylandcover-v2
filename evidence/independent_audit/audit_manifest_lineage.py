#!/usr/bin/env python3
"""Verify whether adding canonical_class explains the validation CSV hash change.
No source files are modified; the historical representation is reconstructed
in memory and checked against the hash written in the frozen YAML.
"""
import argparse,csv,hashlib,io,json,re
from pathlib import Path

def main(base: Path, out: Path) -> None:
    raw=(base/'metadata_and_splits/v2_spatial_val_50k_fixed.csv').read_bytes()
    config=(base/'configs/v2_50k_frozen.yaml').read_text()
    section=config.split('    validation:',1)[1].split('    sealed_test:',1)[0]
    target=re.search(r'sha256:\s*"([a-f0-9]{64})"',section).group(1)
    rows=list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))
    keep=[i for i,c in enumerate(rows[0]) if c!='canonical_class']
    buf=io.StringIO(newline='');writer=csv.writer(buf,lineterminator='\r\n')
    writer.writerows([[r[i] for i in keep] for r in rows])
    reconstructed=buf.getvalue().encode('utf-8')
    digest=hashlib.sha256(reconstructed).hexdigest()
    result={'rows':len(rows)-1,'current_sha256':hashlib.sha256(raw).hexdigest(),
            'frozen_yaml_sha256':target,'reconstructed_sha256':digest,
            'reconstructed_matches_frozen_hash':digest==target,
            'only_change_needed':'Addition of canonical_class column; original column values, order and CRLF serialization preserved.'}
    out.mkdir(parents=True,exist_ok=True)
    (out/'validation_manifest_lineage.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('base',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();main(a.base,a.out)
