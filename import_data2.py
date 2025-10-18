import csv
import os
from datetime import datetime
from collections import defaultdict

try:
    # 你提供的原始数据
    data = """2025-06-01	支出	外食	780	JPY	三井NL
2025-06-01	支出	日用品	2980	JPY	三井master
2025-09-30	支出	外食	1100	JPY	三井NL
2025-09-30	支出	房租	117160	JPY	epos		"""

    # 按月份分组
    monthly_data = defaultdict(list)

    lines = data.strip().split('\n')
    for line in lines:
        parts = line.split('\t')
        if len(parts) >= 5:
            date_str = parts[0]
            date = datetime.strptime(date_str, '%Y-%m-%d')
            month_key = date.strftime('%Y-%m')
            monthly_data[month_key].append(parts)

    # 创建目录和CSV文件
    base_dir = r'C:\Users\liu\accounting\2025'

    for month_key in sorted(monthly_data.keys()):
        records = monthly_data[month_key]

        # 创建CSV文件
        month_num = month_key.split('-')[1]
        csv_file = os.path.join(base_dir, f'{month_num}.csv')

        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['日期', '类型', '分类', '金额', '币种', '账户', '商户', '备注'])

            for record in records:
                # 补齐不足8列的记录
                while len(record) < 8:
                    record.append('')
                writer.writerow(record[:8])

        print(f'已创建 {csv_file}，包含 {len(records)} 条记录')

    print('\n导入完成！')

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
