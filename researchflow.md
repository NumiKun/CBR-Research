# 🔬 Alur Penelitian — CBR Research Project

> **File Implementasi:** `Program/research_implementation.ipynb`
> **Topik:** Klasifikasi Diagnosis Sakit Kepala Menggunakan Case-Based Reasoning (CBR) dan Support Vector Machine (SVM)
> **Kode ICD-X:** G44.0 (Cluster Headache) dan G44.2 (Tension-Type Headache)

---

## 📌 Ringkasan Alur Penelitian

```
Dataset Asli (40 kasus)
        │
        ▼
[Langkah 1-4] Import Library, Konfigurasi Path, Load & Eksplorasi Data (EDA)
        │
        ▼
[Langkah 5-6] Pembangunan Kamus Kode Kasus & Encoding Fitur (One-Hot)
        │
        ▼
[Langkah 7]   Augmentasi Data → Random Deletion (200 kasus)
        │
        ├──────────────────────┬──────────────────────────────┐
        ▼                      ▼                              ▼
[Langkah 8]           [Langkah 9]                   [Langkah 11-14]
SVM (Data Aug.)       SVM (Data Asli / Baseline)    CBR (Data Aug., LOO-CV)
        │                      │                              │
        └──────────────────────┴──────────────────────────────┘
                                │
                                ▼
                     [Langkah 10 & 15]
                     Perbandingan SVM vs CBR (Internal)
                                │
                                ▼
                     [Langkah 16] Fase RETAIN
                     Menyimpan Kasus Baru ke Basis Kasus
                                │
                                ▼
                     Data Testing Eksternal (datatesting.xlsx)
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              [Langkah 18]           [Langkah 19]
              Testing SVM            Testing CBR
                    │                       │
                    └───────────┬───────────┘
                                ▼
                     [Langkah 20]
                     Perbandingan Akhir + Ekspor hasil_testing.csv
```

---

## 📋 Penjelasan Setiap Langkah

### Langkah 1 — Import Library

**Tujuan:** Memuat semua pustaka Python yang dibutuhkan.

| Library | Kegunaan |
|:--|:--|
| `pandas`, `numpy` | Manipulasi dan komputasi data |
| `matplotlib`, `seaborn` | Visualisasi grafik dan confusion matrix |
| `sklearn` | TF-IDF Vectorizer, SVM, LabelEncoder, metrik evaluasi |
| `scipy.sparse` | Operasi pada matriks sparse hasil TF-IDF |
| `random`, `itertools`, `Counter` | Augmentasi data dan analisis distribusi |

---

### Langkah 2 — Konfigurasi Path Dataset

**Tujuan:** Mendefinisikan path ke setiap file dataset secara dinamis dan terstandar.

**Variabel Path yang Didefinisikan:**
- `PATH_DATASET_UTAMA` → `Dataset/dataset.xlsx`
- `PATH_DATASET_AUGMENTED` → `Dataset/dataset_augmented.xlsx`
- `PATH_HASIL_TESTING` → `Dataset/hasil_testing.csv`

> Pendekatan dinamis memastikan notebook berjalan di komputer mana pun tanpa perubahan path manual.

---

### Langkah 3 — Load Dataset

**Tujuan:** Membaca dataset utama dari file Excel.

**Detail Teknis:**
- File: `dataset.xlsx`
- Header berada di **baris ke-2** (`header=1` pada `pd.read_excel`)
- Total: **40 baris** × 7 kolom
- Kolom kunci: `icd_x`, `normalized_semicolon`, `case_codes`

**Format kolom `normalized_semicolon`:**
Teks gejala pasien yang sudah dinormalisasi, dipisah oleh tanda titik koma (`;`).
Contoh: `"pusing;mual;nyeri kepala berdenyut;tidak nafsu makan"`

---

### Langkah 4 — Eksplorasi Data (EDA)

**Tujuan:** Memahami karakteristik dan kualitas data sebelum pemodelan.

**Analisis yang Dilakukan:**

1. **Missing Values** — Memastikan tidak ada nilai kosong di kolom kunci
2. **Statistik Deskriptif** — Ringkasan statistik kolom numerik
3. **Tampilan Kolom Kunci** — Inspeksi visual `icd_x`, `normalized_semicolon`, `case_codes`
4. **Distribusi Label ICD-X:**

