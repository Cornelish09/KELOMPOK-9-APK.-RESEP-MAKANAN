import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re
from collections import namedtuple

# ================== Tipe Bentukan ==================
Recipe = namedtuple("Recipe", ["judul", "bahan", "langkah", "waktu"])

# ================== Array Statis ==================
MAX_RECIPES = 40
recipes = [None] * MAX_RECIPES
num_recipes = 0

displayed_indices = []

# ================== Utilitas ==================

def normalize_title(s: str) -> str:
    """
    Hilangkan semua karakter non-alfanumerik dan ubah ke lowercase.
    Contoh:
      "$Tiwul Ketan!" -> "tiwulketan"
      "Tiwul Ketan 100 gram" -> "tiwulketan100gram"
    """
    return "".join(ch.lower() for ch in s if ch.isalnum())

def number_lines(text: str) -> str:
    """
    Menerima string multiline, hilangkan nomor awalan (jika ada),
    lalu kembalikan string dengan setiap baris diberi nomor urut:
    "1. baris1\n2. baris2\n..."
    """
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        no_number = re.sub(r'^\d+\.\s*', '', stripped)
        lines.append(no_number)
    return "\n".join(f"{i+1}. {lines[i]}" for i in range(len(lines)))

def levenshtein(a: str, b: str) -> int:
    """
    Hitung jarak Levenshtein (edit distance) antara string a dan b.
    """
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]
    for i in range(len_a + 1):
        dp[i][0] = i
    for j in range(len_b + 1):
        dp[0][j] = j

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # hapus
                dp[i][j - 1] + 1,      # sisip
                dp[i - 1][j - 1] + cost  # ganti
            )
    return dp[len_a][len_b]

# ================== Fungsi GUI ==================

def refresh_list(indices=None):
    """Refresh Listbox. Jika indices=None, tampilkan semua resep; jika ada indices, tampilkan sesuai."""
    listbox.delete(0, tk.END)
    displayed_indices.clear()
    if indices is None:
        for i in range(num_recipes):
            listbox.insert(tk.END, recipes[i].judul)
            displayed_indices.append(i)
    else:
        for i in indices:
            listbox.insert(tk.END, recipes[i].judul)
            displayed_indices.append(i)
    clear_form()

def clear_form():
    """Bersihkan semua field input di form kanan."""
    entry_title.delete(0, tk.END)
    text_bahan.delete("1.0", tk.END)
    text_langkah.delete("1.0", tk.END)
    entry_waktu.delete(0, tk.END)

def on_select(event):
    """Saat user memilih atau membatalkan seleksi di Listbox."""
    sel = listbox.curselection()
    if not sel:
        # Jika tidak ada yang terpilih, bersihkan form
        clear_form()
        return
    # Jika ada yang terpilih, tampilkan detailnya
    idx = displayed_indices[sel[0]]
    r = recipes[idx]
    entry_title.delete(0, tk.END)
    entry_title.insert(0, r.judul)
    text_bahan.delete("1.0", tk.END)
    text_bahan.insert(tk.END, r.bahan)
    text_langkah.delete("1.0", tk.END)
    text_langkah.insert(tk.END, r.langkah)
    entry_waktu.delete(0, tk.END)
    entry_waktu.insert(0, str(r.waktu))

def add_recipe():
    """Tambah resep baru ke array statis dengan validasi dan penomoran otomatis."""
    global num_recipes
    judul = entry_title.get().strip()
    bahan_raw = text_bahan.get("1.0", tk.END).strip()
    langkah_raw = text_langkah.get("1.0", tk.END).strip()
    waktu_str = entry_waktu.get().strip()

    if not judul:
        messagebox.showwarning("Peringatan", "Judul wajib diisi")
        return
    if not bahan_raw:
        messagebox.showwarning("Peringatan", "Bahan wajib diisi")
        return
    if not langkah_raw:
        messagebox.showwarning("Peringatan", "Langkah wajib diisi")
        return
    if not waktu_str.isdigit():
        messagebox.showwarning("Peringatan", "Waktu harus berupa angka")
        return
    if num_recipes >= MAX_RECIPES:
        messagebox.showwarning("Peringatan", f"Maksimal {MAX_RECIPES} resep")
        return

    norm_new = normalize_title(judul)
    for i in range(num_recipes):
        if normalize_title(recipes[i].judul) == norm_new:
            messagebox.showwarning("Peringatan", "Judul resep sudah ada")
            return

    bahan_numbered = number_lines(bahan_raw)
    langkah_numbered = number_lines(langkah_raw)
    waktu = int(waktu_str)

    recipes[num_recipes] = Recipe(judul, bahan_numbered, langkah_numbered, waktu)
    num_recipes += 1
    refresh_list()

