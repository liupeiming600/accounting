# -*- coding: utf-8 -*-
import os
import glob
from utils_csv import read_csv, write_csv, normalize_row, validate_row, dedup_rows, sort_rows, COLUMNS


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, '2025')
LEDGER_PATH = os.path.join(BASE_DIR, 'ledger.csv')


def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, '[0-1][0-9].csv')))
    all_rows = []
    errors = []
    for fp in files:
        for r in read_csv(fp):
            r = normalize_row(r)
            es = validate_row(r)
            if es:
                errors.append((fp, r, es))
            all_rows.append(r)

    # 去重+排序
    all_rows = sort_rows(dedup_rows(all_rows))
    write_csv(LEDGER_PATH, all_rows)

    print(f'Merged {len(files)} files -> {LEDGER_PATH}')
    print(f'Rows: {len(all_rows)}')
    if errors:
        print(f'Validation warnings: {len(errors)}')
        for fp, r, es in errors[:10]:
            print(f'- {fp}: {"; ".join(es)} @ {r}')
        if len(errors) > 10:
            print('...')


if __name__ == '__main__':
    main()

