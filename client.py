import socket
import threading
import sys

server_addr = ("127.0.0.1", 9000)

username = ""

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    conn.connect(server_addr)
except socket.error as e:
    print("[!!] Failed to connect to server: %s" % e)
    sys.exit()

print("[*] Connected to the server %s on port %d." % (server_addr[0], server_addr[1]))

def main():
    username = input("Username: ")
    conn.send(username.encode())
    while True:
        try:
            msg = input("Say: ")
            data = msg
            conn.send(data.encode())
        except KeyboardInterrupt:
            conn.send("#EXIT".encode())
            print("\n[*] Exiting...")
            conn.close()
            sys.exit()

if __name__ == "__main__":
    main()
