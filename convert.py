# -*- coding: utf-8 -*-
import os

base = r'C:\Users\liu\accounting\2025'
files = ['06.csv', '07.csv', '08.csv', '09.csv', '10.csv']

for fname in files:
    fpath = os.path.join(base, fname)
    # 读取UTF-8
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 写入UTF-8-BOM
    with open(fpath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print(f'{fname} 已转换')

print('全部完成!')
