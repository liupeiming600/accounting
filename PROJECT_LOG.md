# Project Log / 项目记录

日期：2025-10-18

本文件用于压缩（compact）会话历史，沉淀关键决策、当前快照与下一步待办，便于在 Codex 持续协作时保持上下文轻量且可追溯。

## 变更摘要（本次）
- 清理临时/一次性脚本：`convert.py`, `convert.ps1`, `fix_encoding.py`,
  `import_data.py`, `import_data2.py`, `process_remaining_months.py`,
  `read_excel.py`, `read_excel2.py`。
- 修复与重写文档为正常中文并统一编码：`README.md`, `notes/rules.md`, `2025/10/inbox.md`。
- 新增 `ARCHIVE.md` 记录删除清单与说明。
- 统一编码约定：CSV 使用 UTF-8 BOM；Markdown/代码使用 UTF-8；建议在 Windows 控制台设置合适的输出编码以避免显示乱码。

## 现状快照
- 目录核心文件：
  - `README.md`（项目说明、结构、流程、编码）
  - `notes/rules.md`（记账规则与约定）
  - `ARCHIVE.md`（归档与删除说明）
  - `PROJECT_LOG.md`（会话/决策压缩记录）
  - 数据：`2025/06.csv`, `2025/07.csv`, `2025/08.csv`, `2025/09.csv`, `2025/10.csv`
  - 收件箱：`2025/10/inbox.md`
  - 总账：`ledger.csv`（仅表头，待合并）

## 编码策略（决定）
- CSV：UTF-8 with BOM（`utf-8-sig`），表头固定：`日期, 类型, 分类, 金额, 币种, 账户, 商户, 备注`。
- Markdown/代码：UTF-8（无 BOM）。
- Windows 控制台建议：
  `$OutputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)`

## 待办（优先顺序）
1) 合并总账（已添加脚本 `tools/merge_ledger.py`）
   - 合并 `2025/*.csv` → `ledger.csv`；统一表头、按日期排序、去重。
   - 转账类目（账户之间的划转）做中性化处理（在汇总统计中不计入）。
   - 保持 `ledger.csv` 为 UTF-8 BOM。

2) 月度汇总（已添加脚本 `tools/summarize_month.py`）
   - 输入 `2025/MM.csv`，输出 `summary_by_category.csv`、`summary_by_account.csv`、`summary_by_currency.csv`。

3) 追加记录（已添加脚本 `tools/add_record.py`）
   - 以命令行参数追加单条记录到对应月份 CSV，自动标准化/校验/去重。

4) 统一 BOM（已添加脚本 `tools/ensure_bom.py`）
   - 对现有 CSV 进行 BOM 统一。

5) 规范化映射（可选增强）
   - 在 `notes/rules.md` 或 `rules.json` 中维护账户/分类同义词归一映射（例如 Paypay→PayPay）。

6) 校验脚本（可选）
   - 校验列完整性、金额数值化、币种集合仅限 {JPY, RMB}、编码是否达标（CSV 为 BOM）。

## 备注
- 被删除脚本的功能均为当时一次性尝试，数据已写入对应 CSV；如需正式化处理，将以通用脚本替代。
- 如需恢复任何具体尝试的细节，请参见 `ARCHIVE.md` 的说明或在此文件补充记录。
