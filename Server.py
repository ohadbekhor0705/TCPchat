import socket
import threading


class Server:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.clients: set[socket.socket] = set()
    def handle_client(self, conn: socket.socket, addr):
        connected = True
        
        while connected:
            try:
                message = conn.recv(1024)
                if message:
                    sending_thread = threading.Thread(target=self.send_to_all_clients,args=(conn,message))
                    print(f"[{addr}] {message.decode("utf-8")}")
                    if len(self.clients) != 0:
                        sending_thread.start()
                    if message.decode() == "!dis":
                        sending_thread.join()
                        connected = False
                
            except ConnectionResetError:

                connected = False
        self.clients.remove(conn)
        conn.close()

    def start(self):
        print(f"[SERVER] listing.... {socket.gethostbyname(socket.gethostname())},\n[PORT] {"."*13} {self.port}")
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.ip, self.port))
                s.listen()
                conn, addr = s.accept()
                self.clients.add(conn)
                print(f"[Client]......... {addr} connected.")
                threading.Thread(target=self.handle_client,args=(conn,addr)).start()
    def send_to_all_clients(self , sender: socket.socket, message: bytes):
        for client in self.clients:
            if client != sender:
                if message.decode() == "!dis":
                    client.send(f"{sender} disconnected from the chat".encode())
                    break
                else:
                    client.send(message)


server = Server("0.0.0.0",8080)
server.start()