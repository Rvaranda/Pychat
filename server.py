import socket
import threading
import sys
import pickle

host = "127.0.0.1"
port = 9000
buffer_size = 4096

users_online = []
users_sockets = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((host, port))
except socket.error as e:
    print("[!!] Failed to initialize server: %s" % e)
    sys.exit()

server.listen(2)

print("[*] Listening on port %d..." % port)

def client_handler(client, addr):
    user = client.recv(buffer_size).decode()
    print("[*] %s has connected." % user)

    users_online.append(user)
    users_sockets.append(client)

    #for conn in users_sockets:
    #    conn.send(pickle.dumps(users_online))

    while True:
        data_buffer = ""
        while True:
            data = client.recv(buffer_size).decode()
            data_buffer += data
            if len(data) < buffer_size:
                break
        
        if not "#EXIT" in data_buffer:
            print("[==>] %s says \"%s\"" % (user, data_buffer))
            for i in range(len(users_online)):
                if user != users_online[i]:
                    users_sockets[i].send(data_buffer.encode())
        else:
            break
    
    print("[*] %s has disconnected." % user)
    users_online.remove(user)
    client.close()


def main():
    while True:
        try:
            client, addr = server.accept()
            ct = threading.Thread(target=client_handler, args=(client, addr))
            ct.start()
        except KeyboardInterrupt:
            print("[*] Exiting...")
            sys.exit()

if __name__ == "__main__":
    main()