| Kode ICD-X | Nama Diagnosis | Jumlah Kasus |
|:--:|:--|:--:|
| **G44.0** | Cluster Headache (Sakit Kepala Klaster) | 20 |
| **G44.2** | Tension-Type Headache (Sakit Kepala Tegang) | 20 |

> Dataset bersifat **balanced** (seimbang) antara dua kelas.

---

### Langkah 5 — Pembangunan Kamus Kode Kasus ↔ Gejala

**Tujuan:** Membangun representasi semantik hubungan antara gejala dan kode kasus medis.

**Dua kamus yang dibangun:**

1. **`symptom_to_case_codes`**: Dari setiap gejala → kode kasus apa saja yang terkait (beserta frekuensi kemunculan)
2. **`case_code_to_symptoms`**: Dari setiap kode kasus → gejala apa saja yang paling sering muncul

**Cara Kerja:**
```
Iterasi setiap baris dataset
  → parsing kolom 'normalized_semicolon' (split by ';')
  → parsing kolom 'case_codes' (split by ',')
  → menggunakan Counter untuk menghitung frekuensi korelasi
```

> Kamus ini adalah fondasi representasi kasus dalam sistem CBR.

---

### Langkah 6 — Encoding Fitur (One-Hot Encoding Kode Kasus)

**Tujuan:** Mengubah kolom `case_codes` (multi-label, dipisah koma) menjadi matriks biner.

**Proses:**
- Kumpulkan semua kode kasus unik dari seluruh dataset
- Setiap kode kasus menjadi satu kolom biner: `1` = kode ada, `0` = kode tidak ada
- Hasilnya: Matriks `(40 × N_kode_kasus_unik)` yang bersifat multi-hot

---

### Langkah 7 — Augmentasi Data (Random Deletion)

**Tujuan:** Memperbanyak data latih dari 40 menjadi 200 sampel.

**Teknik:** **Random Deletion** — menghapus sebagian gejala secara acak per kasus.

**Parameter Augmentasi:**

| Parameter | Nilai |
|:--|:--|
| Probabilitas penghapusan per gejala | **15%** (`deletion_prob=0.15`) |
| Jumlah putaran augmentasi | **4× (4 kali)** |
| Total data akhir | **200 baris** (40 asli + 4×40 augmentasi) |
| Minimal gejala dipertahankan | **1 gejala** |
| Random seed | `42` (reproducible) |

**Algoritma `random_symptom_deletion`:**
```
Input : teks gejala dipisah ';'
Proses: Untuk setiap gejala,
          - Hasilkan angka acak 0–1
          - Jika angka > 0.15 → gejala dipertahankan
          - Jika angka ≤ 0.15 → gejala dihapus
          - Jika semua terhapus → paksa pertahankan 1 gejala acak
Output: teks gejala hasil augmentasi
```

**Output:** File `dataset_augmented.xlsx` dengan kolom tambahan `sumber_data` yang menandai apakah baris merupakan data asli atau hasil augmentasi ke berapa.

---

### Langkah 8 — Pemodelan SVM (Data Augmented)

**Tujuan:** Melatih model SVM menggunakan data hasil augmentasi (200 sampel) sebagai model utama.

**Pipeline:**
```
Data Augmented (200 sampel)
  → Fitur: TF-IDF dari 'normalized_semicolon' (max_features=5000)
  → Label: icd_x (diencoding ke angka dengan LabelEncoder)
  → Split: 80% train (160) / 20% test (40)
  → Model: SVC(kernel='linear', random_state=42)
```

**Evaluasi:**
- Accuracy, F1-Score (weighted), Precision (weighted), Recall (weighted)
- Confusion Matrix
- Top-10 fitur TF-IDF berdasarkan koefisien SVM linear

**Objek yang Disimpan untuk Testing Eksternal:**
- `svm_augmented` — model SVM terlatih
- `tfidf_vectorizer` — vectorizer yang di-fit dari data augmented
- `label_encoder` — encoder label icd_x

---

### Langkah 9 — Pemodelan SVM (Data Asli / Baseline)

**Tujuan:** Melatih SVM identik namun hanya dengan **40 data asli** sebagai perbandingan sebelum augmentasi.

