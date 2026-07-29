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

Repositori ini berisi kode sumber, dataset, serta catatan eksperimen yang berfokus pada pendekatan **Case-Based Reasoning (CBR)**. Proyek ini bertujuan untuk menyediakan pipeline eksperimen yang bersih dan terstruktur.

---

## 📂 Struktur Direktori

Berikut adalah panduan struktur utama dalam repositori ini agar Anda mudah bernavigasi:

| Folder / Direktori | Deskripsi | Status Track Git |
| :--- | :--- | :--- |
| 📁 **`Dataset/`** | Menyimpan dataset yang digunakan untuk eksperimen. | Terbatas (`dataset.xlsx` & `dataset_augmented.xlsx`) |
| 📁 **`Paper Sumber/`** | Referensi, jurnal, & literatur utama pendukung riset. | ❌ *Diabaikan seluruhnya (Ignored)* |
| 📁 **`Program/`** | Source code, skrip analitik, & algoritma CBR. | ✅ *Dilacak sepenuhnya* |

### 🛠️ File Utama (dalam `Program/`)
- 📓 **`CBR_Research_Clean.ipynb`** — *Jupyter Notebook utama yang mencakup seluruh alur eksperimen, pemodelan, dan analisis hasil riset.*
- 🐍 **`augmentasi_random_deletion.py`** — *Skrip Python terdedikasi untuk teknik augmentasi data (Metode Random Deletion).*

---

## 🚀 Panduan Memulai (Getting Started)

Ikuti langkah-langkah di bawah ini untuk menjalankan program di komputer Anda:

### 1. Persiapan Dependensi
Pastikan Python telah terinstal, lalu pasang library pendukung yang diperlukan:
```bash
pip install pandas numpy scikit-learn jupyter
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
