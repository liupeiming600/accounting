# -*- coding: utf-8 -*-
import os
from utils_csv import read_csv, write_csv, normalize_row, COLUMNS


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MONTH_CSV = os.path.join(BASE_DIR, '2025', '10.csv')


def main():
    rows = [normalize_row(r) for r in read_csv(MONTH_CSV)]
    out = []
    removed = 0
    # Remove full-amount entries for 2025-10-19 JPY on 乐天Pay merchants: 烤肉(17468) and KTV(4400)
    for r in rows:
        if (
            r.get('日期') == '2025-10-19'
            and r.get('币种') == 'JPY'
            and r.get('账户') == '乐天Pay'
            and (
                (r.get('商户') == '烤肉' and r.get('金额') == '17468') or
                (r.get('商户') == 'KTV' and r.get('金额') == '4400')
            )
        ):
            removed += 1
            continue
        out.append(r)

    # Append 1/4 share entries
    out.append({
        '日期': '2025-10-19', '类型': '支出', '分类': '外食', '金额': '4367',
        '币种': 'JPY', '账户': '乐天Pay', '商户': '烤肉', '备注': '我1/4份'
    })
    out.append({
        '日期': '2025-10-19', '类型': '支出', '分类': '娱乐', '金额': '1100',
        '币种': 'JPY', '账户': '乐天Pay', '商户': 'KTV', '备注': '我1/4份'
    })

    write_csv(MONTH_CSV, out)
    print(f'Adjusted share entries. Removed: {removed}, added: 2 -> {MONTH_CSV}')


if __name__ == '__main__':
    main()