**Pipeline:** Sama dengan Langkah 8, namun menggunakan `dataset.xlsx` (40 baris).

**Split:** 80%/20% → 32 data latih / 8 data uji.

---

### Langkah 10 — Perbandingan SVM: Sebelum vs Sesudah Augmentasi

**Tujuan:** Mengukur dampak augmentasi data terhadap performa SVM.

**Metrik yang Dibandingkan:** Accuracy, F1-Score, Precision, Recall

**Visualisasi:** Bar chart side-by-side (Data Asli vs Data Augmented).

---

### Langkah 11 — Representasi Basis Kasus CBR (Data Augmented)

**Tujuan:** Membangun matriks TF-IDF dari **200 kasus augmented** sebagai "memori" sistem CBR.

**Detail Vectorizer CBR:**
```python
TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
# Menggunakan unigram + bigram untuk representasi lebih kaya
```

**Output:** `case_base_matrix` (matriks sparse TF-IDF 200 × N_fitur).

**Threshold Cosine Similarity:** `THRESHOLD_SIMILARITY = 0.70`

---

### Langkah 12 — Fungsi Inti CBR

**Tujuan:** Mendefinisikan tiga fungsi utama yang mengimplementasikan siklus 4R CBR.

#### `cbr_retrieve()` — Fase RETRIEVE
```
Input : query gejala baru (teks dipisah ';')
Proses:
  1. Transform query ke vektor TF-IDF
  2. Hitung cosine similarity dengan semua 200 kasus di basis kasus
  3. Filter: ambil kasus dengan similarity >= threshold (0.70)
  4. Urutkan descending, ambil top_k=5 teratas
Output: DataFrame kasus mirip + nilai similarity masing-masing
```

#### `cbr_reuse()` — Fase REUSE
```
Input : DataFrame kasus mirip dari Retrieve
Proses: Weighted Majority Voting
  - Setiap kasus memberi "suara" untuk label icd_x-nya
  - Bobot suara = nilai cosine similarity kasus tersebut
  - Label dengan total bobot tertinggi dipilih sebagai prediksi
  - Confidence = bobot label terpilih / total bobot semua kasus
Output: (predicted_label, confidence_score)
        predicted_label = None jika tidak ada kasus mirip
```

#### `cbr_predict()` — Retrieve + Reuse
```
Menggabungkan cbr_retrieve() dan cbr_reuse() menjadi satu fungsi prediksi.
Output dict: {
  'prediksi'   : label icd_x atau None,
  'confidence' : float 0.0–1.0,
  'kasus_mirip': DataFrame kasus yang ditemukan,
  'ada_kasus'  : bool (True jika ada kasus >= threshold)
}
```

---

### Langkah 13 — Demo Query Kasus Baru

**Tujuan:** Demonstrasi penggunaan nyata sistem CBR dengan satu query contoh.

**Contoh Query:** `"demam 3 hari;pusing;bab lembek;perut mual nihil;muntah nihil;alergi obat nihil"`

**Output yang Ditampilkan:**
- Kasus-kasus mirip yang ditemukan (fase Retrieve)
- Prediksi diagnosis + nilai confidence (fase Reuse)
- Keterangan kode ICD-X yang diprediksi

---

### Langkah 14 — Evaluasi CBR — Leave-One-Out Cross-Validation (LOO-CV)

**Tujuan:** Mengevaluasi performa CBR secara valid tanpa *data leakage* pada dataset kecil.

**Prosedur LOO-CV (200 iterasi):**
```
Untuk setiap kasus ke-i dari 200 kasus augmented:
  1. Pisahkan kasus ke-i sebagai "query uji"
  2. Gunakan sisa 199 kasus sebagai basis kasus sementara
  3. Bangun matriks TF-IDF dari 199 kasus (tanpa re-fit vectorizer)
  4. Jalankan cbr_predict() pada query ke-i
  5. Catat hasil: BENAR / SALAH / TIDAK_TERJAWAB
```

**Status Prediksi:**

| Status | Kondisi |
|:--|:--|
| **BENAR** | `prediksi == label_asli` |
| **SALAH** | `prediksi != label_asli` (ada jawaban tapi salah) |
| **TIDAK_TERJAWAB** | Tidak ada kasus dengan similarity >= 0.70 |

