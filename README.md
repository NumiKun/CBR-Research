# CBR Research

Repositori ini berisi kode, dataset, dan eksperimen terkait penelitian (research) yang menggunakan metode *Case-Based Reasoning (CBR)* atau penelitian CBR lainnya.

## Struktur Direktori

Berikut adalah penjelasan mengenai struktur direktori pada repositori ini:

- **`Dataset/`**: Berisi dataset yang digunakan untuk eksperimen. Dataset utama yang di-track pada Git adalah:
  - `dataset.xlsx`
  - `dataset_augmented.xlsx`
  *(File dataset lainnya dalam folder ini diabaikan oleh Git sesuai dengan konfigurasi `.gitignore`)*
- **`Paper Sumber/`**: Berisi makalah (paper), jurnal, atau referensi literatur yang menjadi acuan penelitian. *(Seluruh file di dalam folder ini tidak di-track oleh Git)*
- **`Program/`**: Berisi kode sumber, script, dan Jupyter Notebook penelitian.
  - `CBR_Research_Clean.ipynb`: Notebook utama yang berisi proses eksperimen, pemodelan, atau analisis data.
  - `augmentasi_random_deletion.py`: Script Python yang digunakan untuk melakukan augmentasi data (teknik *random deletion*).

## Cara Menjalankan

1. Pastikan dependensi Python seperti `pandas`, `numpy`, `scikit-learn`, `jupyter`, dan library relevan lainnya telah terinstal.
2. Jalankan script augmentasi data jika membutuhkan dataset yang telah di-augmentasi:
   ```bash
   cd Program
   python augmentasi_random_deletion.py
   ```
3. Buka dan jalankan seluruh sel (cell) di dalam `CBR_Research_Clean.ipynb` menggunakan Jupyter Notebook atau Jupyter Lab untuk melihat analisis dan hasil riset.

## Lisensi

Silakan sesuaikan lisensi dan batasan penggunaan untuk repositori ini.
