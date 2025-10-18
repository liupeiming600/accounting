# -*- coding: utf-8 -*-
import os
import sys
from utils_csv import read_csv, write_csv, normalize_row, validate_row, aggregate


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def write_summary_csv(path, summary: dict, key_name: str):
    rows = []
    for key, vals in summary.items():
        rows.append({
            key_name: key,
            '收入': f"{vals['收入']:.2f}",
            '支出': f"{vals['支出']:.2f}",
            '净额': f"{vals['净额']:.2f}",
        })
    # Keep UTF-8 BOM and simple header order
    import csv
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[key_name, '收入', '支出', '净额'])
        w.writeheader()
        for r in rows:
            w.writerow(r)


def summarize_month(month_csv: str):
    rows = [normalize_row(r) for r in read_csv(month_csv)]
    # Best-effort validation (non-fatal)
    errs = []
    for r in rows:
        es = validate_row(r)
        if es:
            errs.append(es)
    s_cat, s_acc, s_cur = aggregate(rows)
    # 输出到 YYYY/MM/ 目录（若按 2025/10.csv 这种布局）
    base_dir = os.path.dirname(month_csv)
    mm = os.path.splitext(os.path.basename(month_csv))[0]
    month_dir = os.path.join(base_dir, mm)
    os.makedirs(month_dir, exist_ok=True)
    write_summary_csv(os.path.join(month_dir, 'summary_by_category.csv'), s_cat, '分类')
    write_summary_csv(os.path.join(month_dir, 'summary_by_account.csv'), s_acc, '账户')
    write_summary_csv(os.path.join(month_dir, 'summary_by_currency.csv'), s_cur, '币种')
    print(f'Summary written in {month_dir} (category/account/currency). Warnings: {len(errs)}')


def main():
    if len(sys.argv) >= 2:
        target = sys.argv[1]
        if os.path.isdir(target):
            month_csv = os.path.join(target, os.path.basename(target) + '.csv')
        else:
            month_csv = target
    else:
        print('Usage: python tools/summarize_month.py 2025/10.csv or 2025/10')
        sys.exit(1)

    if not os.path.exists(month_csv):
        print(f'Not found: {month_csv}')
        sys.exit(1)
    summarize_month(month_csv)


if __name__ == '__main__':
    main()
