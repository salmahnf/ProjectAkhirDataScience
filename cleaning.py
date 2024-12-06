import pandas as pd
from datetime import datetime, timedelta

# Load file Excel
file_path = 'rumah.xlsx'  # Ganti dengan path yang sesuai
df = pd.read_excel(file_path)

# 1. Hapus baris yang memiliki nilai kosong di salah satu kolom
df = df.dropna()

# 2. Hapus data yang duplikat di semua kolom
df = df.drop_duplicates()

# 3. Menghapus data yang memiliki karakter '-' di kolom 'price'
df = df[df['price'].str.contains('-', na=False) == False]

# 4. Menangani kolom 'price', mengonversinya ke dalam satuan rupiah
def convert_price(price):
    # Menghapus prefix 'Rp' dan spasi
    price = str(price).replace('Rp', '').replace(' ', '')
    
    # Tangani koma sebagai desimal (jika ada)
    price = price.replace(',', '.')
    
    # Jika harga mengandung 'Jt', kalikan dengan 1 juta
    if 'Jt' in price:
        return float(price.replace('Jt', '').strip()) * 1000000
    # Jika harga mengandung 'M', kalikan dengan 1 milyar
    elif 'M' in price:
        return float(price.replace('M', '').strip()) * 1000000000
    # Jika harga dalam format biasa (tanpa satuan)
    try:
        return float(price)
    except ValueError:
        return None  # Jika gagal mengonversi, kembalikan None
    
# Fungsi untuk memproses kolom `date`
def process_date(date_str):
    if isinstance(date_str, str) and "hari" in date_str:
        # Ekstrak jumlah hari
        jumlah_hari = int(date_str.split()[1])
        # Hitung tanggal
        tanggal_diperbarui = datetime.now() - timedelta(days=jumlah_hari)
    else:
        # Gunakan tanggal saat ini jika tidak mengandung "hari"
        tanggal_diperbarui = datetime.now()
    return tanggal_diperbarui.strftime('%Y-%m-%d')

# Mengonversi harga ke dalam satuan rupiah yang sesuai
df['price'] = df['price'].apply(convert_price)

# Terapkan fungsi ke kolom `date`
df['date'] = df['date'].apply(process_date)

# 5. Membersihkan kolom 'luas_tanah', 'luas_bangunan', dan 'kamar_tidur'
def clean_size(value):
    # Menghapus karakter yang tidak diperlukan (misalnya 'LT', 'LB', 'm²', 'KT', dll.)
    value = str(value).replace('LT', '').replace('LB', '').replace('m²', '').replace('KT', '').strip()
    return ''.join(filter(str.isdigit, value))  # Hanya mengambil angka

# Memisahkan kolom "loc" menjadi "kecamatan" dan "kota"
df[['kecamatan', 'kota']] = df['loc'].str.split(',', expand=True)

# Membersihkan data dengan menghapus spasi berlebih
df['kecamatan'] = df['kecamatan'].str.strip()
df['kota'] = df['kota'].str.strip()

# Mengaplikasikan fungsi clean_size pada kolom yang relevan
df['luas_tanah'] = df['luas_tanah'].apply(clean_size).astype(float)
df['luas_bangunan'] = df['luas_bangunan'].apply(clean_size).astype(float)
df['kamar_tidur'] = df['kamar_tidur'].apply(clean_size).astype(float)

# 6. Membagi kolom 'price' dengan 1000000 untuk hasil akhirnya (miliaran ke juta)
df['price'] = df['price'] / 1000000

# Menghapus kolom "loc"
df.drop(columns=['loc'], inplace=True)

# Menyimpan file hasil cleaning ke Excel
output_file = 'rumah_cleaned.xlsx'  # Ganti dengan path yang diinginkan
df.to_excel(output_file, index=False)

print(f"Data cleaning selesai, hasil disimpan di: {output_file}")
