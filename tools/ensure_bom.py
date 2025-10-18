# -*- coding: utf-8 -*-
import os
import glob
from utils_csv import ensure_bom


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def main():
    targets = []
    targets += [os.path.join(BASE_DIR, 'ledger.csv')]
    targets += glob.glob(os.path.join(BASE_DIR, '2025', '[0-1][0-9].csv'))
    for t in targets:
        if os.path.exists(t):
            ensure_bom(t)
            print(f'Ensured UTF-8 BOM: {t}')


if __name__ == '__main__':
    main()

