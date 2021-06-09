import socket
import sys
import threading

def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
        print(data)
    sock_cli.close()

# buat obj socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
sock_cli.connect(("127.0.0.1", 8000))

# kirim username
sock_cli.send(bytes(sys.argv[1], "utf-8"))

# buat thread untuk membaca pesan dan jalankan thread
thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    # kirim/terima pesan
    dest = input("Masukkan username tujuan (bcast untuk broadcast pesan):")
    msg = input("Masukkan pesan: ")
    if msg == "exit":
        sock_cli.close()
        break
    sock_cli.send(bytes("{}|{}".format(dest, msg), "utf_8"))