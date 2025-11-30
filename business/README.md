# 业务活动管理系统

## 概述

本系统用于管理业务活动，核心是**交易记录**和**库存管理**。

## 核心概念

### 基本操作类型

| 操作 | 从账户 | 到账户 | 说明 |
|------|--------|--------|------|
| 消费 | 有 | 空 | 钱花掉了（日常开销）|
| 收入 | 空 | 有 | 钱进来了（工资等）|
| 转换 | 有 | 有 | 余额A→余额B（充值等）|
| 转账 | 有 | 有 | 还信用卡等 |
| 仕入 | 有 | 空 | 余额→库存（进货）|
| 販売 | 空 | 有 | 库存→余额（出货）|
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

## 文件结构

```
accounting/
├── accounts/
│   ├── transactions.csv    # 【核心】所有交易记录
│   └── balances.csv        # 账户余额快照
│
├── inventory/
│   ├── items.csv           # 库存商品
│   └── movements.csv       # 库存进出记录
│
├── poi/
│   ├── events.csv          # POI事件主表
│   └── steps.csv           # 事件步骤明细
│
└── business/projects/
    ├── index.csv           # 项目列表
    └── T202511A/
        └── summary.csv     # 项目汇总
```

## 关联关系

- `transactions.csv` 是单一数据源
- `movements.csv` 的每条记录关联一个交易ID
- `steps.csv` 的每个步骤可关联一个或多个交易ID
- 项目利润 = 筛选该项目的所有交易汇总

## 项目命名规则

- **P** 开头：代购项目（Proxy）
- **T** 开头：転売项目（Tenbai）

格式：`{类型}{年月}{序号}`

## 使用流程

### 仕入（进货）
1. 在 `transactions.csv` 添加仕入记录
2. 在 `inventory/items.csv` 添加商品
3. 在 `inventory/movements.csv` 添加入库记录

### 販売（出货）
1. 在 `transactions.csv` 添加販売记录
2. 更新 `inventory/items.csv` 状态为已售
3. 在 `inventory/movements.csv` 添加出库记录

### POI返点到账
1. 在 `transactions.csv` 添加返点记录
2. 更新 `poi/events.csv` 状态为完成
3. 更新 `poi/steps.csv` 相应步骤
