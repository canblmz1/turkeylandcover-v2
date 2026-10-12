import hashlib
import json
from pathlib import Path

def main():
    root = Path('.').resolve()
    
    # Matching exactly the rule in tools/verify_release.py
    actual_files = [
        p for p in root.rglob('*')
        if p.is_file() 
        and not any(part.startswith('.') for part in p.relative_to(root).parts)
        and not p.name.endswith('.zip')
    ]
    
    files = {}
    for p in sorted(actual_files):
        rel = p.relative_to(root).as_posix()
        if rel in ('SHA256SUMS.txt', 'PUBLIC_DISTRIBUTION_MANIFEST.json'):
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        size = p.stat().st_size
        files[rel] = {'sha256': h, 'bytes': size}

    manifest = {
        'package_name': 'TurkeyLandCover_V2_Public_Distribution',
        'version': 'v2.0',
        'status': 'AUDITED_RESEARCH_RELEASE',
        'weights_status': 'PUBLISHED_UNDER_AGPL_3_0',
        'weights_rationale': 'Distributed under GNU AGPL-3.0 in compliance with Ultralytics terms and AGPL-3.0 Section 6 Corresponding Source requirements (see WEIGHTS_DISTRIBUTION_STATUS.md)',
        'target_checkpoint_sha256': '8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a',
        'training_manifest_status': 'UNKNOWN (Internal server split not exported; not an AGPL-3.0 Section 6 statutory requirement)',
        'upstream_initial_weight_sha256': 'UNKNOWN (Historical /mnt/evren_data/cache/ultralytics/yolo11n-cls.pt not backfilled)',
        'upstream_framework': 'Ultralytics YOLO11 v8.3.0 (https://github.com/ultralytics/ultralytics/tree/v8.3.0)',
        'files': dict(sorted(files.items()))
    }

    manifest_path = root / 'PUBLIC_DISTRIBUTION_MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    
    # Now hash the manifest
    manifest_bytes = manifest_path.read_bytes()
    files['PUBLIC_DISTRIBUTION_MANIFEST.json'] = {
        'sha256': hashlib.sha256(manifest_bytes).hexdigest(),
        'bytes': len(manifest_bytes)
    }

    sums_path = root / 'SHA256SUMS.txt'
    lines = [f"{files[rel]['sha256']}  {rel}" for rel in sorted(files.keys())]
    sums_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f"Successfully computed and wrote hashes for {len(files)} files.")

if __name__ == '__main__':
    main()
