import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535).decode("utf-8")
        if len(data) == 0:
            break

        # parsing pesan
        dest, msg = data.split("|")

        msg = "<{}>: {}".format(username_cli, msg)

        # teruskan pesan ke semua client
        if dest == "bcast":
            send_broadcast(clients, msg, addr_cli)
        else:
            for dest_sock_cli, dest_addr_cli, dest_username_cli in clients.values():
                print(dest)
                print(dest_username_cli)
                if dest_username_cli == dest:
                    print("Kirim pesan")
                    send_msg(dest_sock_cli, msg)

    # client dc
    sock_cli.close()
    print("Connection closed", addr_cli)

# fungsi broadcast
def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, username_cli in clients.values():
        if not (addr_cli[0] == sender_addr_cli[0] and addr_cli[1] == sender_addr_cli[1]):
            send_msg(sock_cli,data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

# buat object socket server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding object socket ke alamat IP dan port
sock_server.bind(("127.0.0.1", 8000))

# listen
sock_server.listen(5)

# buat dictionary untuk menyimpan info client
clients = {}

while True:
    # accept connection
    sock_cli, addr_cli = sock_server.accept()

    # read username client
    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli," joined")

    # buat thread baru untuk membaca pesan dan jalankan threadnya
    thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
    thread_cli.start()

    #simpan info ttg client ke dictionary
    clients[username_cli] = (sock_cli, addr_cli, thread_cli)