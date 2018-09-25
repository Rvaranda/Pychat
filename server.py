import socket
import threading
import sys

host = "127.0.0.1"
port = 9000
buffer_size = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((host, port))
except socket.error as e:
    print("[!!] Failed to initialize server: %s" % e)
    sys.exit()

server.listen(5)

print("[*] Listening on port %d..." % port)

def client_handler(client, addr):
    user = client.recv(buffer_size).decode()
    print("[*] %s has connected." % user)

    while True:
        data_buffer = ""
        while True:
            data = client.recv(buffer_size).decode()
            data_buffer += data
            if len(data) < buffer_size:
                break
        
        if not "#EXIT" in data_buffer:
            print("[==>] %s says \"%s\"" % (user, data_buffer))
        else:
            break
    
    print("[*] %s has disconnected." % user)
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
