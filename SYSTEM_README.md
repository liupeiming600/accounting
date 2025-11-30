# 个人财务管理系统

## 系统概述

本系统用于管理个人财务，包括：
- 日常收支记录
- 账户余额追踪
- 信用卡管理
- 転売项目
- POI活动(积分返点)追踪
- 库存管理

---

## 核心概念

### 交易类型

| 类型 | 从账户 | 到账户 | 说明 |
|------|--------|--------|------|
| 消费 | 有 | 空 | 日常支出 |
| 收入 | 空 | 有 | 工资、麻将收入等 |
| 转换 | 有 | 有 | 余额A → 余额B（如充值Apple Account）|
| 转账 | 有 | 有 | 还信用卡、账户间转账 |
| 仕入 | 有 | 空 | 余额 → 库存（购买商品用于转卖）|
| 販売 | 空 | 有 | 库存 → 余额（出售商品）|
| 返点 | 空 | 有 | POI返点到账 |

### 数据流向

```
账户余额 ──仕入──► 库存 ──販売──► 账户余额
    │                              ▲
    │                              │
    └──转换──► 另一账户 ──────────┘
         │
         └── POI返点（附加效果）
```

### 关键原则

1. **转换 ≠ 仕入**：购买Apple Gift Card是「转换」（余额A→Apple余额），用Apple余额买iPhone才是「仕入」（余额→库存）
2. **POI是附加效果**：发生在转换或仕入时，独立追踪
3. **transactions.csv是单一数据源**：所有金钱流动都记录在这里

---

## 文件结构

```
accounting/
├── config/
│   ├── accounts.csv        # 账户定义
│   ├── categories.csv      # 消费分类
│   ├── credit_cards.csv    # 信用卡详情（含返点率）
│   └── reward_rates.csv    # 支付方式默认返点率
│
├── accounts/
│   ├── balances.csv        # 当前余额快照
│   └── transactions/       # 交易记录（按月份分文件）
│       ├── 2025-11.csv
│       ├── 2025-12.csv
│       └── ...
│
├── inventory/
│   ├── items.csv           # 库存商品
│   └── movements.csv       # 库存进出记录
│
├── poi/                    # POI活动（按活动开始月份分目录）
│   ├── 2025-11/
│   │   ├── events.csv      # 11月开始的事件
│   │   └── steps.csv       # 步骤明细
│   ├── 2025-12/
│   │   ├── events.csv      # 12月开始的事件
│   │   └── steps.csv       # 步骤明细
│   └── ...
│
├── business/
│   ├── README.md           # 业务系统说明
│   └── projects/
│       ├── index.csv       # 项目列表
│       └── T202511A/
│           └── summary.csv # 项目汇总
│
├── 2025/
│   ├── 06.csv ~ 11.csv     # 月度日常消费记录
│   └── ...
│
└── SYSTEM_README.md        # 本文档
```

---

## 账户体系

### 现金 & 人民币
| 账户ID | 名称 | 币种 |
|--------|------|------|
| CASH_JPY | 现金 | JPY |
| WECHAT | 微信钱包 | RMB |
| ALIPAY | 支付宝 | RMB |
| HUABEI | 花呗 | RMB |

### 银行
| 账户ID | 名称 |
|--------|------|
| MITSUI_BANK | 三井住友银行 |
| MUFG_BANK | 三菱UFJ银行 |
| RAKUTEN_BANK | 乐天银行 |
| MIZUHO_BANK | みずほ银行 |

### 电子钱包
| 账户ID | 名称 |
|--------|------|
| SUICA | Suica |
| PAYPAY | PayPay |
| RAKUTEN_PAY | 乐天Pay（楽天キャッシュ）|
| JAL_PAY | JAL Pay |
| WAON | WAON |
| ANA_PAY | ANA Pay |
| AU_PAY | AU Pay |
| NANACO | nanaco |
| APPLE | Apple Account |
| PASELI | Paseli |

### 积分 & 里程
| 账户ID | 名称 |
|--------|------|
| AMAZON_POINT | Amazon积分 |
| RAKUTEN_POINT | 楽天ポイント |
| PAYPAY_POINT | PayPayポイント |
| JAL_MILES | JALマイル |
| ANA_MILES | ANAマイル |
| WAON_POINT | WAONポイント |
| PONTA_POINT | Pontaポイント |
| V_POINT | Vポイント |
| V_POINT_ANA | Vポイント(ANA移行可) |
| D_POINT | dポイント |
| JRE_POINT | JREポイント |
| NANACO_POINT | nanacoポイント |
| PASELI_POINT | Paseliポイント |

