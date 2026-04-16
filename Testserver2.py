import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clients = {}  # name -> socket


def handle_client(conn, addr):
    try:
        # Name empfangen
        name = conn.recv(1024).decode()
        clients[name] = conn
        print(f"[JOIN] {name} hat sich verbunden ({addr})")

        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{name}] {msg}")

    except:
        pass
    finally:
        print(f"[LEFT] {name} hat die Verbindung getrennt")
        del clients[name]
        conn.close()


def send_messages():
    while True:
        target = input("An wen senden? (Name): ")
        if target not in clients:
            print("Client nicht gefunden.")
            continue

        msg = input("Nachricht: ")
        try:
            clients[target].send(msg.encode())
        except:
            print("Fehler beim Senden.")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server läuft auf Port {PORT}...")

    threading.Thread(target=send_messages, daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()