**Metrik yang Dihitung:**
- **Coverage** = kasus terjawab / total kasus
- **Accuracy Overall** = prediksi benar / total kasus
- **Accuracy Conditional** = prediksi benar / kasus terjawab saja
- Weighted F1-Score, Precision, Recall (dihitung pada kasus terjawab)
- Rata-rata confidence dan rata-rata jumlah kasus yang ditemukan per query

**Visualisasi:**
- Histogram distribusi max cosine similarity per kasus (LOO-CV)
- Pie chart coverage (terjawab vs tidak terjawab)
- Confusion matrix (pada kasus terjawab)

---

### Langkah 15 — Perbandingan CBR vs SVM (Internal)

**Tujuan:** Membandingkan performa CBR (LOO-CV pada data augmented) dengan kedua model SVM.

**Tabel Perbandingan:**

| Metode | Data | Evaluasi |
|:--|:--|:--|
| SVM — Data Asli | 40 sampel (80/20 split) | Accuracy, F1, Precision, Recall |
| SVM — Data Augmented | 200 sampel (80/20 split) | Accuracy, F1, Precision, Recall |
| CBR — Overall | 200 sampel LOO-CV | Accuracy Overall, F1, Precision, Recall |
| CBR — Conditional | Hanya kasus terjawab | Accuracy Conditional, F1, Precision, Recall |

**Visualisasi:** Bar chart 3-kolom side-by-side (SVM Asli, SVM Augmented, CBR Augmented).

---

### Langkah 16 — Fase RETAIN

**Tujuan:** Menambahkan kasus baru yang sudah divalidasi dokter ke basis kasus agar sistem CBR terus berkembang secara inkremental.

**Fungsi `cbr_retain()`:**
```
Input : df_case_base (basis kasus saat ini)
        new_case_text (teks gejala baru dipisah ';')
        true_label    (label diagnosis yang divalidasi dokter)
        vectorizer    (TF-IDF vectorizer yang sudah di-fit)
Proses:
  1. Buat baris baru DataFrame dengan kolom kunci
  2. Gabungkan baris baru ke df_case_base (pd.concat)
  3. Transform ulang seluruh basis kasus ke matriks TF-IDF (tanpa re-fit)
Output: (df_case_base_updated, case_matrix_updated)
```

**Demo Verifikasi:** Setelah RETAIN, sistem diuji dengan query serupa untuk membuktikan kasus yang baru disimpan sudah ikut dipertimbangkan dalam pencarian similarity.

---

### Langkah 17 — Load Dataset Testing Eksternal

**Tujuan:** Membaca `datatesting.xlsx` sebagai data uji **eksternal** — kasus yang sama sekali belum pernah dilihat selama training, augmentasi, maupun LOO-CV.

**Detail Dataset Testing:**

| Aspek | Nilai |
|:--|:--|
| File | `datatesting.xlsx` |
| Posisi header | Baris pertama (`header=0`) |
| Jumlah kasus | **25 baris** |
| Distribusi G44.0 | 9 kasus |
| Distribusi G44.2 | 16 kasus |

---

### Langkah 18 — Testing dengan Model SVM

**Tujuan:** Mengevaluasi generalisasi SVM pada 25 kasus testing yang belum pernah dilihat model.

**Proses (tanpa retraining):**
```
df_test['normalized_semicolon']
  → tfidf_vectorizer.transform()   ← vectorizer dari Langkah 8
  → svm_augmented.predict()        ← model dari Langkah 8
  → label_encoder.inverse_transform()
  → bandingkan dengan y_true_ext → BENAR / SALAH
```

**Output:**
- Tabel prediksi SVM per kasus testing
- Metrik evaluasi: Accuracy, F1-Score, Precision, Recall
- Classification Report per kelas
- Confusion Matrix

---

### Langkah 19 — Testing dengan Metode CBR

**Tujuan:** Mengevaluasi CBR pada 25 kasus testing menggunakan **seluruh 200 basis kasus augmented** (tidak perlu LOO karena data testing sudah sepenuhnya eksternal dan tidak tumpang tindih dengan basis kasus).

