<div align="center">
  <h1>🧠 CBR Research Project</h1>
  <p><i>Penelitian Eksperimental menggunakan metode Case-Based Reasoning (CBR)</i></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Jupyter-Notebook-orange.svg" alt="Jupyter Notebook" />
    <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status Active" />
  </p>
</div>

---

## 📖 Tentang Proyek

Repositori ini berisi kode sumber, dataset, serta catatan eksperimen yang berfokus pada pendekatan **Case-Based Reasoning (CBR)** untuk klasifikasi diagnosis sakit kepala (ICD-X). Proyek ini bertujuan untuk menyediakan pipeline eksperimen yang bersih, terstruktur, dan terukur (membandingkan performa CBR Cosine Similarity dengan Support Vector Machine (SVM) serta evaluasi pada data testing eksternal).

---

## 📂 Struktur Direktori

Berikut adalah panduan struktur utama dalam repositori ini agar Anda mudah bernavigasi:

| Folder / Direktori | Deskripsi | Status Track Git |
| :--- | :--- | :--- |
| 📁 **`Dataset/`** | Menyimpan dataset utama dan data uji yang digunakan untuk eksperimen. | ⚠️ Terbatas (`dataset.xlsx` & `datatesting.xlsx`) |
| 📁 **`Paper Sumber/`** | Referensi, jurnal, & literatur utama pendukung riset. | ❌ *Diabaikan seluruhnya (Ignored)* |
| 📁 **`Program/`** | Source code, skrip analitik, & algoritma CBR. | ✅ *Dilacak sepenuhnya* |

### 📊 Dataset yang Digunakan
- 📄 **`dataset.xlsx`** — Dataset utama (kasus latih awal) yang berisi gejala dan diagnosis ICD-X.
- 📄 **`datatesting.xlsx`** — Dataset pengujian eksternal untuk mengevaluasi generalisasi model SVM dan CBR.
- 📄 **`dataset_augmented.xlsx`** *(Generated)* — Dataset hasil augmentasi *Random Deletion* (200 sampel) yang dipakai sebagai basis kasus CBR.
- 📊 **`hasil_testing.csv`** *(Generated)* — File ekspor detail prediksi SVM dan CBR terhadap `datatesting.xlsx`.

### 🛠️ File Utama (dalam `Program/`)
- 📓 **`CBR_Research_Clean.ipynb`** — *Jupyter Notebook utama yang mencakup seluruh alur eksperimen: EDA, encoding, augmentasi, pemodelan SVM & CBR, evaluasi LOO-CV, pengujian eksternal pada `datatesting.xlsx`, dan ekspor hasil ke `hasil_testing.csv`.*
- 🐍 **`augmentasi_random_deletion.py`** — *Skrip Python terdedikasi untuk teknik augmentasi data (Metode Random Deletion).*

---

## 🚀 Panduan Memulai (Getting Started)

Ikuti langkah-langkah di bawah ini untuk menjalankan program di komputer Anda:

### 1. Persiapan Dependensi
Pastikan Python telah terinstal, lalu pasang library pendukung yang diperlukan:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl jupyter
```

### 2. Eksekusi Augmentasi Data (Opsional)
Jika Anda ingin men-generate dataset augmentasi yang baru, jalankan skrip berikut:
```bash
cd Program
python augmentasi_random_deletion.py
```

### 3. Eksplorasi Eksperimen
Buka Jupyter Notebook untuk berinteraksi langsung dengan data dan melihat hasil pemodelan:
```bash
jupyter notebook Program/CBR_Research_Clean.ipynb
```
*(atau jalankan melalui VS Code / Jupyter Lab)*

---

## 📄 Lisensi

Silakan sesuaikan lisensi penggunaan proyek ini dengan kebutuhan riset atau publikasi Anda.

<div align="center">
  <br>
  <sub>Dibuat dengan ❤️ untuk kemajuan penelitian.</sub>
</div>
