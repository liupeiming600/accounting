# -*- coding: utf-8 -*-
import os
import sys
from utils_csv import read_csv, normalize_row, COLUMNS


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def md_escape(text: str) -> str:
    return (text or '').replace('|', '\\|').replace('\n', ' ')


def export_markdown(month_csv: str, out_path: str):
    rows = [normalize_row(r) for r in read_csv(month_csv)]
    header = '| ' + ' | '.join(COLUMNS) + ' |\n'
    sep = '| ' + ' | '.join(['---'] * len(COLUMNS)) + ' |\n'
    lines = [header, sep]
    for r in rows:
        lines.append('| ' + ' | '.join(md_escape(r.get(c, '')) for c in COLUMNS) + ' |\n')
    if out_path == '-':
        # print to stdout without writing any file
        import sys as _sys
        _sys.stdout.write(''.join(lines))
    else:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'Exported {len(rows)} rows to {out_path}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python tools/export_markdown.py 2025/10.csv [out.md]')
        sys.exit(1)
    month_csv = sys.argv[1]
    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        # default to YYYY/MM/records.md
        base_dir = os.path.dirname(month_csv)
        mm = os.path.splitext(os.path.basename(month_csv))[0]
        out_path = os.path.join(base_dir, mm, 'records.md')
    export_markdown(month_csv, out_path)


if __name__ == '__main__':
    main()
