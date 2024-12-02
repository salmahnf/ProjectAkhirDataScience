import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Memuat data yang sudah dibersihkan
cleaned_data = pd.read_csv("data_rumah_cleaned.csv", sep=';')

# Melakukan One-Hot Encoding pada kolom kategorikal (contohnya 'type', 'sertifikasi', 'region', 'area')
cleaned_data = pd.get_dummies(cleaned_data, columns=['type', 'sertifikasi', 'region', 'area'], drop_first=True)

# Menyiapkan fitur (X) dan target (y)
X = cleaned_data.drop(columns=['price'])  # Features (kecuali kolom target 'price')
y = cleaned_data['price']  # Target variable (price)

# Split data menjadi training dan testing sets (80% untuk training dan 20% untuk testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membuat model Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Melatih model
model.fit(X_train, y_train)

# Memprediksi dan menghitung metrik evaluasi
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Menampilkan hasil evaluasi
print(f'Mean Absolute Error (MAE): {mae}')
print(f'Mean Squared Error (MSE): {mse}')
print(f'R² Score: {r2}')
