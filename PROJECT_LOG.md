# Project Log / 项目记录

日期：2025-11-30

本文件用于压缩会话历史，沉淀关键决策、当前快照与下一步待办，便于在 Codex 协作时保持上下文轻量且可追溯。

## 变更摘要（本次）
- 以 `SYSTEM_README.md` 为权威设计文档，重新梳理 README 及规则说明，明确单一数据源为 `accounts/transactions.csv`。
- 补充交易类型、目录结构、库存/POI/业务项目的关联关系，标注 2025 年月度 CSV 为历史/补充视图。

## 现状快照
- 核心设计：`SYSTEM_README.md`（账户体系、交易类型、库存/POI/项目现状与余额）。
- 数据与配置：
  - `config/`（账户/分类/信用卡定义）
  - `accounts/transactions.csv`（唯一资金流水表，含转卖/返点/转换等类型）
  - `accounts/balances.csv`（余额快照）
  - `inventory/items.csv`、`inventory/movements.csv`（库存与进出）
  - `poi/events.csv`、`poi/steps.csv`（积分返点）
  - `business/projects/`（项目索引与项目级汇总）
- 历史/补充数据：`2025/*.csv`（口语化日常消费记录），`tools/` 下旧版脚本用于月度流水处理。

## 编码策略（决定）
- CSV：UTF-8 with BOM（`utf-8-sig`）。
- Markdown/代码：UTF-8（无 BOM）。
- Windows 控制台建议：`$OutputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)`。

## 待办（优先顺序）
1) **统一数据入口**：为日常消费/收入构建直接写入 `accounts/transactions.csv` 的流程，并规划 2025 月度 CSV 的迁移或双写策略。
2) **库存与 POI 联动校验**：确保 `inventory/movements.csv`、`poi/steps.csv` 的关联交易 ID 与 `transactions.csv` 同步更新，避免漏挂或错挂。
3) **报表与对账**：基于交易表生成项目/账户/币种/类型维度的汇总视图，支持转卖项目利润与返点落地情况的可视化；必要时补充校验脚本覆盖交易字段合法性。

## 备注
- `.archive/` 为外部会话归档，不参与计算。
- 旧版月度脚本仍可用于 2025 数据，但需确认字段口径与核心流水一致后再运行。
