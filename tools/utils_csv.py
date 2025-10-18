# -*- coding: utf-8 -*-
import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Iterable, Tuple


COLUMNS = ['日期', '类型', '分类', '金额', '币种', '账户', '商户', '备注']

VALID_TYPES = {'支出', '收入', '转账'}
VALID_CURRENCIES = {'JPY', 'RMB'}


def read_csv(path: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not os.path.exists(path):
        return rows
    with open(path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        # Tolerate header variants by mapping known names
        header = reader.fieldnames or []
        mapping = _build_header_mapping(header)
        for r in reader:
            row = {col: (r.get(mapping.get(col, col), '') or '').strip() for col in COLUMNS}
            rows.append(row)
    return rows


def write_csv(path: str, rows: Iterable[Dict[str, str]]):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, '') for k in COLUMNS})


def _build_header_mapping(header: List[str]) -> Dict[str, str]:
    # Map canonical column -> actual header name in file
    normalize = {
        '日期': {'日期', 'date'},
        '类型': {'类型', 'type'},
        '分类': {'分类', 'category'},
        '金额': {'金额', 'amount'},
        '币种': {'币种', 'currency'},
        '账户': {'账户', 'account'},
        '商户': {'商户', 'merchant'},
        '备注': {'备注', 'note', 'notes', 'comment'},
    }
    header_lower = {h.lower(): h for h in header}
    mapping: Dict[str, str] = {}
    for canon, aliases in normalize.items():
        for a in aliases:
            key = a.lower()
            if key in header_lower:
                mapping[canon] = header_lower[key]
                break
    return mapping


_ACCOUNT_MAP = {
    'paypay': 'PayPay',
    'rakutenpay': '乐天Pay',
    'rakuten pay': '乐天Pay',
    'ana pay': 'ANA Pay',
    'jal pay': 'JAL Pay',
    'waon': 'WAON',
    'paseli': 'Paseli',
    'suica': 'Suica',
    'amexgold': 'Amex Gold',
    'amex gold': 'Amex Gold',
    'view card': 'View Card',
    '三井nl': '三井NL',
    '三井olive': '三井Olive',
    '三井master': '三井master',
}

_CATEGORY_MAP = {
    '外食': '外食',
    '娱乐': '娱乐',
    '游戏': '游戏',
    '买菜': '买菜',
    '日用品': '日用品',
    '便利店': '便利店',
    '交通费': '交通费',
    '光热费': '光热费',
    '房租': '房租',
    '医疗': '医疗',
    '衣服': '衣服',
    '书籍': '书籍',
    '旅游': '旅游',
    '谷子': '谷子',
    '转账': '转账',
}


def normalize_row(row: Dict[str, str]) -> Dict[str, str]:
    r = {k: (row.get(k, '') or '').strip() for k in COLUMNS}
    # 日期标准化
    if r['日期']:
        try:
            dt = datetime.strptime(r['日期'], '%Y-%m-%d')
            r['日期'] = dt.strftime('%Y-%m-%d')
        except Exception:
            pass
    # 币种标准化
    cur = r['币种'].upper()
    if cur == 'CNY':
        cur = 'RMB'
    r['币种'] = cur
    # 账户标准化（大小写/空格）
    key = re.sub(r'\s+', ' ', r['账户']).strip().lower()
    if key in _ACCOUNT_MAP:
        r['账户'] = _ACCOUNT_MAP[key]
    # 分类标准化（尽量映射；未知保留原值）
    r['分类'] = _CATEGORY_MAP.get(r['分类'], r['分类'])
    # 金额去除千分位
    amt = r['金额'].replace(',', '').strip()
    r['金额'] = amt
    return r


def validate_row(row: Dict[str, str]) -> List[str]:
    errors: List[str] = []
    # 列完备
    for c in COLUMNS:
        if c not in row:
            errors.append(f'缺少列: {c}')
    # 日期
    d = row.get('日期', '')
    try:
        datetime.strptime(d, '%Y-%m-%d')
    except Exception:
        errors.append(f'日期非法: {d}')
    # 类型
    t = row.get('类型', '')
    if t not in VALID_TYPES:
        errors.append(f'类型非法: {t}')
    # 金额
    a = row.get('金额', '')
    try:
        float(a)
    except Exception:
        errors.append(f'金额非法: {a}')
    # 币种
    c = row.get('币种', '').upper()
    if c not in VALID_CURRENCIES:
        errors.append(f'币种非法: {c}')
    return errors


def is_transfer(row: Dict[str, str]) -> bool:
    return row.get('分类') == '转账' or row.get('类型') == '转账'


def dedup_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    out: List[Dict[str, str]] = []
    for r in rows:
        key = tuple(r.get(k, '') for k in COLUMNS)
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def sort_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    return sorted(rows, key=lambda r: (r.get('日期', ''), r.get('类型', ''), r.get('分类', ''), r.get('金额', '')))


def ensure_bom(path: str):
    rows = read_csv(path)
    write_csv(path, rows)


def month_key(date_str: str) -> Tuple[str, str]:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%Y'), dt.strftime('%m')


def aggregate(rows: Iterable[Dict[str, str]]):
    summary_by_category: Dict[str, Dict[str, float]] = {}
    summary_by_account: Dict[str, Dict[str, float]] = {}
    summary_by_currency: Dict[str, Dict[str, float]] = {}

    def add(sumdict: Dict[str, Dict[str, float]], key: str, t: str, amount: float):
        d = sumdict.setdefault(key, {'收入': 0.0, '支出': 0.0, '净额': 0.0})
        if t == '收入':
            d['收入'] += amount
            d['净额'] += amount
        elif t == '支出':
            d['支出'] += amount
            d['净额'] -= amount

    for r in rows:
        if is_transfer(r):
            continue
        try:
            amt = float(r['金额'])
        except Exception:
            continue
        t = r['类型']
        add(summary_by_category, r['分类'] or '(未分类)', t, amt)
        add(summary_by_account, r['账户'] or '(未账户)', t, amt)
        add(summary_by_currency, r['币种'] or '(未币种)', t, amt)

    return summary_by_category, summary_by_account, summary_by_currency

