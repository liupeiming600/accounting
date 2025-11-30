# Archive Notes

为精简仓库、避免重复与乱码问题，已移除以下一次性/临时脚本。脚本功能均已在文档中保留说明，必要时可在将来用更通用的入口重写。

移除的文件与用途
- `convert.py`：批量将 CSV 重新写为 UTF-8 BOM。
- `convert.ps1`：PowerShell 版本的 UTF-8 BOM 批量转换脚本。
- `fix_encoding.py`：写入 2025/06.csv 的造数/编码修复尝试脚本。
- `import_data.py`：将硬编码的原始文本导入到 2025/06-09 的临时导入脚本（含大量示例数据）。
- `import_data2.py`：更小的导入示例脚本。
- `process_remaining_months.py`：7 月数据写入脚本（一次性）。
- `read_excel.py` / `read_excel2.py`：查看 Excel 列结构/样本数据的探查脚本。

当前保留内容
- 核心设计与数据：`SYSTEM_README.md`、`README.md`、`PROJECT_LOG.md`、`notes/rules.md`，以及唯一流水表 `accounts/transactions.csv`。
- 辅助模块：`config/`（账户/分类/信用卡）、`inventory/`（库存）、`poi/`（积分返点）、`business/`（项目）。
- 历史月度视图：`2025/*.csv`、`ledger.csv` 与 `2025/10/inbox.md`，仅供回溯或双写参考（均为 UTF-8 BOM）。

编码约定
- CSV：UTF-8 with BOM；Markdown/代码：UTF-8。
- 如需在 Windows 控制台避免乱码，可设置：
  `$OutputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)`

说明
- 被删除脚本均为一次性用途，数据本体已写入对应的 CSV 文件，不会影响现有账目。
- 若需要正式的导入/合并/汇总工具，建议新增通用脚本而非恢复这些临时脚本。
