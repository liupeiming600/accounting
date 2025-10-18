# Accounting 个人记账

项目用于按月记录与管理个人收支数据，并在需要时汇总生成总账与月度统计。

结构
- `2025/MM.csv` 月度标准化数据文件，例如 `2025/10.csv`。
- `2025/MM/inbox.md` 月度收件箱，用于临时记录未清洗/未归档流水。
- `notes/rules.md` 记账规则与约定。
- `ledger.csv` 总账（所有月份合并后，可按需生成）。
- `ARCHIVE.md` 清理说明与历史记录摘要（不保留冗余脚本的代码，仅保留信息）。
 - `tools/` 脚本工具（CSV 为主的流水线）：
   - `merge_ledger.py` 合并 `2025/*.csv` → `ledger.csv`（排序、去重、校验）。
   - `summarize_month.py` 生成 `summary_by_*.csv`（分类/账户/币种）。
   - `add_record.py` 追加单条记录到对应月份 CSV。
   - `ensure_bom.py` 统一 BOM 编码。

工作流
1. 将零散流水先记到对应月份的 `inbox.md`。
2. 整理并清洗为标准化行，写入 `2025/MM.csv`（UTF-8 含 BOM）。
3. 运行 `python tools/summarize_month.py 2025/10.csv` 生成 `summary_by_*.csv`。
4. 需要总账时，运行 `python tools/merge_ledger.py` 合并为 `ledger.csv`。

示例命令
- 追加一条记录：
  `python tools/add_record.py --date 2025-10-08 --type 支出 --category 外食 --amount 520 --currency JPY --account Amex Gold --merchant  --note 午餐`
- 生成 10 月汇总（写入 `2025/10/summary_by_*.csv`）：
  `python tools/summarize_month.py 2025/10.csv`
- 合并总账：
  `python tools/merge_ledger.py`

数据格式（CSV）
- 列顺序：`日期, 类型, 分类, 金额, 币种, 账户, 商户, 备注`
- 示例：`2025-10-01, 支出, 外食, 1100, JPY, 现金, , `

编码约定
- CSV：UTF-8 with BOM（`utf-8-sig`）。
- Markdown/代码：UTF-8（无 BOM）。
- Windows 控制台建议设置：`$OutputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)` 以避免显示乱码。

规则与约定
- 详见 `notes/rules.md`。