def save_recipe():
    """Simpan perubahan pada resep terpilih."""
    global num_recipes
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Peringatan", "Pilih resep untuk disimpan")
        return
    idx = displayed_indices[sel[0]]

    judul = entry_title.get().strip()
    bahan_raw = text_bahan.get("1.0", tk.END).strip()
    langkah_raw = text_langkah.get("1.0", tk.END).strip()
    waktu_str = entry_waktu.get().strip()

    if not judul:
        messagebox.showwarning("Peringatan", "Judul wajib diisi")
        return
    if not bahan_raw:
        messagebox.showwarning("Peringatan", "Bahan wajib diisi")
        return
    if not langkah_raw:
        messagebox.showwarning("Peringatan", "Langkah wajib diisi")
        return
    if not waktu_str.isdigit():
        messagebox.showwarning("Peringatan", "Waktu harus berupa angka")
        return

    norm_new = normalize_title(judul)
    for i in range(num_recipes):
        if i != idx and normalize_title(recipes[i].judul) == norm_new:
            messagebox.showwarning("Peringatan", "Judul resep sudah ada")
            return

    bahan_numbered = number_lines(bahan_raw)
    langkah_numbered = number_lines(langkah_raw)
    waktu = int(waktu_str)

    recipes[idx] = Recipe(judul, bahan_numbered, langkah_numbered, waktu)
    refresh_list()

def delete_selected():
    """Hapus satu atau banyak resep terpilih dan sesuaikan array."""
    global num_recipes
    sels = listbox.curselection()
    if not sels:
        messagebox.showwarning("Peringatan", "Pilih resep untuk dihapus")
        return

    msg = "Yakin ingin menghapus resep yang dipilih?"
    if len(sels) == 1:
        msg = "Yakin ingin menghapus resep ini?"
    if not messagebox.askyesno("Konfirmasi", msg):
        return

    to_delete = {displayed_indices[i] for i in sels}
    kept = [recipes[i] for i in range(num_recipes) if i not in to_delete]
    new_count = len(kept)

    for i in range(new_count):
        recipes[i] = kept[i]
    for j in range(new_count, num_recipes):
        recipes[j] = None

    num_recipes = new_count
    refresh_list()

def delete_all():
    """Hapus semua resep (set array menjadi None dan reset counter)."""
    global num_recipes
    if num_recipes == 0:
        messagebox.showinfo("Info", "Tidak ada resep yang dapat dihapus")
        return
    if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua resep?"):
        for i in range(num_recipes):
            recipes[i] = None
        num_recipes = 0
        refresh_list()

def search_by_choice():
    """Cari resep berdasarkan nama atau bahan, dengan saran typo untuk nama."""
    q = entry_search.get().strip().lower()
    if not q:
        refresh_list()
        return

    found = []
    if var_search_type.get() == "nama":
        for i in range(num_recipes):
            if q in recipes[i].judul.lower():
                found.append(i)
        if found:
            refresh_list(found)
            return

        # cek typo
        q_proc = re.sub(r'\s+', '', q)
        best_title = None
        best_i = None
        best_dist = None
        for i in range(num_recipes):
            title_proc = re.sub(r'\s+', '', recipes[i].judul.lower())
            dist = levenshtein(q_proc, title_proc)
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_title = recipes[i].judul
                best_i = i

        if best_dist is not None and best_dist <= 2:
            yn = messagebox.askyesno("Mungkin Maksud", f"Mungkin maksud Anda: {best_title}?")
            if yn:
                refresh_list([best_i])
            else:
                messagebox.showinfo("Hasil Pencarian", "Nama resep tidak ditemukan")
                refresh_list([])
        else:
            messagebox.showinfo("Hasil Pencarian", "Nama resep tidak ditemukan")
            refresh_list([])

    else:
        for i in range(num_recipes):
            if q in recipes[i].bahan.lower():
                found.append(i)
        if not found:
            messagebox.showinfo("Hasil Pencarian", "Bahan resep tidak ditemukan")
            refresh_list([])
        else:
            refresh_list(found)

def search_by_time():
    """Filter dan tampilkan resep dengan waktu ≤ input."""
    q = entry_search_time.get().strip()
    if not q.isdigit():
        messagebox.showwarning("Peringatan", "Masukkan waktu (angka) yang valid")
        return
    max_waktu = int(q)

    filtered = [i for i in range(num_recipes) if recipes[i].waktu <= max_waktu]
    if not filtered:
        messagebox.showinfo("Hasil Pencarian", f"Tidak ada resep dengan waktu ≤ {max_waktu} menit")
        refresh_list([])
        return

    refresh_list(filtered)

def show_all_recipes():
    """Tampilkan seluruh resep; jika kosong, tampilkan pesan."""
    if num_recipes == 0:
        messagebox.showinfo("Info", "Resep masih kosong, tidak ada yang bisa ditampilkan")
        return
    refresh_list()

