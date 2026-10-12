#!/usr/bin/env python3
"""Read-only audit of saved TurkeyLandCover V2 predictions (no model inference).
Dependencies: numpy, pandas. Never imports or executes scripts from the evidence.
Usage: python reproduce_audit.py EVIDENCE_DIRECTORY OUTPUT_DIRECTORY
"""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd

CLASSES = ['bare_sparse_vegetation','built_up','cropland','grassland',
           'herbaceous_wetland','permanent_water_bodies','shrubland','tree_cover']
BALANCED = np.array([7616,5504,5349,4885,356,10576,638,5329], dtype=np.float64)
NATURAL = np.array([10004,6652,175485,298287,421,12960,924,175045], dtype=np.float64)
TAU = 0.5
EPS = 1e-12

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def metrics_from_cm(cm):
    cm=np.asarray(cm, dtype=np.int64)
    support=cm.sum(1); predicted=cm.sum(0); tp=cm.diagonal()
    recall=np.divide(tp,support,out=np.zeros(8,dtype=float),where=support!=0)
    precision=np.divide(tp,predicted,out=np.zeros(8,dtype=float),where=predicted!=0)
    f1=np.divide(2*tp,support+predicted,out=np.zeros(8,dtype=float),where=(support+predicted)!=0)
    present=support>0
    return {'n':int(cm.sum()),'correct':int(tp.sum()),'top1':float(tp.sum()/cm.sum()),
            'macro_f1_all8':float(f1.mean()),'macro_f1_present':float(f1[present].mean()),
            'balanced_acc_all8':float(recall.mean()),'balanced_acc_present':float(recall[present].mean()),
            'worst_f1_all8':float(f1.min()),'worst_f1_present':float(f1[present].min()),
            'weighted_f1':float(np.sum(f1*support)/cm.sum()),'present_classes':int(present.sum()),
            'cm':cm.tolist(), 'per_class':{c:{'support':int(support[i]),'predicted_count':int(predicted[i]),
                'tp':int(tp[i]),'precision':float(precision[i]),'recall':float(recall[i]),'f1':float(f1[i])}
                for i,c in enumerate(CLASSES)}}

def metrics(y,p):
    assert y.shape==p.shape and y.ndim==1
    assert np.all((y>=0)&(y<8)) and np.all((p>=0)&(p<8))
    return metrics_from_cm(np.bincount(y*8+p,minlength=64).reshape(8,8))

def province_metrics(y,p,prov):
    return {c:metrics(y[prov==c],p[prov==c]) for c in np.unique(prov)}

def read_npz(p):
    with np.load(p,allow_pickle=False) as z:
        return {k:z[k] for k in z.files}

