# -*- coding: utf-8 -*-
import os
import sys
import csv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
COLUMNS = ['日期', '类型', '分类', '金额', '币种', '账户', '商户', '备注']
CANDIDATE_ENCODINGS = ['utf-8-sig', 'utf-8', 'gbk', 'cp936', 'shift_jis', 'cp932']


def detect_encoding(path: str) -> str:
    with open(path, 'rb') as f:
        head = f.read(4096)
    for enc in CANDIDATE_ENCODINGS:
        try:
            txt = head.decode(enc, errors='strict')
        except Exception:
            continue
        first = txt.splitlines()[0] if '\n' in txt else txt
        if '日期' in first and '类型' in first:
            return enc
        cols = [c.strip() for c in first.split(',')]
        hit = sum(1 for c in COLUMNS if c in cols)
        if hit >= 6:
            return enc
    # fallback
    return 'utf-8-sig'


def md_escape(text: str) -> str:
    return (text or '').replace('|', '\\|').replace('\n', ' ')


def show_month(csv_path: str):
    enc = detect_encoding(csv_path)
    with open(csv_path, 'r', encoding=enc, newline='') as f:
        reader = csv.DictReader(f)
        # header
        print('| ' + ' | '.join(COLUMNS) + ' |')
        print('| ' + ' | '.join(['---'] * len(COLUMNS)) + ' |')
        for r in reader:
            row = [md_escape((r.get(c, '') or '').strip()) for c in COLUMNS]
            print('| ' + ' | '.join(row) + ' |')


def main():
    if len(sys.argv) < 2:
        print('Usage: python tools/show_month.py 2025/10.csv')
        sys.exit(1)
    show_month(sys.argv[1])


if __name__ == '__main__':
    main()

