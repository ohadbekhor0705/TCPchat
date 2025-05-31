import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from Client import *
import threading

class App:
    def __init__(self) -> None:
        self.root = None
        self.conn = None
        self.ip_field = None
        self.port_field = None
        self.chat_field = None
        self.input_field = None
        self.width = 1200
        self.height = 700
        self.font = ("Calibri",16)
        self.chat_font = ("Calibri",10)
        self.send_button = None
        self.ip_label = None
        self.port_label = None
        self.connect_btn = None

    def setup_window(self):
        self.root = ttk.Window(themename="cyborg")
        self.root.resizable(False,False)
        self.root.geometry("{}x{}".format(self.width,self.height))
        self.root.title("Client chat")
        self.create_elements()


    def create_elements(self):
        self.chat_field =  ttk.Text(
            self.root, width = int(60*1.5), font = self.chat_font, height= self.height*3.5//100, state = "disabled")
        self.chat_field.place(x=0,y=0)

        self.input_field = ttk.Entry(
            self.root,
            font = self.font,
            width= 50
        )
        self.input_field.place(x=0,y=550)

        self.send_button = ttk.Button(
            self.root,
            text= "SEND",
            bootstyle="primary",
            width=50,
            state= "disabled",
            command=self.send
        )
        self.send_button.place(x=750,y=550)

        self.ip_label = ttk.Label(
            self.root,
            width = 30,
            text="IP:",
            font=self.font
        )
        self.ip_label.place(x=860,y=30)

        self.ip_field = ttk.Entry(
            self.root,
            width=20,
            font= self.font
            
        )
        self.ip_field.place(x= 900,y= 30)
        self.ip_field.insert(0,"127.0.0.1")

        self.port_label = ttk.Label(
            self.root,
            width = 29,
            text="PORT:",
            font=self.font
        )
        self.port_label.place(x=860,y=110)

        self.port_field = ttk.Entry(
            self.root,
            width=45,
            font= self.font,
         
        )
        self.port_field.insert(0,"8080")
        self.port_field.place(x = 940, y = 110)

        self.connect_btn = ttk.Button(
            self.root,
            width=35,
            text="Connect",
            bootstyle= "SUCCESS",
            command=self.connect
        )
        self.connect_btn.place(x = 860, y = 170)
        

    def connect(self):
        try:
            ip = self.ip_field.get()
            port = int(self.port_field.get())
            self.conn = Client(ip,port,"")
            if self.conn.connected:
                self.ip_field.config(state="disabled")
                self.port_field.config(state="disabled")
                self.ip_field.config(state="disabled")
                self.port_field.config(state="disabled")
                self.connect_btn.config(state="disabled")

                self.input_field.config(state="normal")
                self.send_button.config(state="normal")

                threading.Thread(target=self.update).start()
            else:
                self.add_row("[SYSTEM] couldn't connect to server!")
        except Exception as err:
            print(err)
            self.add_row("[SYSTEM] Invalid Data! pleas check your server, ip & port.")           
    def update(self):
        try:
            while True:
                if not self.conn:
                    break
                data = self.conn.recv()
     
                if data:
                    self.add_row(data)
                
        except Exception as e:
            self.add_row(e)
            

    def send(self):
        msg = self.input_field.get()
        self.add_row(msg)
        self.conn.send_message(msg)
        if msg == "!dis":
            self.disconnect()
    
    def add_row(self, msg):
         self.chat_field.configure(state="normal")
         self.chat_field.insert(END,f"{msg} \n")
         self.chat_field.configure(state="disabled")
    
    def clear_chat(self):
         self.chat_field.configure(state="normal")
         self.chat_field.delete(1,END)
         self.chat_field.configure(state="disabled")
    def disconnect(self):
        self.send_button.config(state="disabled")
        self.input_field.config(state="disabled")
        self.ip_field.config(state="normal")
        self.port_field.config(state="normal")
        self.connect_btn.config(state="normal")
        self.conn = None


    def draw(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.setup_window()
    app.draw()