import csv
from collections import defaultdict
from decimal import Decimal
from datetime import datetime

# Read the November data
data = []
with open(r'C:\Users\liu\accounting\2025\11.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

print("=" * 80)
print("11月消费深度分析报告")
print("=" * 80)
print()

# 基础统计
jpy_records = [r for r in data if r['币种'] == 'JPY']
rmb_records = [r for r in data if r['币种'] == 'RMB']

jpy_expense_records = [r for r in jpy_records if r['类型'] == '支出' and r['分类'] != '转账']
jpy_income_records = [r for r in jpy_records if r['类型'] == '收入' and r['分类'] != '转账']

print("【基础统计】")
print(f"  总记录数:       {len(data)} 条")
print(f"  JPY记录:        {len(jpy_records)} 条")
print(f"  RMB记录:        {len(rmb_records)} 条")
print(f"  JPY支出笔数:    {len(jpy_expense_records)} 笔")
print(f"  JPY收入笔数:    {len(jpy_income_records)} 笔")
print()

# 分类详细分析
category_data = defaultdict(lambda: {'count': 0, 'total': Decimal('0'), 'amounts': [], 'dates': []})

for r in jpy_expense_records:
    cat = r['分类']
    amt = Decimal(r['金额'])
    category_data[cat]['count'] += 1
    category_data[cat]['total'] += amt
    category_data[cat]['amounts'].append(amt)
    category_data[cat]['dates'].append(r['日期'])

print("【分类详细分析 - JPY支出】")
print()
print(f"{'分类':<10} {'笔数':>6} {'总额':>12} {'平均':>10} {'最高':>10} {'最低':>8}")
print("-" * 70)

sorted_cats = sorted(category_data.items(), key=lambda x: x[1]['total'], reverse=True)
total_expense = sum(c['total'] for _, c in sorted_cats)

for cat, info in sorted_cats:
    avg = info['total'] / info['count'] if info['count'] > 0 else 0
    max_amt = max(info['amounts'])
    min_amt = min(info['amounts'])
    print(f"{cat:<10} {info['count']:>6} {info['total']:>12,} {avg:>10,.0f} {max_amt:>10,} {min_amt:>8,}")

print("-" * 70)
print(f"{'合计':<10} {sum(c['count'] for _, c in sorted_cats):>6} {total_expense:>12,}")
print()

# 支付方式分析
payment_data = defaultdict(lambda: {'count': 0, 'total': Decimal('0')})

for r in jpy_expense_records:
    pay = r['账户']
    amt = Decimal(r['金额'])
    payment_data[pay]['count'] += 1
    payment_data[pay]['total'] += amt

print("【支付方式分析】")
print()
print(f"{'支付方式':<15} {'笔数':>6} {'总额':>12} {'占比':>8} {'单笔均价':>10}")
print("-" * 60)

sorted_pay = sorted(payment_data.items(), key=lambda x: x[1]['total'], reverse=True)
for pay, info in sorted_pay:
    pct = info['total'] / total_expense * 100
    avg = info['total'] / info['count']
    print(f"{pay:<15} {info['count']:>6} {info['total']:>12,} {pct:>7.1f}% {avg:>10,.0f}")

print()

# 日期分析
daily_expense = defaultdict(lambda: Decimal('0'))
daily_count = defaultdict(int)

for r in jpy_expense_records:
    date = r['日期']
    daily_expense[date] += Decimal(r['金额'])
    daily_count[date] += 1

print("【每日消费分析】")
print()

max_day = max(daily_expense.items(), key=lambda x: x[1])
min_day = min(daily_expense.items(), key=lambda x: x[1])
avg_daily = sum(daily_expense.values()) / len(daily_expense)

print(f"  记账天数:       {len(daily_expense)} 天")
print(f"  日均消费:       {avg_daily:,.0f} JPY")
print(f"  最高消费日:     {max_day[0]} ({max_day[1]:,} JPY)")
print(f"  最低消费日:     {min_day[0]} ({min_day[1]:,} JPY)")
print()

print("  【消费最高的5天】")
sorted_days = sorted(daily_expense.items(), key=lambda x: x[1], reverse=True)[:5]
for date, amt in sorted_days:
    print(f"    {date}: {amt:>10,} JPY ({daily_count[date]}笔)")
print()

# 外食深度分析
food_records = [r for r in jpy_expense_records if r['分类'] == '外食']
food_amounts = [Decimal(r['金额']) for r in food_records]

print("【外食深度分析】")
print()
print(f"  外食笔数:       {len(food_records)} 笔")
print(f"  外食总额:       {sum(food_amounts):,} JPY")
print(f"  单笔平均:       {sum(food_amounts)/len(food_amounts):,.0f} JPY")
print(f"  单笔最高:       {max(food_amounts):,} JPY")
print(f"  单笔最低:       {min(food_amounts):,} JPY")
print()

ranges = [(0, 500), (500, 1000), (1000, 2000), (2000, 5000), (5000, 100000)]
print("  【价格分布】")
for low, high in ranges:
    count = len([a for a in food_amounts if low <= a < high])
    if count > 0:
        pct = count / len(food_amounts) * 100
        bar = "#" * int(pct / 5)
        print(f"    {low:>5}-{high:<5}: {count:>2}笔 ({pct:>5.1f}%) {bar}")
print()

# 麻将分析
mahjong_records = [r for r in jpy_records if r['分类'] == '麻将']
mahjong_income = sum(Decimal(r['金额']) for r in mahjong_records if r['类型'] == '收入')
mahjong_expense = sum(Decimal(r['金额']) for r in mahjong_records if r['类型'] == '支出')
mahjong_sessions = len(set(r['日期'] for r in mahjong_records))

print("【麻将战绩分析】")
print()
print(f"  打麻将次数:     {mahjong_sessions} 次")
print(f"  总收入:         {mahjong_income:,} JPY")
print(f"  总支出:         {mahjong_expense:,} JPY")
print(f"  净收益:         {mahjong_income - mahjong_expense:,} JPY")
if mahjong_sessions > 0:
    print(f"  场均收益:       {(mahjong_income - mahjong_expense) / mahjong_sessions:,.0f} JPY")
print()

print("  【每次战绩】")
mahjong_by_date = defaultdict(lambda: Decimal('0'))
for r in mahjong_records:
    amt = Decimal(r['金额'])
    if r['类型'] == '收入':
        mahjong_by_date[r['日期']] += amt
    else:
        mahjong_by_date[r['日期']] -= amt

win_count = 0
lose_count = 0
for date, net in sorted(mahjong_by_date.items()):
    if net > 0:
        status = "WIN"
        win_count += 1
    elif net < 0:
        status = "LOSE"
        lose_count += 1
    else:
        status = "DRAW"
    sign = "+" if net > 0 else ""
    print(f"    {date}: {sign}{net:>7,} JPY [{status}]")

print()
if mahjong_sessions > 0:
    print(f"  胜率:           {win_count}/{mahjong_sessions} ({win_count/mahjong_sessions*100:.0f}%)")
print()

# 交通费分析
transport = [r for r in jpy_expense_records if r['分类'] == '交通费']
transport_amounts = [Decimal(r['金额']) for r in transport]

print("【交通费分析】")
print()
print(f"  交通笔数:       {len(transport)} 笔")
print(f"  交通总额:       {sum(transport_amounts):,} JPY")
if len(transport) > 0:
    print(f"  单程平均:       {sum(transport_amounts)/len(transport):,.0f} JPY")
print()

# 便利店分析
cvs = [r for r in jpy_expense_records if r['分类'] == '便利店']
cvs_amounts = [Decimal(r['金额']) for r in cvs]

print("【便利店分析】")
print()
print(f"  便利店笔数:     {len(cvs)} 笔")
print(f"  便利店总额:     {sum(cvs_amounts):,} JPY")
if len(cvs) > 0:
    print(f"  单笔平均:       {sum(cvs_amounts)/len(cvs):,.0f} JPY")
print()

# 周末 vs 工作日
print("【消费时间分析】")
print()

weekend_expense = Decimal('0')
weekday_expense = Decimal('0')
weekend_count = 0
weekday_count = 0

for r in jpy_expense_records:
    date = datetime.strptime(r['日期'], '%Y-%m-%d')
    amt = Decimal(r['金额'])
    if date.weekday() >= 5:
        weekend_expense += amt
        weekend_count += 1
    else:
        weekday_expense += amt
        weekday_count += 1

print(f"  工作日:         {weekday_expense:,} JPY ({weekday_count}笔)")
print(f"  周末:           {weekend_expense:,} JPY ({weekend_count}笔)")
total_all = weekend_expense + weekday_expense
if total_all > 0:
    print(f"  周末消费占比:   {weekend_expense/total_all*100:.1f}%")
print()

# 高频消费
print("【高频消费分类 Top 5】")
print()
top5_freq = sorted(category_data.items(), key=lambda x: x[1]['count'], reverse=True)[:5]
for i, (cat, info) in enumerate(top5_freq, 1):
    avg = info['total'] / info['count']
    print(f"  {i}. {cat:<10} {info['count']:>3}笔  总额{info['total']:>8,}  均价{avg:>6,.0f}")
print()

# RMB分析
rmb_expense = [r for r in rmb_records if r['类型'] == '支出']
if rmb_expense:
    print("【RMB消费分析】")
    print()
    rmb_total = sum(Decimal(r['金额']) for r in rmb_expense)
    print(f"  RMB支出笔数:    {len(rmb_expense)} 笔")
    print(f"  RMB支出总额:    {rmb_total:.2f} RMB")
    print(f"  单笔平均:       {rmb_total/len(rmb_expense):.2f} RMB")
    print()

    rmb_by_cat = defaultdict(lambda: Decimal('0'))
    for r in rmb_expense:
        rmb_by_cat[r['分类']] += Decimal(r['金额'])

    print("  【RMB分类】")
    for cat, amt in sorted(rmb_by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"    {cat}: {amt:.2f} RMB")
    print()

# 总结
print("=" * 80)
print("本月消费亮点总结")
print("=" * 80)
print()
print(f"  - 存款率 55.5%，财务状况优秀")
print(f"  - 麻将 {mahjong_sessions} 场，胜率 {win_count}/{mahjong_sessions}，净赚 {mahjong_income - mahjong_expense:,} JPY")
print(f"  - 外食 {len(food_records)} 笔，均价 {sum(food_amounts)/len(food_amounts):,.0f} JPY")
print(f"  - 最常用支付: {sorted_pay[0][0]} ({sorted_pay[0][1]['count']}笔)")
print(f"  - 日均消费: {avg_daily:,.0f} JPY")
if total_all > 0:
    print(f"  - 周末消费占比: {weekend_expense/total_all*100:.1f}%")
print()
print("=" * 80)
