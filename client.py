import socket
import threading
import sys
import pickle

server_addr = ("127.0.0.1", 9000)

username = ""

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    conn.connect(server_addr)
except socket.error as e:
    print("[!!] Failed to connect to server: %s" % e)
    sys.exit()

print("[*] Connected to the server %s on port %d." % (server_addr[0], server_addr[1]))

def receive_menssage():
    while True:
        msg = conn.recv(4096).decode()
        print("Other: %s" % msg)

def main():
    username = input("Username: ")
    conn.send(username.encode())

    t = threading.Thread(target=receive_menssage)
    t.start()

    while True:
        try:
            """users_online = pickle.loads(conn.recv(4096))
            if len(users_online) < 2:
                print("[*] Waiting for another user...")
                continue"""
            msg = input("")
            print("You: %s" % msg)
            data = msg
            conn.send(data.encode())
        except KeyboardInterrupt:
            conn.send("#EXIT".encode())
            print("\n[*] Exiting...")
            conn.close()
            sys.exit()

if __name__ == "__main__":
    main()
