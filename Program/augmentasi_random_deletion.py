"""
AUGMENTASI DATA - RANDOM SYMPTOM DELETION
==========================================
Pengganti dari CharSwapAugmenter (textattack).

Teknik: Menghapus gejala secara acak dari setiap baris kasus yang
        gejalanya dipisah oleh titik koma (';').

Alasan lebih cocok:
  1. Relevan secara klinis: mensimulasikan pasien yang tidak melaporkan
     semua gejalanya kepada dokter.
  2. TIDAK merusak kata-kata individual, sehingga kompatibel dengan
     TF-IDF berbasis kata (word-level TfidfVectorizer).
  3. Ringan: tidak butuh library eksternal (hanya modul `random` bawaan Python).

Cara pakai:
  - Copy-paste seluruh kode ini ke sel baru di notebook Anda,
    menggantikan sel augmentasi CharSwapAugmenter yang lama.
"""

# ============================================================
# CELL 1: Import Library (tidak perlu !pip install textattack lagi)
# ============================================================
import pandas as pd
import numpy as np
import random
import itertools
from collections import Counter


# ============================================================
# CELL 2: Augmentasi Data - Random Symptom Deletion
# ============================================================

random.seed(42)  # Untuk reproduktibilitas hasil


def random_symptom_deletion(baris_teks, deletion_prob=0.15):
    """
    Menghapus gejala secara acak dari teks yang dipisah titik koma.

    Args:
        baris_teks   : String gejala dipisah ';' (misal: "pusing;mual;demam")
        deletion_prob: Probabilitas setiap gejala dihapus (default 15%).
                       Minimal 1 gejala selalu dipertahankan.
    Returns:
        String gejala yang sudah dimodifikasi, dipisah ';'.

    Contoh:
        Input : "pusing;mual;demam 3 hari;alergi obat nihil"
        Output: "pusing;demam 3 hari;alergi obat nihil"  (1 gejala terhapus)
    """
    teks = str(baris_teks).strip()
    daftar_gejala = [g.strip() for g in teks.split(';') if g.strip()]

    # Jika hanya 1 gejala, langsung kembalikan tanpa modifikasi
    if len(daftar_gejala) <= 1:
        return teks

    # Filter: hanya simpan gejala yang TIDAK terpilih untuk dihapus
    hasil = [g for g in daftar_gejala if random.random() > deletion_prob]

    # Pastikan minimal 1 gejala tersisa (jangan sampai hasilnya kosong)
    if len(hasil) == 0:
        hasil = [random.choice(daftar_gejala)]

    return ";".join(hasil)


# ============================================================
# CELL 3: Load Dataset dan Jalankan Augmentasi
# ============================================================

print("Membaca file dataset.xlsx...")
df = pd.read_excel('/content/dataset.xlsx', header=1)
df.columns = df.columns.str.strip()

if 'normalized_semicolon' not in df.columns:
    print("\nERROR: Kolom 'normalized_semicolon' tidak ditemukan!")
else:
    JUMLAH_AUGMENTASI = 4
    list_df_augment = []

    print(f"\nMulai proses augmentasi Random Deletion sebanyak {JUMLAH_AUGMENTASI} kali...")
    print(f"Metode: Menghapus gejala secara acak (probabilitas 15% per gejala)")

    for i in range(JUMLAH_AUGMENTASI):
        df_temp = df.copy()

        # Terapkan random deletion pada kolom normalized_semicolon
        df_temp['normalized_semicolon'] = df_temp['normalized_semicolon'].apply(
            lambda x: random_symptom_deletion(x, deletion_prob=0.15)
        )
        df_temp['sumber_data'] = f'RandomDeletion Augment ke-{i+1}'

        list_df_augment.append(df_temp)

    df['sumber_data'] = 'Data Asli'

    df_final = pd.concat([df] + list_df_augment, ignore_index=True)

    nama_file_baru = "/content/dataset_augmented.xlsx"
    df_final.to_excel(nama_file_baru, index=False)

    # Tampilkan contoh hasil augmentasi (3 baris pertama)
    print("\n--- Contoh Hasil Augmentasi (3 Baris Pertama) ---")
    for idx in range(min(3, len(df))):
        print(f"\nBaris {idx+1} - Data Asli:")
        print(f"  {df.iloc[idx]['normalized_semicolon']}")
        for aug_num, df_aug in enumerate(list_df_augment[:2]):
            print(f"  Augmentasi {aug_num+1}: {df_aug.iloc[idx]['normalized_semicolon']}")

    print("\n" + "="*40)
    print("PROSES SELESAI!")
    print(f"Jumlah data awal     : {len(df)} baris")
    print(f"Jumlah data sekarang : {len(df_final)} baris")
    print(f"Silakan cek file {nama_file_baru} di folder Colab.")


# ============================================================
# CATATAN PENTING: Perbaikan Data Leakage
# ============================================================
# Untuk evaluasi model yang valid, lakukan train/test split pada
# data ASLI terlebih dahulu, BARU augmentasi hanya pada data latih.
#
# Contoh pipeline yang benar:
#
#   from sklearn.model_selection import train_test_split
#
#   # 1. Split data asli (40 baris) sebelum augmentasi
#   X_train_raw, X_test, y_train_raw, y_test = train_test_split(
#       df['normalized_semicolon'], df['icd_x'],
#       test_size=0.2, random_state=42, stratify=df['icd_x']
#   )
#
#   # 2. Augmentasi hanya pada X_train_raw
#   train_augmented_rows = []
#   for i in range(JUMLAH_AUGMENTASI):
#       X_aug = X_train_raw.apply(
#           lambda x: random_symptom_deletion(x, deletion_prob=0.15)
#       )
#       y_aug = y_train_raw.copy()
#       train_augmented_rows.append(
#           pd.DataFrame({'normalized_semicolon': X_aug, 'icd_x': y_aug})
#       )
#
#   df_train_original = pd.DataFrame({
#       'normalized_semicolon': X_train_raw,
#       'icd_x': y_train_raw
#   })
#   df_train_final = pd.concat([df_train_original] + train_augmented_rows,
#                               ignore_index=True)
#
#   X_train = df_train_final['normalized_semicolon']
#   y_train = df_train_final['icd_x']
#   # X_test dan y_test tetap dari data asli (bebas augmentasi)
