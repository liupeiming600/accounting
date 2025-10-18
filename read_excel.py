import pandas as pd
import sys

try:
    df = pd.read_excel(r'C:\Users\liu\Desktop\主账本_Liu.xlsx')
    print("列名:", df.columns.tolist())
    print("\n前10行数据:")
    print(df.head(10))
    print("\n数据形状:", df.shape)
except Exception as e:
    print(f"错误: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
