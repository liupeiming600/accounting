# AGENTS 指南（项目根生效）

本文件为协作型编码助手（Codex CLI）在本仓库的工作约定与启动清单。作用域为仓库根目录及其所有子目录。

## 启动清单（每次新会话）
- 快速浏览 `SYSTEM_README.md`、`README.md`、`PROJECT_LOG.md`、`notes/rules.md`，确认当前以 `accounts/transactions.csv` 为唯一资金流水。
- 了解周边模块：`inventory/`（库存）、`poi/`（积分返点）、`business/`（项目汇总）、`config/`（账户/分类/信用卡定义）。
- 历史口径：`2025/*.csv` 与 `ledger.csv` 属于旧版月度视图，处理前需强调其“历史/仅供参考”属性。
- 忽略耗时/无关目录：`.git/`、`.archive/`。

## 交互与输出
- 保持简洁直接：先说明预期动作，再分组展示结果。
- 涉及写入交易或库存/返点联动时，先给出“候选记录/字段预览”，确认后再落盘。
- 多步骤任务可用计划工具（update_plan）标记进度；单一步骤任务直接执行。

## 数据与编码约定
- 交易表字段顺序：`交易ID, 日期, 类型, 从账户, 到账户, 金额, 关联库存ID, 关联事件ID, 项目ID, 备注`（详见 `notes/rules.md`）。
- CSV 编码：UTF-8 with BOM（`utf-8-sig`）；Markdown/代码：UTF-8（无 BOM）。
- 账户/信用卡/分类 ID 以 `config/` 为准；币种由账户定义，转账/转换为中性流动，返点为独立收益。

## 记账与联动（优先级）
1) **标准入口**：默认写入 `accounts/transactions.csv`，必要时同步 `inventory/movements.csv`、`poi/steps.csv` 或项目 ID（如 `T202511A`）。
2) **历史月度文件**：如用户指定继续使用 `2025/MM.csv` 或旧版脚本，需说明其为“历史视图/双写”，避免与核心流水冲突。
3) **资产/余额**：更新余额请写 `accounts/balances.csv`，对账需引用交易表而非旧版月度 CSV。

## 常用任务与命令
- 追加交易（旧脚本仍存）：`py -3 tools/add_record.py ...` 仅针对 `2025/MM.csv`，使用前声明其“历史用途”。
- 月度汇总/合并：`tools/summarize_month.py`、`tools/merge_ledger.py` 仅作用于 2025 月度文件；不默认运行。
- BOM 统一：`py -3 tools/ensure_bom.py`（覆盖月度 CSV 与 ledger 等历史文件）。

## 注意事项
- 不做隐式默认：日期/币种/账户/项目/关联 ID 不明确时先确认；RMB 报销默认 `ALIPAY` 仅在用户同意的前提下使用。
- `.archive/` 为外部助手会话归档，不参与任何计算或汇总。
- 不在未获指示时操作“核心交易表 + 库存/返点联动”，也不自动运行旧版合并/汇总脚本。