**Proses:**
```
Untuk setiap kasus di df_test (25 kasus):
  → cbr_predict(
        query_text      = gejala kasus testing,
        case_base_tfidf = case_base_matrix (200 kasus),
        df_cases        = df_cbr,
        vectorizer      = cbr_vectorizer,
        threshold       = 0.70,
        top_k           = 5
    )
  → Catat: prediksi, confidence, best_sim, n_retrieved
  → Tentukan status: BENAR / SALAH / TIDAK_TERJAWAB
```

**Output Tambahan:**
- Detail kasus yang **TIDAK TERJAWAB** (max sim < 0.70) beserta nilai `best_sim` tertinggi yang bisa dicapai
- Metrik: Coverage, Accuracy Overall, Accuracy Conditional
- Confusion matrix (hanya kasus terjawab)

> **Catatan:** Pada data testing eksternal, performa CBR cenderung rendah karena tingginya perbedaan kosakata (out-of-vocabulary rate ~63%) antara data training dan testing.

---

### Langkah 20 — Ekspor Hasil Testing ke CSV

**Tujuan:** Menyimpan seluruh detail prediksi SVM dan CBR pada data testing dalam satu file CSV terstruktur untuk keperluan arsip dan analisis lanjutan.

**Kolom `hasil_testing.csv`:**

| Kolom | Tipe | Deskripsi |
|:--|:--|:--|
| `No` | int | Nomor urut kasus testing (1–25) |
| `label_asli` | str | Label diagnosis ICD-X sebenarnya |
| `gejala` | str | Teks gejala dari kolom `normalized_semicolon` |
| `prediksi_svm` | str | Prediksi model SVM (`G44.0` / `G44.2`) |
| `status_svm` | str | `BENAR` / `SALAH` |
| `prediksi_cbr` | str | Prediksi CBR (`G44.0`, `G44.2`, atau `TIDAK_TERJAWAB`) |
| `confidence_cbr` | float | Skor keyakinan CBR (0.00 – 1.00) |
| `best_sim_cbr` | float | Nilai cosine similarity tertinggi yang ditemukan |
| `n_retrieved_cbr` | int | Jumlah kasus yang lolos threshold similarity |
| `status_cbr` | str | `BENAR` / `SALAH` / `TIDAK_TERJAWAB` |

**Output:** `Dataset/hasil_testing.csv`

---

## 🔑 Keputusan Desain Kunci

| Keputusan | Nilai / Pilihan | Alasan |
|:--|:--|:--|
| Metode augmentasi | Random Deletion (15%) | Sederhana, tetap mempertahankan semantik gejala asli |
| Jumlah augmentasi | 4× (total 200 kasus) | Memperkaya variasi tanpa terlalu banyak noise |
| Representasi CBR | TF-IDF unigram + bigram | Menangkap frasa gejala 2 kata (contoh: "nyeri kepala") |
| Fungsi kemiripan | Cosine Similarity | Invariant terhadap panjang teks, sesuai untuk TF-IDF |
| Threshold CBR | 0.70 | Trade-off antara precision tinggi dan coverage yang cukup |
| Strategi voting | Weighted Majority Vote | Kasus lebih mirip mendapat bobot lebih besar |
| Evaluasi internal | LOO-CV | Dataset kecil (200 sampel), LOO lebih valid dari k-fold |

---

## 📊 Ringkasan Metrik Evaluasi

### Evaluasi Internal (Langkah 8–15)

| Model | Data Latih | Data Uji | Metode Evaluasi |
|:--|:--|:--|:--|
| SVM (Baseline) | 32 (80%) | 8 (20%) | Train/test split |
| SVM (Augmented) | 160 (80%) | 40 (20%) | Train/test split |
| CBR | 199 (per iterasi LOO) | 1 (per iterasi LOO) | LOO-CV (200 iterasi) |

### Evaluasi Eksternal (Langkah 17–20)

| Model | Basis / Model | Data Uji | Evaluasi |
|:--|:--|:--|:--|
| SVM (Augmented) | Dilatih dari 200 kasus | 25 kasus baru | Accuracy, F1, Precision, Recall |
| CBR | 200 kasus augmented | 25 kasus baru | Coverage, Accuracy Overall/Conditional, F1, Precision, Recall |

---

*Dokumen ini dihasilkan dari analisis `Program/research_implementation.ipynb`.*
