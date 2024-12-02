import pandas as pd

# Membaca file CSV
csv_file = 'rumah.csv'
df = pd.read_csv(csv_file)

# Menyimpan sebagai file Excel (.xlsx)
excel_file = 'rumah.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"File berhasil disimpan sebagai {excel_file}")
