# Assignment 2 - Code4Impact (UNI521)

## Deskripsi
Repository ini berisi implementasi integrasi **ESP32** dengan **Flask API** untuk mengumpulkan data sensor lingkungan yang terdiri dari:
- **Sensor DHT11** untuk membaca data **temperatur** dan **kelembapan**.
- **Gas Sensor MQ2** untuk membaca konsentrasi gas dalam bentuk persentase.

Data yang dikumpulkan oleh ESP32 dikirimkan ke **Flask API** melalui protokol HTTP POST dan disimpan ke dalam database **MongoDB**.

---

## Fitur Utama
1. **Koneksi WiFi ESP32**:
   - ESP32 secara otomatis terhubung ke jaringan WiFi menggunakan kredensial yang telah dikonfigurasi.

2. **Pengumpulan Data Sensor**:
   - Temperatur dan kelembapan dari **DHT11**.
   - Konsentrasi gas dari **MQ2**, dikalkulasi dalam bentuk persentase.

3. **Integrasi Flask API**:
   - Data sensor dikirim secara **real-time** ke endpoint Flask API.
   - Flask API menyimpan data ke dalam database **MongoDB** untuk kebutuhan analisis lebih lanjut.

4. **Format Data yang Dikirim**:
   Data dikirim dalam format JSON dengan parameter berikut:
   ```json
   {
       "temperature": <nilai_temperatur>,
       "humidity": <nilai_kelembapan>,
       "gas_value": <persentase_gas>,
       "timestamp": <waktu_pengukuran>
   }
