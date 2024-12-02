import pandas as pd
import re

# Load dataset
file_path = r'C:\Users\Salma Hanifa\OneDrive\Dokumen\belajar python\datascience\projectAkhir\data_rumah.xlsx'
data = pd.ExcelFile(file_path)
df = data.parse('Sheet1')

# Membuat salinan dataset untuk proses pembersihan data
cleaned_data = df.copy()

# Membersihkan kolom 'price'
# Menghapus simbol mata uang, representasi teks, dan menangani rentang harga
def clean_price(price):
    # Jika terdapat rentang harga, ambil batas bawah dari rentang
    if '-' in price:
        price = price.split('-')[0]
    # Hapus simbol mata uang dan representasi teks
    price = re.sub(r'[^0-9,]', '', price)  # Hanya menyisakan angka dan koma
    price = price.replace(',', '')  # Hapus koma untuk konversi yang bersih
    return float(price)

cleaned_data['price'] = cleaned_data['price'].apply(clean_price)

# Membersihkan kolom 'kamar_tidur'
# Ekstrak nilai numerik dan konversi ke tipe float
cleaned_data['kamar_tidur'] = cleaned_data['kamar_tidur'].str.extract(r'(\d+)').astype(float)

# Membersihkan kolom 'luas_tanah' dan 'luas_bangunan'
# Mendefinisikan fungsi untuk membersihkan kolom-kolom tersebut
def clean_area_updated(area):
    # Hapus prefix (misalnya, "LT", "LB") dan satuan di akhir (misalnya, "m²")
    area = re.sub(r'[^0-9\-]', '', area)
    if '-' in area:
        # Jika terdapat rentang, ambil rata-rata
        values = area.split('-')
        area = (float(values[0]) + float(values[1])) / 2
    else:
        area = float(area) if area else None
    return area

cleaned_data['luas_tanah'] = cleaned_data['luas_tanah'].apply(clean_area_updated)
cleaned_data['luas_bangunan'] = cleaned_data['luas_bangunan'].apply(clean_area_updated)

# Membagi kolom 'loc' menjadi komponen detail: 'area' dan 'region'
cleaned_data[['area', 'region']] = cleaned_data['loc'].str.split(',', expand=True)

# Menghapus kolom asli 'loc'
cleaned_data = cleaned_data.drop(columns=['loc'])

# Menghapus baris di mana 'sertifikasi' bernilai "Tidak Tersedia"
cleaned_data = cleaned_data[cleaned_data['sertifikasi'] != "Tidak Tersedia"]

# Menyimpan data yang telah dibersihkan ke dalam format CSV
cleaned_data.to_csv("data_rumah_cleaned.csv", index=False, sep=';')

# save cleaned data directly to Excel
cleaned_data.to_excel("data_rumah_cleaned.xlsx", index=False)

print("Data cleaned and saved successfully as data_rumah_cleaned!")
