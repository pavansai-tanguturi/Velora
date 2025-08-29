import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                print(f"\nFriend: {msg}\nYou: ", end="")
        except:
            print("\n[ERROR] Connection lost.")
            sock.close()
            break

def main():
    host = input("Enter server host (from ngrok, e.g. 0.tcp.in.ngrok.io): ").strip()
    port = int(input("Enter server port (from ngrok, e.g. 12345): ").strip())

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to chat!")

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    while True:
        msg = input("You: ")
        try:
            sock.send(msg.encode('utf-8'))
        except:
            print("[ERROR] Message failed.")
            break

if __name__ == "__main__":
    main()