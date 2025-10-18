# -*- coding: utf-8 -*-
import os
import sys
import argparse
from datetime import datetime
from utils_csv import read_csv, write_csv, normalize_row, validate_row, dedup_rows, COLUMNS, month_key


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def append_row(record: dict):
    r = normalize_row(record)
    errs = validate_row(r)
    if errs:
        raise SystemExit('校验失败: ' + '; '.join(errs))
    y, m = month_key(r['日期'])
    month_dir = os.path.join(BASE_DIR, y)
    month_csv = os.path.join(month_dir, f'{m}.csv')
    rows = read_csv(month_csv)
    rows.append(r)
    rows = dedup_rows(rows)
    write_csv(month_csv, rows)
    print(f'已写入 {month_csv}: {r}')


def parse_args(argv):
    p = argparse.ArgumentParser(description='追加一条记账记录到对应月份 CSV (UTF-8 BOM)。')
    p.add_argument('--date', required=True, help='日期 YYYY-MM-DD')
    p.add_argument('--type', required=True, dest='类型', choices=['支出', '收入', '转账'])
    p.add_argument('--category', required=True, dest='分类')
    p.add_argument('--amount', required=True, dest='金额')
    p.add_argument('--currency', required=True, dest='币种')
    p.add_argument('--account', required=True, dest='账户')
    p.add_argument('--merchant', default='', dest='商户')
    p.add_argument('--note', default='', dest='备注')
    args = p.parse_args(argv)
    rec = {
        '日期': args.date,
        '类型': args.类型,
        '分类': args.分类,
        '金额': args.金额,
        '币种': args.币种,
        '账户': args.账户,
        '商户': args.商户,
        '备注': args.备注,
    }
    return rec


def main():
    rec = parse_args(sys.argv[1:])
    append_row(rec)


if __name__ == '__main__':
    main()

