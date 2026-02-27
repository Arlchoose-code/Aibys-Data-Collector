import os
import random
import tempfile
import time
from tqdm import tqdm
import shutil

def shuffle_raksasa_aibys(input_file, output_file, num_chunks=200): # Tambah chunk biar per file lebih kecil
    start_time = time.time()
    print(f"[*] MEMULAI DISK-BASED SHUFFLE (File: {input_file})")
    print(f"[*] Target RAM Usage: Minimal")
    
    temp_dir = tempfile.mkdtemp()
    # Membuka banyak file sekaligus bisa kena limit OS, kita handle per grup kalau perlu
    # Tapi untuk 200 chunks biasanya Windows/Linux masih oke
    chunk_files = [open(os.path.join(temp_dir, f"chunk_{i}.txt"), 'w', encoding='utf-8', buffering=1024*1024) for i in range(num_chunks)]

    print(f"[*] Tahap 1: Distribusi Dokumen ke {num_chunks} Buckets...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            current_doc = []
            for line in f:
                line = line.replace('\0', '')
                current_doc.append(line)
                
                if "<|endoftext|>" in line:
                    target_chunk = random.randint(0, num_chunks - 1)
                    chunk_files[target_chunk].write("".join(current_doc))
                    current_doc = []
            
            # Sisa buffer jika ada
            if current_doc:
                doc_str = "".join(current_doc)
                if "<|endoftext|>" not in doc_str:
                    doc_str += "<|endoftext|>\n"
                chunk_files[random.randint(0, num_chunks - 1)].write(doc_str)

        # Tutup semua file chunk
        for cf in chunk_files:
            cf.close()

        print(f"[*] Tahap 2: Deep Shuffle per Bucket & Konsolidasi...")

        with open(output_file, 'w', encoding='utf-8', buffering=1024*1024) as f_out:
            # Kita acak urutan chunk yang akan diproses
            chunk_indices = list(range(num_chunks))
            random.shuffle(chunk_indices)

            for i in tqdm(chunk_indices, desc="Shuffling Buckets"):
                chunk_path = os.path.join(temp_dir, f"chunk_{i}.txt")
                
                if os.path.exists(chunk_path):
                    docs = []
                    # Membaca ulang per chunk untuk di-shuffle di memori 
                    # Karena sudah dibagi 200, tiap chunk cuma ~240MB (Aman di RAM 32GB)
                    with open(chunk_path, 'r', encoding='utf-8') as f_in:
                        this_doc = []
                        for line in f_in:
                            this_doc.append(line)
                            if "<|endoftext|>" in line:
                                docs.append("".join(this_doc))
                                this_doc = []
                    
                    random.shuffle(docs)
                    for d in docs:
                        f_out.write(d)
                    
                    # Bebaskan memori segera
                    del docs
                    os.remove(chunk_path)

        durasi = (time.time() - start_time) / 60
        print("\n" + "="*55)
        print(f"✅ BERHASIL! Dataset Aibys sudah di-shuffle secara disk-based.")
        print(f"📁 File Output : {output_file}")
        print(f"⏱️ Total Waktu  : {durasi:.2f} menit")
        print("="*55)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # Gunakan num_chunks lebih besar (misal 200-500) jika ingin RAM lebih irit lagi
    shuffle_raksasa_aibys("train.txt", "train_shuffled.txt", num_chunks=300)