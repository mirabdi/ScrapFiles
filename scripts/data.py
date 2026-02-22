import pandas as pd
from io import StringIO

# Raw data input
data = """
date,count,sum,purchase,avg_cheque
2025-07-25,154/341,119858.23/443584.44,77844.98/277618.96,778.30/1300.83
2025-07-26,115/323,103978.23/498432.59,64665.33/309460.62,904.16/1543.13
2025-07-27,124/327,98445.50/551629.84,61277.71/344375.22,793.92/1686.94
2025-07-28,150/364,124113.13/573523.94,76994.41/350936.16,827.42/1575.62
2025-07-29,156/365,108631.47/551718.12,66806.45/344771.16,696.36/1511.56
2025-07-30,160/379,121429.00/623776.06,76267.26/382622.74,758.93/1645.85
2025-07-31,128/371,113643.80/692194.26,69739.68/422920.20,887.84/1865.75
2025-08-01,172/399,147897.41/801659.36,90669.44/485672.02,859.87/2009.17
2025-08-02,170/428,211437.10/970187.04,127442.61/594113.57,1243.75/2266.79
2025-08-03,115/320,94889.85/749329.57,58814.62/459359.44,825.13/2341.65
2025-08-04,190/487,142505.50/947319.05,84955.81/567650.66,750.03/1945.21
2025-08-05,168/452,150919.50/1090984.18,95710.89/665459.79,898.33/2413.68
"""

# Load data into a DataFrame
df = pd.read_csv(StringIO(data))

# Split columns and calculate percentages
df[['focus_count', 'total_count']] = df['count'].str.split('/', expand=True).astype(int)
df[['focus_sum', 'total_sum']] = df['sum'].str.split('/', expand=True).astype(float)
df[['focus_purchase', 'total_purchase']] = df['purchase'].str.split('/', expand=True).astype(float)
df[['focus_avg_cheque', 'total_avg_cheque']] = df['avg_cheque'].str.split('/', expand=True).astype(float)

# Calculate percentages
df['count_pct'] = (df['focus_count'] / df['total_count'] * 100).round(2)
df['sum_pct'] = (df['focus_sum'] / df['total_sum'] * 100).round(2)
df['purchase_pct'] = (df['focus_purchase'] / df['total_purchase'] * 100).round(2)
df['avg_cheque_pct'] = (df['focus_avg_cheque'] / df['total_avg_cheque'] * 100).round(2)

# Final format
final_df = df[['date', 'focus_count', 'total_count', 'count_pct',
               'focus_sum', 'total_sum', 'sum_pct',
               'focus_purchase', 'total_purchase', 'purchase_pct',
               'focus_avg_cheque', 'total_avg_cheque', 'avg_cheque_pct']]

final_df.to_excel("data.xlsx", index=False)