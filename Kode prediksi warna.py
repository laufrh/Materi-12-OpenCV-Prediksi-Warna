import cv2
import numpy as np
import csv
import time
from sklearn import svm
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Konfigurasi Kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# Membaca Database
FileDB = 'DatabaseWarna.txt' # Pastikan file ini tersedia dan formatnya benar
Database = pd.read_csv(FileDB, sep=",", header=0)
print("Database:\n", Database)

# X = Data (B, G, R), y = Target
X = Database[['B', 'G', 'R']]
y = Database['Target']

# Normaliasasi Data dan Pelatihan Model SVM
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Normalisasi data
clf = svm.SVC(kernel='linear')      # Gunakan karnel linear
clf.fit(X_scaled, y) # Pelatihan model

# Fungsi prediksi warna
def predict_color(b, g, r):
    color_scaled = scaler.transform([[b, g, r]])
    try:
      Prediction = clf.predict(color_scaled)[0] # Ambil hasil prediksi
      return Prediction
    except Exception as e:
        return "Tidak Teridentifikasi"

# Loop Kamera untuk Prediksi
while True:
    ret, frame = cap.read()
    if not ret:
        print("Tidak dapat membaca frame dari kamera.")
        break

    # Membalikkan frame jika kamera terbalik
    img = cv2.flip(frame, 1)

    # Ambil warna rata-rata dari area tertentu
    region = img[220:260, 330:340]  # Area yang dianalisis
    colorB = int(np.mean(region[:, :, 0]))
    colorG = int(np.mean(region[:, :, 1]))
    colorR = int(np.mean(region[:, :, 2]))

    # Prediksi warna
    prediction = predict_color(colorB, colorG, colorR)
    print(f"B: {colorB}, G: {colorG}, R: {colorR} => Prediksi: {prediction}")

    # Tampilkan hasil di jendela kamera
    cv2.putText(img, f"Prediksi: {prediction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Color Tracking", img)

    # Tombol keluar (ESC)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # Tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()

