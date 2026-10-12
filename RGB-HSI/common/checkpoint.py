"""Evaluate a retained RGB-HSI checkpoint using its original embedded config."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--alignment-manifest', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--device', choices=('cpu', 'cuda'), default='cpu')
    parser.add_argument('--eval-split', choices=('validation', 'test'), default='test')
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error('Choose a new output directory to preserve existing results')
    import torch
    state = torch.load(args.checkpoint, map_location='cpu', weights_only=True)
    config = dict(state['config'])
    if config.get('alignment_manifest'):
        if not args.alignment_manifest:
            parser.error('Specify the original registration manifest with --alignment-manifest')
        digest = hashlib.sha256(args.alignment_manifest.read_bytes()).hexdigest()
        if config.get('alignment_sha256') and config['alignment_sha256'] != digest:
            parser.error('Registration manifest hash differs from checkpoint')
        config['alignment_manifest'] = str(args.alignment_manifest.resolve())
    elif args.alignment_manifest:
        parser.error('This checkpoint did not use registration')
    config.update(data_root=str(args.data_root.resolve()), output_dir=str(args.output_dir.resolve()),
                  device=args.device, amp=False, workers=0)
    with tempfile.TemporaryDirectory(prefix='rgb-hsi-evaluate-') as temp:
        path = Path(temp) / 'config.json'
        path.write_text(json.dumps(config), encoding='utf-8')
        command = [sys.executable, str(ROOT/'RGB-HSI/common/train.py'), '--config', str(path),
                   '--evaluate', '--checkpoint', str(args.checkpoint.resolve()), '--eval-split', args.eval_split]
        if config.get('train_area_consistency'):
            command.append('--area-consistency')
        raise SystemExit(subprocess.call(command, cwd=ROOT))

if __name__ == '__main__':
    main()
