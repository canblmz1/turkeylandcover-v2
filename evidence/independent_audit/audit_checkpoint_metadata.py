#!/usr/bin/env python3
"""Read scalar metadata without unpickling/loading/executing a PyTorch model.
Uses pickletools.genops plus a deliberately tiny parser for primitive dict/list
metadata. Rejects class globals, reducers and memo references in parsed values.
Usage: python audit_checkpoint_metadata.py EVIDENCE_DIRECTORY OUTPUT_DIRECTORY
"""
from pathlib import Path
import json, pickletools, zipfile, argparse, hashlib
SKIP={'BINPUT','LONG_BINPUT','MEMOIZE'}
STR={'BINUNICODE','SHORT_BINUNICODE','UNICODE','BINUNICODE8'}
INT={'BININT','BININT1','BININT2','LONG','LONG1','LONG4','INT'}

def skip(ops,i):
    while i<len(ops) and ops[i][0].name in SKIP:i+=1
    return i

def primitive(ops,i):
    i=skip(ops,i);op,arg,pos=ops[i];name=op.name
    if name in STR|INT|{'BINFLOAT','FLOAT'}:return arg,skip(ops,i+1)
    if name=='NEWTRUE':return True,skip(ops,i+1)
    if name=='NEWFALSE':return False,skip(ops,i+1)
    if name=='NONE':return None,skip(ops,i+1)
    if name=='EMPTY_TUPLE':return [],skip(ops,i+1)
    if name in ('EMPTY_DICT','EMPTY_LIST'):
        result={} if name=='EMPTY_DICT' else []
        i=skip(ops,i+1)
        if ops[i][0].name!='MARK':return result,i
        i+=1
        end='SETITEMS' if isinstance(result,dict) else 'APPENDS'
        while ops[i][0].name!=end:
            k,i=primitive(ops,i)
            if isinstance(result,dict):
                v,i=primitive(ops,i);result[k]=v
            else:result.append(k)
        return result,skip(ops,i+1)
    raise ValueError(f'Unsupported opcode {name} at {pos}; metadata parsing stopped safely')

def main(base,out):
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(base/'models/best.pt') as z:
        pk=next(n for n in z.namelist() if n.endswith('/data.pkl'))
        ops=list(pickletools.genops(z.read(pk)))
        selected={}
        # String-key metadata locations only, not arbitrary object deserialization.
        for key in ['date','version','names','train_args','train_metrics','train_results']:
            found=[i for i,(op,arg,pos) in enumerate(ops) if op.name in STR and arg==key]
            # names/train_args/train_metrics/train_results occur once in this checkpoint.
            i=found[0]
            selected[key],_=primitive(ops,skip(ops,i+1))
        selected['inspection_method']='pickletools opcode parsing; no pickle.load, torch.load or model execution'
        selected['model_sha256']=hashlib.sha256((base/'models/best.pt').read_bytes()).hexdigest()
        selected['model_archive_entries']=len(z.namelist())
        selected['tensor_storage_bytes']=sum(i.file_size for i in z.infolist() if '/data/' in i.filename)
    (out/'checkpoint_embedded_metadata.json').write_text(json.dumps(selected,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in selected.items() if k!='train_results'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('base',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();main(a.base,a.out)
