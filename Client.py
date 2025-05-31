
import threading
import socket
class Client:
	def __init__(self,ip: int,port,name = "") -> None:
		self.name = name
		self.port = port
		self.ip = ip
		self.client: socket.socket = None
		self.connected = self.connect()

	def connect(self) -> bool:
		#returns if the client mannage to connect to the serever
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.ip,self.port))
	
		except Exception as e:
			self.client = None
			return False
		return True
	def disconnect(self):
		self.connected = False
		self.client = None
	def send_message(self, msg: str):
		self.client.send(msg.encode("utf-8"))

	def recv(self) -> str:	
		data = self.client.recv(1024).decode()
		return data
	


		

	