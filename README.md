# 📦 Aibys Data Collector

Tools untuk mengumpulkan, membersihkan, dan mempersiapkan dataset teks Bahasa Indonesia untuk melatih LLM. Dikembangkan oleh **Syahril Haryono** sebagai bagian dari ekosistem Aibys.

> 💡 **Repo ini adalah langkah pertama sebelum pre-training — kumpulkan dan siapkan dataset kamu di sini, lalu lanjut ke [Indonesian LLM Starter](https://github.com/syhrlhyn834/Indonesian-LLM-Starter).**

---

## 🔗 Ekosistem Aibys

| Repo | Fungsi |
|---|---|
| 📦 **Aibys Data Collector** (repo ini) | Kumpulkan & siapkan dataset untuk training |
| 🏗️ [Indonesian LLM Starter](https://github.com/syhrlhyn834/Indonesian-LLM-Starter) | Pre-training LLM dari scratch |
| 🎯 [Indonesian LLM Fine-tune](https://github.com/syhrlhyn834/indonesian-llm-finetune) | Fine-tuning model hasil pre-training dengan LoRA |

**Alur lengkap:**
```
Aibys Data Collector    →    Indonesian LLM Starter    →    Indonesian LLM Fine-tune
(kumpul & siap data)         (pre-train model)               (fine-tune jadi assistant)
        ↓                            ↓                                  ↓
  train_shuffled.txt    →      aibys_final.pt           →        model siap chat
```

---

## 🎯 Untuk Apa Repo Ini?

Sebelum bisa melatih LLM, kamu butuh data teks dalam jumlah besar — idealnya **10 Miliar token ke atas**. Repo ini menyediakan tools untuk:

- 📥 **Download** dataset dari HuggingFace secara streaming (RAM-efficient)
- 🧹 **Bersihkan** teks dari noise, null character, URL, dan karakter aneh
- 🔀 **Shuffle** dataset raksasa secara disk-based tanpa meledakkan RAM
- 📊 **Audit** kualitas dan estimasi jumlah token
- 🤖 **Generate** data identitas AI untuk menanamkan kepribadian model

---

## 🗂️ Struktur Project

```
aibys-data-collector/
│
├── aibys_collector.py          # 📥  Download dataset dari HuggingFace
├── aibys_shuffler.py           # 🔀  Shuffle dataset besar secara disk-based
├── cek_progres.py              # 📊  Cek total ukuran, karakter & estimasi token
├── cek_ascii.py                # 🔍  Audit kebersihan data (non-ASCII checker)
├── buat_blueprint_identitas.py # 🤖  Generate data identitas & kepribadian AI
│
└── data/                       # Output dataset (tidak di-commit)
    ├── dataset1.txt
    ├── dataset2.txt
    └── ...
```

---

## ⚙️ Penjelasan Tiap Script

### `aibys_collector.py` — Downloader Dataset
Script interaktif untuk download dataset dari HuggingFace. Bisa tambah banyak repo ke "keranjang" sekaligus, lalu download semua dalam satu proses.

Fitur:
- **Streaming mode** — dataset sebesar apapun tidak akan meledakkan RAM
- **Multi-repo** — download banyak dataset sekaligus
- **Pembersihan otomatis** — hapus null character, URL, control character, normalisasi Unicode
- **Separator `<|endoftext|>`** — otomatis ditambah antar dokumen supaya model tau batas antar teks

```
🛒 AIBYS DATA COLLECTOR V5.2
1. Tambah Repo ke Daftar
2. 🔥 GAS DOWNLOAD
3. Keluar
```

### `aibys_shuffler.py` — Disk-Based Shuffler
Shuffle dataset yang sudah besar (puluhan GB) tanpa perlu load semua ke RAM.

Cara kerjanya:
1. **Distribusi** — bagi semua dokumen ke 200-300 bucket kecil secara random
2. **Deep shuffle** — shuffle dokumen di dalam setiap bucket
3. **Konsolidasi** — gabungkan semua bucket dengan urutan random

```python
# Default: 300 chunks, cocok untuk dataset 47GB+ di RAM 32GB
shuffle_raksasa_aibys("train.txt", "train_shuffled.txt", num_chunks=300)
```

### `cek_progres.py` — Progress Checker
Scan semua file `.txt` di folder `data/` dan tampilkan laporan lengkap:
- Total ukuran file
- Total baris & karakter
- **Estimasi token** (pakai rasio 3.7 karakter/token untuk Bahasa Indonesia)
- Status: apakah sudah cukup untuk training 10B+ token

```
📊 LAPORAN AKHIR TOTAL DATASET
📦 Total Ukuran     : 47.23 GB
🔡 Total Karakter   : 48,291,023,841
🚀 ESTIMASI TOKEN   : 13.051 Billion
🎉 STATUS: SIAP TRAINING 10B+ TOKEN!
```

### `cek_ascii.py` — ASCII Auditor
Audit semua file `.txt` dan cari baris yang mengandung karakter non-ASCII. Berguna untuk memastikan dataset bersih sebelum tokenisasi.

```
✅ SEMUA FILE BERSIH ASCII.
# atau
⚠️  Masih ada 0.0023% baris mengandung non-ASCII.
```

### `buat_blueprint_identitas.py` — Identity Data Generator
Generate **500.000 baris** data percakapan identitas dalam format formal/baku. Digunakan untuk "menanamkan" kepribadian dan identitas model supaya model tau siapa dirinya.

Format output:
```
User: Siapakah pencipta dari sistem kecerdasan buatan ini?
Assistant: Sistem Aibys ini diciptakan dan dikembangkan sepenuhnya oleh Syahril Haryono.
<|endoftext|>
```

---

## 🚀 Cara Pakai dari Awal

### Install
```bash
git clone https://github.com/syhrlhyn834/aibys-data-collector.git
cd aibys-data-collector
pip install datasets tqdm
```

### Step 1 — Download Dataset
```bash
python aibys_collector.py
```

Contoh input:
```
[+] Nama Repo HF     : wikipedia
[+] Nama Subset      : id
[+] Nama Kolom       : text
[+] Limit data       : 1M
[+] Simpan sebagai   : wikipedia_id.txt
```

Dataset Indo yang direkomendasikan:

| Repo HuggingFace | Subset | Kolom |
|---|---|---|
| `wikipedia` | `id` | `text` |
| `mc4` | `id` | `text` |
| `uonlp/CulturaX` | `id` | `text` |
| `cahya/all-indo-man-made-corpus` | - | `text` |
| `Xavier-Nuttall/indo-wiki` | - | `text` |

### Step 2 — Generate Data Identitas
```bash
python buat_blueprint_identitas.py
```
Output: `identitas_aibys_baku.txt` (500.000 baris)

Gabungkan ke dataset utama:
```bash
# Windows
type identitas_aibys_baku.txt >> data\train.txt

# Linux/Mac
cat identitas_aibys_baku.txt >> data/train.txt
```

### Step 3 — Cek Progress
```bash
python cek_progres.py
```

### Step 4 — Audit Kebersihan Data
```bash
python cek_ascii.py
```

### Step 5 — Shuffle Dataset
```bash
python aibys_shuffler.py
```
Output: `train_shuffled.txt` — siap dipakai untuk training!

### Step 6 — Lanjut ke Pre-training
Pindahkan hasil ke folder `data/` di [Indonesian LLM Starter](https://github.com/syhrlhyn834/Indonesian-LLM-Starter):
```bash
cp train_shuffled.txt ../Indonesian-LLM-Starter/data/train.txt
```

---

## 🔧 Konfigurasi Shuffler

Sesuaikan `num_chunks` di `aibys_shuffler.py` berdasarkan RAM:

| RAM | Dataset Size | `num_chunks` |
|---|---|---|
| 8GB | ~10GB | 100 |
| 16GB | ~25GB | 200 |
| 32GB | ~50GB | 300 |
| 64GB | ~100GB | 500 |

---

## 📦 Dependencies

```
datasets>=2.14.0
tqdm>=4.66.0
```

```bash
pip install datasets tqdm
```

---

## 👤 Author

**Syahril Haryono** — Developer independen asal Indonesia.

---

## 📄 License

Apache 2.0 — bebas digunakan, dimodifikasi, dan didistribusikan dengan atribusi.

---

*Langkah pertama membangun LLM kamu sendiri. Lanjut ke [Indonesian LLM Starter](https://github.com/syhrlhyn834/Indonesian-LLM-Starter) setelah dataset siap. 🚀*
