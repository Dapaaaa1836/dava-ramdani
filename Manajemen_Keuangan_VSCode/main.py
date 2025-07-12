from utils import *
from stack import Stack
from queue import Queue # type: ignore

undo_stack = Stack()
notif_queue = Queue()

def menu():
    print("\n--- Aplikasi Manajemen Keuangan ---")
    print("1. Tambah Transaksi")
    print("2. Lihat Semua Transaksi")
    print("3. Update Transaksi")
    print("4. Hapus Transaksi")
    print("5. Undo Hapus Terakhir")
    print("6. Tampilkan Notifikasi")
    print("7. Laporan Bulanan")
    print("0. Keluar")

if __name__ == "__main__":
    load_csv()
    while True:
        menu()
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            tambah_transaksi(notif_queue)
        elif pilihan == "2":
            tampilkan_data()
        elif pilihan == "3":
            update_transaksi()
        elif pilihan == "4":
            hapus_transaksi(undo_stack)
        elif pilihan == "5":
            undo_hapus(undo_stack)
        elif pilihan == "6":
            tampilkan_notifikasi(notif_queue)
        elif pilihan == "7":
            buat_laporan_bulanan()
        elif pilihan == "0":
            simpan_csv()
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")
