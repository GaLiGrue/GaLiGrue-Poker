import socket
import threading

HOST = '10.4.7.24'  # Server-IP anpassen
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"[SERVER] {msg}")
        except:
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    name = input("Dein Name: ")
    client.send(name.encode())

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input()
        client.send(msg.encode())


if __name__ == "__main__":
    main()