def main(base,out):
    out.mkdir(parents=True,exist_ok=True)
    assert not out.resolve().is_relative_to(base.resolve()),'Audit output must not overwrite evidence'
    hashes=[]
    for line in (base/'SHA256SUMS.txt').read_text().splitlines():
        h,fn=line.split(maxsplit=1); p=base/fn.strip().lstrip('*')
        hashes.append({'path':fn,'expected':h,'actual':sha(p),'match':sha(p)==h})
    test=read_npz(base/'predictions/test_predictions.npz')
    dev=read_npz(base/'development/balanced_val_logits.npz')
    assert test['class_names'].tolist()==dev['class_names'].tolist()==CLASSES
    assert BALANCED.sum()==40253 and NATURAL.sum()==679778
    delta=np.log(NATURAL/NATURAL.sum()+EPS)-np.log(BALANCED/BALANCED.sum()+EPS)
    logits=test['raw_logits']; y=test['ground_truth_idx']; p=test['pred_idx']; prov=test['province']
    assert logits.shape==(len(y),8) and np.isfinite(logits).all()
    corrected=logits+(TAU*delta).astype(np.float32)
    p_rebuilt=corrected.argmax(1)
    t=metrics(y,p)
    t['top5_correct']=int((np.argsort(corrected,axis=1)[:,-5:]==y[:,None]).any(1).sum())
    t['top5']=t['top5_correct']/len(y)
    tprov=province_metrics(y,p,prov)
    t['mean_province_f1_all8']=float(np.mean([m['macro_f1_all8'] for m in tprov.values()]))
    t['mean_province_f1_present']=float(np.mean([m['macro_f1_present'] for m in tprov.values()]))
    recorded=json.loads((base/'results/v2_final_test_results.json').read_text())
    csv_cm=pd.read_csv(base/'results/confusion_matrix_raw.csv',index_col=0).values
    test_checks={
        'unique_sample_ids':len(np.unique(test['sample_id'])),
        'duplicate_sample_ids':len(y)-len(np.unique(test['sample_id'])),
        'logits_all_finite':bool(np.isfinite(logits).all()),
        'predictions_differ_from_frozen_logit_argmax':int((p!=p_rebuilt).sum()),
        'cm_matches_results_json':bool(np.array_equal(t['cm'],recorded['metrics']['confusion_matrix'])),
        'cm_matches_saved_csv':bool(np.array_equal(t['cm'],csv_cm)),
        'metric_deltas_vs_json':{k:float(t[a]-recorded['metrics'][k]) for a,k in
            [('top1','top1'),('top5','top5'),('macro_f1_all8','macro_f1'),('balanced_acc_all8','balanced_acc'),
             ('worst_f1_all8','worst_f1'),('weighted_f1','weighted_f1')]},
        'frozen_shift_max_abs_diff_vs_json':float(np.max(np.abs((TAU*delta).astype(np.float32)-np.array([recorded['priors']['shift_vector'][c] for c in CLASSES]))))}
    tm=pd.read_csv(base/'metadata_and_splits/v2_spatial_test.csv')
    dm=pd.read_csv(base/'metadata_and_splits/v2_spatial_val_50k_fixed.csv')
    assert tm.sample_id.is_unique and dm.sample_id.is_unique
    tm_index=tm.set_index('sample_id'); dm_index=dm.set_index('sample_id')
    unknown_test=sorted(set(test['sample_id'])-set(tm.sample_id))
    unknown_dev=sorted(set(dev['sample_id'])-set(dm.sample_id))
    assert not unknown_test and not unknown_dev
    excluded=tm[~tm.sample_id.isin(test['sample_id'])]
    excluded.to_csv(out/'excluded_test_manifest_rows.csv',index=False)
    split_checks={'test_manifest_rows':len(tm),'evaluated_test_rows':len(y),'excluded_test_rows':len(excluded),
       'excluded_test_by_province':{str(k):int(v) for k,v in excluded.province_code.value_counts().items()},
       'test_province_mismatch_vs_manifest':int((tm_index.loc[test['sample_id'],'province_code'].values!=prov).sum()),
       'dev_province_mismatch_vs_manifest':int((dm_index.loc[dev['sample_id'],'province_code'].values!=dev['province']).sum()),
       'dev_ground_truth_mismatch_vs_manifest':int((dm_index.loc[dev['sample_id'],'canonical_class'].values!=np.array(CLASSES)[dev['ground_truth_idx']]).sum()),
       'test_dev_sample_overlap':len(set(test['sample_id'])&set(dev['sample_id'])),
       'test_dev_province_overlap':len(set(prov)&set(dev['province'])),
       'train_membership_independently_verifiable':False,
       'test_ground_truth_independently_verifiable':False}
    dy=dev['ground_truth_idx']; dl=dev['logits']; dp=dev['province']
    assert dl.shape==(50000,8) and np.isfinite(dl).all()
    sweep={}; sweep_json=json.loads((base/'development/v2_stage3_results.json').read_text())
    for tau in np.arange(11)/10:
        pred=(dl+tau*delta).argmax(1)
        m=metrics(dy,pred); pm=province_metrics(dy,pred,dp)
        key=f'{tau:.2f}'
        sweep[key]={'tau':float(tau),'top1':m['top1'],'macro_f1':m['macro_f1_all8'],
          'balanced_acc':m['balanced_acc_all8'],'worst_f1':m['worst_f1_all8'],
          'mean_prov_macro_f1_present':float(np.mean([v['macro_f1_present'] for v in pm.values()])),
          'mean_prov_macro_f1_all8':float(np.mean([v['macro_f1_all8'] for v in pm.values()])),
          'province_metrics':pm}
    selected=max(sweep,key=lambda k:(sweep[k]['mean_prov_macro_f1_present'],sweep[k]['worst_f1'],sweep[k]['balanced_acc'],sweep[k]['top1']))
    dsel=metrics(dy,(dl+TAU*delta).argmax(1))
    dprov=sweep['0.50']['province_metrics']
    lopo={}
    for held in np.unique(dp):
        key=max(sweep,key=lambda k:(np.mean([v['macro_f1_present'] for pr,v in sweep[k]['province_metrics'].items() if pr!=held]),
                                     sweep[k]['worst_f1'],sweep[k]['balanced_acc'],sweep[k]['top1']))
        lopo[held]={'tau':sweep[key]['tau'],'held_out_macro_f1_present':sweep[key]['province_metrics'][held]['macro_f1_present']}
    dev_checks={'selected_tau_recomputed':sweep[selected]['tau'],
       'selected_tau_declared':sweep_json['selected_tau'],
       'max_sweep_delta_vs_json':max(abs(sweep[k][own]-sweep_json['tau_sweep'][k][given]) for k in sweep for own,given in
          [('top1','top1'),('macro_f1','macro_f1'),('balanced_acc','balanced_acc'),('worst_f1','worst_f1'),('mean_prov_macro_f1_present','mean_prov_macro_f1')]),
       'lopo':lopo,
       'mean_lopo_heldout_f1':float(np.mean([v['held_out_macro_f1_present'] for v in lopo.values()]))}
    gap={'global_macro_f1':t['macro_f1_all8']-dsel['macro_f1_all8'],
       'mean_province_f1_present':t['mean_province_f1_present']-sweep['0.50']['mean_prov_macro_f1_present'],
       'mean_province_f1_all8':t['mean_province_f1_all8']-sweep['0.50']['mean_prov_macro_f1_all8'],
       'top1':t['top1']-dsel['top1'],'balanced_accuracy':t['balanced_acc_all8']-dsel['balanced_acc_all8']}
    # Reproduce the declared patch-IID bootstrap without any model calls.
    rng=np.random.default_rng(20261012); boot=[]
    for _ in range(1000):
        ix=rng.choice(len(y),size=len(y),replace=True)
        m=metrics(y[ix],p[ix]);boot.append([m['top1'],m['macro_f1_all8'],m['balanced_acc_all8']])
    ci=np.percentile(boot,[2.5,97.5],axis=0).T
    cis={k:ci[i].tolist() for i,k in enumerate(['top1_ci','macro_f1_ci','balanced_acc_ci'])}
    ci_delta=max(abs(cis[k][i]-recorded['metrics']['ci_95'][k][i]) for k in cis for i in range(2))
    result={'hash_verification':hashes,'hashes_all_match':all(h['match'] for h in hashes),
       'test_metrics':t,'test_consistency':test_checks,'split_checks':split_checks,
       'test_provinces':tprov,'development_selected_metrics':dsel,
       'development_checks':dev_checks,'development_sweep':sweep,
       'comparable_dev_to_test_gaps':gap,'bootstrap_patch_iid_95':cis,'bootstrap_max_abs_difference_vs_saved':ci_delta}
    (out/'independent_audit_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    for name,pm in [('test',tprov),('development',dprov)]:
        pd.DataFrame([dict(province=pr,**{k:v for k,v in m.items() if k not in ['cm','per_class']}) for pr,m in pm.items()]).to_csv(out/f'{name}_province_metrics_recomputed.csv',index=False)
    pd.DataFrame([dict(class_name=c,**v) for c,v in t['per_class'].items()]).to_csv(out/'test_class_metrics_recomputed.csv',index=False)
    pd.DataFrame(t['cm'],columns=CLASSES,index=CLASSES).to_csv(out/'test_confusion_matrix_recomputed.csv')
    pd.DataFrame([{k:v for k,v in row.items() if k!='province_metrics'} for row in sweep.values()]).to_csv(out/'development_tau_sweep_recomputed.csv',index=False)
    summary={'hashes':len(hashes),'all_hashes_match':result['hashes_all_match'],'test_checks':test_checks,
             'test_metrics':{k:v for k,v in t.items() if k not in ['cm','per_class']},
             'split_checks':split_checks,'dev_checks':dev_checks,'gaps':gap,'bootstrap_match_max_abs_delta':ci_delta}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence_dir',type=Path);parser.add_argument('output_dir',type=Path)
    args=parser.parse_args();main(args.evidence_dir,args.output_dir)