### 证券（分项记录）
| 账户ID | 名称 |
|--------|------|
| SBI_STOCK | SBI証券-国内株式 |
| SBI_FUND | SBI証券-投資信託 |
| SBI_CASH | SBI証券-預り金 |
| RAKUTEN_STOCK | 乐天証券-国内株式 |
| RAKUTEN_FUND | 乐天証券-投資信託 |
| RAKUTEN_CASH | 乐天証券-預り金 |
| RAKUTEN_FX | 乐天証券-FX証拠金 |
| RAKUTEN_CFD | 乐天証券-CFD |

---

## 信用卡

### 常用卡（13张）

| 简称 | 全名 | 締め日 | 引落日 |
|------|------|--------|--------|
| 三井NL | 三井住友ゴールドM NL | 月末 | 翌月26日 |
| 三井事业卡 | オーナーズM（NL） | 月末 | 翌月26日 |
| ANA Gold | ANAマスターゴールド | 15日 | 翌月10日 |
| Amazon MC | Amazon マスター | 月末 | 翌月26日 |
| Amex Gold | アメリカン・エキスプレス・ゴールド・プリファード・カード | 7日 | 当月26日 |
| Epos Card | エポスゴールドカード | 27日 | 翌月27日 |
| Saison GP | SAISON GOLD Premium | 10日 | 翌月4日 |
| Saison Amex | セゾンゴールド・アメリカン・エキスプレス・カード | 10日 | 翌月4日 |
| View Card | ビックカメラSuicaカード | 5日 | 翌月4日 |
| 乐天Visa | 楽天カード(Visa) | 月末 | 翌月27日 |
| 乐天Master | 楽天カード(Mastercard) | 月末 | 翌月27日 |
| PayPayカード | PayPayカード | 月末 | 翌月27日 |
| JCBカードW | JCBカードWL NL | 15日 | 翌月10日 |

**引落口座：全部为三井住友银行**

### 不常用卡（5张）
- Olive フレキシブルペイ
- DMM JCBカード
- JQ CARDセゾン
- シネマイレージカード セゾン
- セブンカード・プラス(JCB)

---

## POI活动系统

### 目录结构
POI活动按**活动开始月份**分目录管理：
```
poi/
├── 2025-11/
│   ├── events.csv    # 11月开始的活动
│   └── steps.csv     # 步骤明细
├── 2025-12/
│   ├── events.csv    # 12月开始的活动
│   └── steps.csv     # 步骤明细
└── ...
```

### 事件类型
- **充值**：充值获得返点（如便利店Apple Gift Card 10%）
- **消费**：消费达标获得返点（如Amazon黑五活动）
- **リボ**：リボ活（多步骤复杂活动）

### 事件状态
```
进行中 → 待返点 → 已返点
```

### 文件说明
- `events.csv`：事件主表
  - 包含：事件ID、名称、类型、渠道、URL、规则说明、预计返点等
- `steps.csv`：步骤明细
  - 包含：步骤描述、状态、关联交易ID

### 当前活动（2025-12-01）

#### 进行中
| 事件 | 类型 | 目标 | 进度 | 预计返点 |
|------|------|------|------|----------|
| JCB スマリボ | リボ | ¥300,000 | ¥138,001 (46%) | ¥30,000 |

#### 待返点
| 事件 | 预计返点 | 形式 | 预计时间 |
|------|----------|------|----------|
| Ministop Apple充值10% | ¥10,000 | Apple Gift Card | 12月下旬 |
| 7-11 Apple充值10% | ¥10,000 | Apple Gift Card | 12月下旬 |
| FamilyMart Apple充值10% | ¥4,000 | Apple Gift Card | 12月下旬 |
| Amazon黑五积分 | ¥10,000 | Amazon积分 | 12月 |
| Amazon Prime 5% | ¥5,000 | Amazon积分 | 12月 |
| 楽天ブックス3.5% | ¥5,249 | 楽天ポイント | 12月 |

---

## 転売项目系统

### 项目命名规则
- **P**开头：代购项目（Proxy）
- **T**开头：転売项目（Tenbai）
- 格式：`{类型}{年月}{序号}`

### 项目列表
| 项目ID | 名称 | 状态 |
|--------|------|------|
| P202509A | 击中萌四期方 | 完成（利润¥9,979 RMB，ROI 19.28%）|
| T202511A | iPhone転売+Switch+PS5 | 进行中 |

### 库存状态定义
- **待入荷**：商家还没货（入荷次第発送）
- **待收货**：已下单，配送中
- **待售**：已到手，可出售
- **已售**：已出售

### 当前库存（2025-11-30）
| 商品 | 成本 | 状态 |
|------|------|------|
| iPhone17 256GB (Amazon) | ¥129,800 | 待收货 |
| iPhone17 256GB (Apple) x3 | ¥389,400 | 待收货 |
| iPhone17 Pro Max 256GB | ¥194,800 | 待收货 |
| Switch OLED | ¥37,970 | 待收货 |
| PS5 Pro | ¥101,587 | 待入荷 |
| PSVR2 Horizon同梱版 | ¥48,373 | 待入荷 |

