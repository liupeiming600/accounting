# -*- coding: utf-8 -*-
import os
import glob
from typing import Optional


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_GLOBS = [
    os.path.join(BASE_DIR, '2025', '[0-1][0-9].csv'),
]
CANDIDATE_ENCODINGS = ['utf-8-sig', 'utf-8', 'gbk', 'cp936', 'shift_jis', 'cp932']
EXPECTED_HEADER_TOKENS = ['日期', '类型', '分类', '金额', '币种', '账户', '商户', '备注']


def detect_encoding(path: str) -> Optional[str]:
    with open(path, 'rb') as f:
        head = f.read(4096)
    for enc in CANDIDATE_ENCODINGS:
        try:
            txt = head.decode(enc, errors='strict')
        except Exception:
            continue
        first = txt.splitlines()[0] if '\n' in txt else txt
        if all(tok in first for tok in ['日期', '类型']):
            return enc
        # Split by comma and compare tokens loosely
        cols = [c.strip() for c in first.split(',')]
        hit = sum(1 for c in EXPECTED_HEADER_TOKENS if c in cols)
        if hit >= 6:  # tolerate partial header
            return enc
    return None


def repair_file(path: str) -> str:
    enc = detect_encoding(path)
    if not enc:
        return f'SKIP (unknown encoding): {path}'
    if enc.lower().startswith('utf-8'):
        # ensure BOM by re-write
        with open(path, 'r', encoding=enc, newline='') as f:
            content = f.read()
        with open(path, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(content)
        return f'ENSURED UTF-8 BOM: {path}'
    # transcode to UTF-8 BOM
    with open(path, 'r', encoding=enc, newline='') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(content)
    return f'FIXED {enc} -> UTF-8 BOM: {path}'


def main():
    files = []
    for g in DATA_GLOBS:
        files.extend(glob.glob(g))
    files = sorted(files)
    for fp in files:
        print(repair_file(fp))


if __name__ == '__main__':
    main()

