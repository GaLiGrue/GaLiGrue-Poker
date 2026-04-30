import socket
import threading

HOST = "10.4.7.24"   # Server-IP (bei anderem PC z.B. "192.168.178.25")
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

running = True


def empfangen():
    """
    Nachrichten vom Server empfangen
    """
    global running

    while running:
        try:
            msg = client.recv(1024).decode()

            if not msg:
                print("Verbindung beendet.")
                break

            print(msg)

            # Wenn Server Eingabe erwartet:
            if msg.startswith("INPUT:"):
                antwort = input("> ")
                client.send(antwort.encode())

        except:
            print("Verbindung verloren.")
            break

    running = False
    client.close()


# Empfangsthread starten
thread = threading.Thread(target=empfangen)
thread.start()


# Hauptthread wartet
while running:
    pass