def sort_by_name(asc=True):
    """Urutkan berdasarkan nama (insertion sort pada indeks)."""
    indices = list(range(num_recipes))
    for j in range(1, len(indices)):
        key_idx = indices[j]
        key_name = recipes[key_idx].judul.lower()
        i = j - 1
        while i >= 0:
            comp_idx = indices[i]
            comp_name = recipes[comp_idx].judul.lower()
            if (asc and comp_name > key_name) or (not asc and comp_name < key_name):
                indices[i + 1] = indices[i]
                i -= 1
            else:
                break
        indices[i + 1] = key_idx
    refresh_list(indices)

def sort_by_time(asc=True):
    """Urutkan berdasarkan waktu (insertion sort pada array statis)."""
    for j in range(1, num_recipes):
        key_rec = recipes[j]
        key_time = key_rec.waktu
        i = j - 1
        while i >= 0 and ((asc and recipes[i].waktu > key_time) or (not asc and recipes[i].waktu < key_time)):
            recipes[i + 1] = recipes[i]
            i -= 1
        recipes[i + 1] = key_rec
    refresh_list()

def load_csv():
    """Impor file CSV, validasi header/isi, lalu masukkan ke array statis."""
    global num_recipes
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not path:
        return

    expected = ["judul", "bahan", "langkah", "waktu"]
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header or [c.strip().lower() for c in header] != expected:
                messagebox.showwarning("Peringatan", "Header CSV tidak sesuai. Harus: Judul,Bahan,Langkah,Waktu")
                return

            temp = []
            for row_num, row in enumerate(reader, start=2):
                if len(row) < 4:
                    messagebox.showwarning("Peringatan", f"Baris {row_num} kurang kolom")
                    return
                judul_c, bahan_c, langkah_c, time_c = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
                if not judul_c or not bahan_c or not langkah_c or not time_c.isdigit():
                    messagebox.showwarning("Peringatan", f"Data tidak valid di baris {row_num}")
                    return
                temp.append([judul_c, bahan_c, langkah_c, int(time_c)])

        slots = MAX_RECIPES - num_recipes
        if len(temp) > slots:
            messagebox.showwarning("Peringatan", f"Maksimal {MAX_RECIPES} resep")
            return

        existing = {normalize_title(recipes[i].judul) for i in range(num_recipes)}
        for rec in temp:
            if normalize_title(rec[0]) in existing:
                messagebox.showwarning("Peringatan", f"Judul '{rec[0]}' sudah ada")
                return

        for rec in temp:
            recipes[num_recipes] = Recipe(rec[0], number_lines(rec[1]), number_lines(rec[2]), rec[3])
            num_recipes += 1

        refresh_list()

    except Exception as e:
        messagebox.showerror("Error", f"Gagal memuat CSV:\n{e}")

def export_csv():
    """Ekspor seluruh data resep ke file CSV (dengan header)."""
    if num_recipes == 0:
        messagebox.showwarning("Peringatan", "Tidak ada resep untuk diekspor")
        return
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv"),("All files","*.*")])
    if not path:
        return
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Judul", "Bahan", "Langkah", "Waktu"])
            for i in range(num_recipes):
                r = recipes[i]
                writer.writerow([r.judul, r.bahan, r.langkah, r.waktu])
        messagebox.showinfo("Sukses", f"Berhasil mengekspor ke:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekspor CSV:\n{e}")

# ================== Inisialisasi GUI ==================

root = tk.Tk()
root.title("Aplikasi Resep Masakan")
root.configure(bg="#FAF0E6")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

# ---------- Frame Kiri ----------
frm_left = tk.Frame(root, bg="#FFEFD5", bd=2, relief="groove")
frm_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

for i in range(16):
    frm_left.rowconfigure(i, weight=0)
frm_left.rowconfigure(15, weight=1)
frm_left.columnconfigure(0, weight=1)

tk.Button(frm_left, text="Muat CSV", command=load_csv, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=0, column=0, sticky="ew", padx=5, pady=(10,2))
tk.Button(frm_left, text="Ekspor CSV", command=export_csv, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=1, column=0, sticky="ew", padx=5, pady=(0,10))

tk.Label(frm_left, text="Cari (Nama/Bahan):", bg="#FFEFD5").grid(row=2, column=0, sticky="w", padx=5)
entry_search = tk.Entry(frm_left, bg="#FFF8DC", fg="#333")
entry_search.grid(row=3, column=0, sticky="ew", padx=5, pady=(0,5))

var_search_type = tk.StringVar(value="nama")
frame_radio = tk.Frame(frm_left, bg="#FFEFD5")
frame_radio.grid(row=4, column=0, sticky="w", padx=5, pady=(0,5))
tk.Radiobutton(frame_radio, text="Nama", variable=var_search_type, value="nama", bg="#FFEFD5")\
    .grid(row=0, column=0, padx=(0,10))
