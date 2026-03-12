import socket

# --- Server Side ---
def start_server():
    """
    Startet einen Server mit der Adresse "127.0.0.1" und dem Port "12345"
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345)) # Bind to address and port
    server_socket.listen(1) # Listen for incoming connections
    print("Warte auf Spieler...")
    conn, addr = server_socket.accept() # Accept connection
    print(f"Verbunden über {addr}")
    data = conn.recv(1024) # Receive data
    print(f"Daten empfangen: {data.decode()}")
    conn.sendall(b"<<Server>> Test") # Send response
    conn.close()

# --- Client Side ---
def start_client():
    """
    Startet einen Client und verbindet ihm zu "127.0.0.1:12345"
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345)) # Connect to server
    client_socket.sendall(b"<<Client>> Hallo")
    data = client_socket.recv(1024)
    print(f"Empfangen: {data.decode()}")
    client_socket.close()

#start_server() # nur auf EINEM server

#start_client() # auf jedem client