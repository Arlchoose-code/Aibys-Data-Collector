import os
from tqdm import tqdm

def audit_semua_txt(folder_path="data", max_lines_per_file=None):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    if not txt_files:
        print("❌ Tidak ada file .txt di folder ini!")
        return

    print(f"📂 Ditemukan {len(txt_files)} file .txt")
    print("="*60)

    total_lines_global = 0
    total_non_ascii_global = 0

    for file_name in txt_files:
        file_path = os.path.join(folder_path, file_name)
        print(f"\n[*] Auditing: {file_name}")

        non_ascii_count = 0
        total_lines = 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in tqdm(f, desc=f"Scanning {file_name}", leave=False):
                total_lines += 1

                if not all(ord(c) < 128 for c in line):
                    non_ascii_count += 1
                    if non_ascii_count <= 5:
                        print(f"\n[!] Non-ASCII di {file_name} baris {total_lines}:")
                        print(f"    {line.strip()[:120]}...")

                if max_lines_per_file and total_lines >= max_lines_per_file:
                    break

        print(f"   ├─ Total baris     : {total_lines:,}")
        print(f"   └─ Non-ASCII baris : {non_ascii_count:,}")

        total_lines_global += total_lines
        total_non_ascii_global += non_ascii_count

    print("\n" + "="*60)
    print("📊 HASIL AUDIT GLOBAL")
    print("="*60)
    print(f"Total Baris Di-scan : {total_lines_global:,}")
    print(f"Total Non-ASCII     : {total_non_ascii_global:,}")
    print("="*60)

    if total_non_ascii_global == 0:
        print("✅ SEMUA FILE BERSIH ASCII.")
    else:
        persen = (total_non_ascii_global / total_lines_global) * 100
        print(f"⚠️  Masih ada {persen:.4f}% baris mengandung non-ASCII.")

if __name__ == "__main__":
    # max_lines_per_file=None → scan full
    # max_lines_per_file=5_000_000 → batasi biar cepat
    audit_semua_txt("data", max_lines_per_file=None)