**库存总成本：¥901,930**

---

## 日常记账

### 输入格式（口语化）
```
11.30
3970 rpay 外食
460 suica 交通费
麻将 +8400
```

### 系统标准化
- 分类标准化：外食、交通费、便利店等
- 账户名称标准化：rpay → 乐天Pay
- 自动生成CSV记录

### 标准分类
| 分类 | 说明 | 关键词 |
|------|------|--------|
| 外食 | 餐饮 | 吃饭、外卖、咖啡 |
| 便利店 | 便利店消费 | 711、罗森、全家 |
| 交通费 | 交通 | 电车、Suica |
| 服饰 | 衣服 | 衣服、裤子 |
| 鞋子 | 鞋 | 鞋子 |
| 化妆品 | 护肤美妆 | 化妆品 |
| 日用品 | 生活用品 | 日用品、理发 |
| 买菜 | 食材 | 买菜、超市 |
| 娱乐 | 娱乐活动 | 电影、live、游戏 |
| 麻将 | 麻将 | 麻将（净额计算）|
| 房租 | 房租 | |
| 光热费 | 水电燃气 | 电费、水费 |
| 医疗 | 医疗 | 看病、药 |
| 订阅 | 订阅服务 | Claude、Netflix |

### AA分账处理
当有朋友分摊时，记录实际支付金额：
```
外食 1618 rpay (原3970-朋友A分摊112RMB)
```

---

## 账户余额快照（2025-12-01）

### 现金 & 人民币
| 账户 | 余额 |
|------|------|
| 现金 | ¥35,200 |
| 微信 | ¥3,208 RMB |
| 支付宝 | ¥19,509 RMB |
| 花呗 | -¥9,557 RMB |

### 银行
| 账户 | 余额 |
|------|------|
| 三井住友 | ¥116,649 |
| 三菱UFJ | ¥0 |
| 乐天 | ¥0 |

### 电子钱包
| 账户 | 余额 |
|------|------|
| Suica | ¥12,945 |
| PayPay | ¥923 |
| 乐天Pay | ¥75,237 |
| JAL Pay | ¥80,000 |
| WAON | ¥4,523 |
| ANA Pay | ¥21,299 |
| AU Pay | ¥0 |
| nanaco | ¥0 |
| Apple | ¥25,400 |
| Paseli | ¥4,514 |

### 积分 & 里程
| 账户 | 余额 |
|------|------|
| Amazon | 12,453 pt |
| 楽天 | 160 pt |
| PayPay | 14,478 pt |
| WAON | 0 pt |
| Ponta | 19 pt |
| V Point | 258 pt |
| V Point(ANA) | 1,155 pt |
| d Point | 238 pt |
| JRE | 4,203 pt |
| nanaco | 8,750 pt |
| Paseli | 4,268 pt |
| JAL | 7,538 マイル |
| ANA | 39,242 マイル |

### 证券
| 账户 | 余额 |
|------|------|
| SBI-国内株式 | ¥308,871 |
| SBI-投資信託 | ¥214,089 |
| SBI-預り金 | ¥7,502 |
| 乐天-国内株式 | ¥37,900 |
| 乐天-投資信託 | ¥169,850 |
| 乐天-預り金 | ¥212 |
| 乐天-FX | ¥185,930 |
| 乐天-CFD | ¥1,046,991 |

---

## 操作指南

### 添加日常消费
1. 口语化输入给Claude
2. Claude标准化后写入`2025/MM.csv`

### 添加転売交易
1. **转换**（充值）：记录到`accounts/transactions/YYYY-MM.csv`（类型=转换）
2. **仕入**（进货）：
   - 记录到`accounts/transactions/YYYY-MM.csv`（类型=仕入）
   - 添加到`inventory/items.csv`
   - 添加到`inventory/movements.csv`
3. **販売**（出货）：
   - 记录到`accounts/transactions/YYYY-MM.csv`（类型=販売）
   - 更新`inventory/items.csv`状态
   - 添加到`inventory/movements.csv`

### 添加POI事件
1. 在对应月份目录创建/更新：`poi/YYYY-MM/events.csv`（含URL、规则说明）
2. 添加步骤：`poi/YYYY-MM/steps.csv`（关联交易ID）
3. 返点到账时：
   - 更新事件状态
   - 添加返点交易到`accounts/transactions/YYYY-MM.csv`

### 更新账户余额
直接编辑`accounts/balances.csv`，更新日期

---

*最后更新：2025-12-01*
