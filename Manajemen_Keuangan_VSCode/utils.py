import csv
import os
from datetime import datetime

DATA_PATH = "data/transaksi.csv"
DATA = []

def load_csv():
    global DATA
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"])
    with open(DATA_PATH, mode="r") as file:
        reader = csv.DictReader(file)
        DATA = list(reader)

def simpan_csv():
    with open(DATA_PATH, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"])
        writer.writeheader()
        for row in DATA:
            writer.writerow(row)

def tampilkan_data():
    if not DATA:
        print("Belum ada data transaksi.")
        return
    print("\n--- Daftar Transaksi ---")
    for d in DATA:
        print(f"ID: {d['id']} | {d['tanggal']} - {d['jenis']} - {d['kategori']} - Rp{d['jumlah']} | {d['deskripsi']}")

def generate_id():
    return str(max([int(d["id"]) for d in DATA], default=0) + 1)

def tambah_transaksi(queue):
    tanggal = input("Tanggal [YYYY-MM-DD]: ") or datetime.now().strftime("%Y-%m-%d")
    jenis = input("Jenis [Pemasukan/Pengeluaran]: ")
    kategori = input("Kategori: ")
    jumlah = input("Jumlah (angka): ")
    deskripsi = input("Deskripsi: ")

    data_baru = {
        "id": generate_id(),
        "tanggal": tanggal,
        "jenis": jenis,
        "kategori": kategori,
        "jumlah": jumlah,
        "deskripsi": deskripsi
    }

    DATA.append(data_baru)
    print("✅ Transaksi berhasil ditambahkan.")
    queue.enqueue(f"Transaksi baru: {jenis} Rp{jumlah} - {kategori}")

def update_transaksi():
    id_ = input("Masukkan ID yang ingin di-update: ")
    for d in DATA:
        if d["id"] == id_:
            print("Masukkan data baru (biarkan kosong jika tidak ingin diubah):")
            d["tanggal"] = input(f"Tanggal [{d['tanggal']}]: ") or d["tanggal"]
            d["jenis"] = input(f"Jenis [{d['jenis']}]: ") or d["jenis"]
            d["kategori"] = input(f"Kategori [{d['kategori']}]: ") or d["kategori"]
            d["jumlah"] = input(f"Jumlah [{d['jumlah']}]: ") or d["jumlah"]
            d["deskripsi"] = input(f"Deskripsi [{d['deskripsi']}]: ") or d["deskripsi"]
            print("✅ Transaksi berhasil di-update.")
            return
    print("❌ ID tidak ditemukan.")

def hapus_transaksi(stack):
    id_ = input("Masukkan ID transaksi yang ingin dihapus: ")
    for i, d in enumerate(DATA):
        if d["id"] == id_:
            konfirmasi = input(f"Yakin hapus transaksi {id_}? (y/n): ")
            if konfirmasi.lower() == "y":
                removed = DATA.pop(i)
                stack.push(removed)
                print("🗑️ Transaksi berhasil dihapus.")
                return
            else:
                print("❌ Penghapusan dibatalkan.")
                return
    print("❌ ID tidak ditemukan.")

def undo_hapus(stack):
    if stack.is_empty():
        print("❌ Tidak ada transaksi yang bisa di-undo.")
        return
    restored = stack.pop()
    DATA.append(restored)
    print(f"✅ Transaksi ID {restored['id']} berhasil di-undo.")

def tampilkan_notifikasi(queue):
    print("\n📥 Notifikasi Transaksi:")
    while not queue.is_empty():
        print("- " + queue.dequeue())

def buat_laporan_bulanan():
    from pandas import read_csv, to_datetime
    import pandas as pd

    df = read_csv(DATA_PATH)
    df["tanggal"] = to_datetime(df["tanggal"], errors="coerce")
    df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

    laporan = df.groupby(["bulan", "jenis"])["jumlah"].sum().unstack(fill_value=0)
    laporan.reset_index(inplace=True)

    laporan_path = "data/laporan_bulanan.csv"
    laporan.to_csv(laporan_path, index=False)

    print("\n✅ Laporan bulanan berhasil dibuat di: " + laporan_path)
    print(laporan.to_string(index=False))