tk.Radiobutton(frame_radio, text="Bahan", variable=var_search_type, value="bahan", bg="#FFEFD5")\
    .grid(row=0, column=1)

tk.Button(frm_left, text="Cari", command=search_by_choice, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=5, column=0, sticky="ew", padx=5, pady=(0,10))
tk.Button(frm_left, text="Tampilkan Semua", command=show_all_recipes, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=6, column=0, sticky="ew", padx=5, pady=(0,10))

tk.Button(frm_left, text="Urut Nama ↑", command=lambda: sort_by_name(True), bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=7, column=0, sticky="ew", padx=5, pady=(0,5))
tk.Button(frm_left, text="Urut Nama ↓", command=lambda: sort_by_name(False), bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=8, column=0, sticky="ew", padx=5, pady=(0,10))

tk.Label(frm_left, text="Cari Waktu ≤ (menit):", bg="#FFEFD5").grid(row=9, column=0, sticky="w", padx=5)
entry_search_time = tk.Entry(frm_left, bg="#FFF8DC", fg="#333")
entry_search_time.grid(row=10, column=0, sticky="ew", padx=5, pady=(0,5))
tk.Button(frm_left, text="Cari Waktu", command=search_by_time, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=11, column=0, sticky="ew", padx=5, pady=(0,10))

tk.Button(frm_left, text="Urut Waktu ↑", command=lambda: sort_by_time(True), bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=12, column=0, sticky="ew", padx=5, pady=(0,5))
tk.Button(frm_left, text="Urut Waktu ↓", command=lambda: sort_by_time(False), bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=13, column=0, sticky="ew", padx=5, pady=(0,10))

tk.Button(frm_left, text="Hapus Selected", command=delete_selected, fg="#fff", bg="#B22222", activebackground="#8B0000")\
    .grid(row=14, column=0, sticky="ew", padx=5, pady=(0,10))

listbox = tk.Listbox(frm_left, bg="#F5E1C9", fg="#333", selectbackground="#D2B48C",
                     exportselection=False, selectmode="multiple")
listbox.grid(row=15, column=0, sticky="nsew", padx=5, pady=(0,5))
scrollbar = tk.Scrollbar(frm_left, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.grid(row=15, column=1, sticky="nsw", pady=(0,5))
listbox.config(yscrollcommand=scrollbar.set)
listbox.bind("<<ListboxSelect>>", on_select)

# ---------- Frame Kanan ----------
frm_right = tk.Frame(root, bg="#FFEFD5", bd=2, relief="groove")
frm_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
for i in range(7):
    frm_right.rowconfigure(i, weight=0)
frm_right.rowconfigure(1, weight=1)
frm_right.rowconfigure(2, weight=1)
frm_right.columnconfigure(1, weight=1)

tk.Label(frm_right, text="Judul:", bg="#FFEFD5").grid(row=0, column=0, sticky="e", padx=5, pady=(10,2))
entry_title = tk.Entry(frm_right, bg="#FFF8DC", fg="#333")
entry_title.grid(row=0, column=1, sticky="ew", pady=(10,2), padx=(0,5))

tk.Label(frm_right, text="Bahan:", bg="#FFEFD5").grid(row=1, column=0, sticky="ne", padx=5)
text_bahan = tk.Text(frm_right, bg="#FFF8DC", fg="#333")
text_bahan.grid(row=1, column=1, sticky="nsew", pady=(0,2), padx=(0,5))

tk.Label(frm_right, text="Langkah:", bg="#FFEFD5").grid(row=2, column=0, sticky="ne", padx=5)
text_langkah = tk.Text(frm_right, bg="#FFF8DC", fg="#333")
text_langkah.grid(row=2, column=1, sticky="nsew", pady=(0,2), padx=(0,5))

tk.Label(frm_right, text="Waktu (menit):", bg="#FFEFD5").grid(row=3, column=0, sticky="e", padx=5)
entry_waktu = tk.Entry(frm_right, bg="#FFF8DC", fg="#333")
entry_waktu.grid(row=3, column=1, sticky="w", pady=(0,2), padx=(0,5))

tk.Button(frm_right, text="Tambah", command=add_recipe, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=4, column=0, sticky="w", padx=5, pady=(10,5))
tk.Button(frm_right, text="Simpan", command=save_recipe, bg="#D2B48C", fg="#fff", activebackground="#C3A592")\
    .grid(row=4, column=1, sticky="w", pady=(10,5))
tk.Button(frm_right, text="Hapus Semua", command=delete_all, fg="#fff", bg="#B22222", activebackground="#8B0000")\
    .grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=(5,10))

refresh_list()
root.mainloop()
