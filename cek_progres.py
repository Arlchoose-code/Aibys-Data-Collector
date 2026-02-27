import os
import time

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def hitung_semua_txt(folder_path="."):
    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} tidak ditemukan!")
        return

    # Ambil semua file .txt
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    if not txt_files:
        print("❌ Tidak ada file .txt di folder ini!")
        return

    print(f"📂 Ditemukan {len(txt_files)} file .txt")
    print("=" * 60)

    total_baris_global = 0
    total_karakter_global = 0
    total_size_global = 0

    start_time = time.time()

    for file_name in txt_files:
        file_path = os.path.join(folder_path, file_name)
        file_size = os.path.getsize(file_path)
        total_size_global += file_size

        print(f"\n[*] Menghitung: {file_name} ({format_size(file_size)})")

        total_baris = 0
        total_karakter = 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore', buffering=1024*64) as f:
            for line in f:
                total_baris += 1
                total_karakter += len(line)

        print(f"   ├─ {total_baris:,} baris")
        print(f"   └─ {total_karakter:,} karakter")

        total_baris_global += total_baris
        total_karakter_global += total_karakter

    # --- Estimasi Token ---
    rasio_indo_32k = 3.7
    estimasi_token = total_karakter_global / rasio_indo_32k
    durasi = time.time() - start_time

    print("\n" + "=" * 60)
    print("           📊 LAPORAN AKHIR TOTAL DATASET")
    print("=" * 60)
    print(f"📦 Total Ukuran     : {format_size(total_size_global)}")
    print(f"📝 Total Baris      : {total_baris_global:,}")
    print(f"🔡 Total Karakter   : {total_karakter_global:,}")
    print("-" * 60)
    print(f"🚀 ESTIMASI TOKEN   : {estimasi_token / 1e9:.3f} Billion")
    print(f"⏱️ Waktu Scan       : {durasi:.2f} detik")
    print("=" * 60)

    if estimasi_token >= 10e9:
        print("🎉 STATUS: SIAP TRAINING 10B+ TOKEN!")
    else:
        print("💡 STATUS: Masih bisa ditambah kalau mau 10B+.")
    print("=" * 60)


if __name__ == "__main__":
    # Ganti "." kalau file ada di folder lain
    hitung_semua_txt("data")
