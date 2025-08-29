import socket
import threading

# Server config
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5003       # Local port (ngrok will tunnel this)

# Keep track of connected clients
clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"{addr}: {msg}")
            broadcast(msg, conn)
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"[DISCONNECTED] {addr} left.")

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] Listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start()