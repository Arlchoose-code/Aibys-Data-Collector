import re, os, unicodedata
from datasets import load_dataset
from tqdm import tqdm

def clean_text(text):
    if not text: return None
    
    # 1. Anti-Null Hardened (SOLUSI: Biar gak kena spam 'Found null character')
    text = text.replace('\x00', '')
    
    # 2. Normalisasi Unicode (NFC) - Biar karakter unik stabil
    text = unicodedata.normalize('NFC', text)
    
    # 3. Hapus URL (Mengurangi noise)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 4. Anti-Control Char tapi SAFE-SYMBOL
    # Kita hapus karakter kontrol (0-31) tapi sisain \n dan \t
    # Karakter di atas 127 (∫, ∑, √) TETAP AMAN.
    text = "".join(ch for ch in text if ord(ch) >= 32 or ch in "\n\t")
    
    # 5. Rapiin Spasi (Tapi jangan buang baris baru)
    text = re.sub(r'[ \t]+', ' ', text).strip()
    
    # Hanya ambil dokumen yang punya substansi
    return text if len(text) >= 50 else None

def parse_limit(limit_str):
    if not limit_str: return 0
    l = str(limit_str).lower().strip()
    try:
        if 'm' in l: return int(float(l.replace('m', '')) * 1_000_000)
        if 'k' in l: return int(float(l.replace('k', '')) * 1_000)
        return int(l)
    except: return 0

def collect_v5_final():
    keranjang = []
    
    # Pastikan folder data ada di partisi laptop lu
    if not os.path.exists('data'):
        os.makedirs('data')

    while True:
        print("\n" + "="*50)
        print("🛒 AIBYS DATA COLLECTOR V5.2 (FINAL PRO)")
        print("   Status: Multi-File | Null-Safe | Symbol-Safe")
        print("="*50)
        print(f"Isi Keranjang: {len(keranjang)} Repo")
        print("1. Tambah Repo ke Daftar")
        print("2. 🔥 GAS DOWNLOAD (Sesuai Nama File Masing-Masing)")
        print("3. Keluar")
        
        choice = input("\nPilih (1/2/3): ")

        if choice == '1':
            repo = input("\n[+] Nama Repo HF: ")
            subset = input("[+] Nama Subset (kosongkan jika tidak ada): ") or None
            kolom = input("[+] Nama Kolom (pisah dengan koma, misal: text atau instruction,output): ")
            limit = input("[+] Limit data (misal: 1M, 500k, atau 0): ")
            
            # Setting nama file masing-masing
            def_name = repo.split('/')[-1].replace('.', '_') + ".txt"
            filename = input(f"[+] Simpan sebagai (Default: {def_name}): ") or def_name
            
            keranjang.append({
                'repo': repo, 
                'subset': subset, 
                'kolom': [k.strip() for k in kolom.split(',')], 
                'limit': parse_limit(limit),
                'filename': filename
            })
            print(f"✅ {repo} masuk list sebagai {filename}!")

        elif choice == '2':
            if not keranjang:
                print("❌ Keranjang lu masih kosong, Ril!"); continue
            
            print(f"\n🚀 Memulai proses download untuk {len(keranjang)} repo...")
            
            for item in keranjang:
                file_path = os.path.join('data', item['filename'])
                print(f"\n[*] Target: {item['repo']} -> {file_path}")
                
                try:
                    # Streaming biar RAM 32GB lu adem
                    ds = load_dataset(item['repo'], item['subset'], split='train', streaming=True)
                    count = 0
                    
                    # Mode 'w' (write) supaya bersih tiap kali run ulang
                    with open(file_path, 'w', encoding='utf-8') as f:
                        pbar = tqdm(desc=f"Processing {item['filename'][:15]}...", unit=" docs")
                        
                        for row in ds:
                            raw_texts = []
                            for k in item['kolom']:
                                val = row.get(k)
                                if val: raw_texts.append(str(val))
                            
                            content = " ".join(raw_texts)
                            cleaned = clean_text(content)
                            
                            if cleaned:
                                # Tambah separator endoftext biar model tau batas dokumen
                                f.write(cleaned + "\n<|endoftext|>\n")
                                count += 1
                                pbar.update(1)
                            
                            if item['limit'] > 0 and count >= item['limit']: 
                                break
                        pbar.close()
                    print(f"✅ Selesai! {count} data masuk ke {item['filename']}")
                    
                except Exception as e:
                    print(f"❌ Error di {item['repo']}: {e}")
            
            print(f"\n🏆 SEMUA BERES! Cek folder 'data' di laptop lu."); break

        elif choice == '3':
            break

if __name__ == "__main__":
    collect_v5_final()