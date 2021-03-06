import socket
import tkinter as tk
import time
from threading import Thread
import urllib.request

'''
PUT THE SERVER IP HERE!!!!!
'''
SERVERIP = '81.100.27.47'
    
class Client:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ChattingSHITE')
        self.topframe = tk.Frame(self.window)
        self.chatframe = tk.Frame(self.window, padx=2, pady=2)
        self.namelabel= tk.Label(self.topframe, text='Name: ')
        self.nameentry = tk.Entry(self.topframe, width=10)
        self.namelabel.pack(side='left')
        self.nameentry.pack(side='right')
        
        self.displaychat = tk.Text(self.chatframe, state='disabled',
                              width=60, height=10, bd=1, relief='solid',
                                   wrap='word')
        self.displaychat.bind("<1>", lambda event: self.displaychat.focus_set())
        self.chatscroll = tk.Scrollbar(self.chatframe, command=self.displaychat.yview)
        self.chatscroll.pack(side='right', expand=True, fill='y')
        self.displaychat.pack(side='left', expand=True, fill='both')
        
        self.displaychat.config(yscrollcommand=self.chatscroll.set, state='disabled')
        self.msgentry = tk.Entry(self.window, width=60)
        self.send = tk.Button(self.window, text='Send', command=self.sendmsg)
        self.msgentry.bind('<Return>', self.sendmsg)

        self.topframe.pack()
        self.chatframe.pack(fill='both', expand=True)
        self.msgentry.pack(fill='y')
        self.send.pack()

        t = Thread(target=self.displayincoming)
        t.start()

        self.window.lift()
        self.window.mainloop()

    def localmsg(self, msg):
        self.displaychat.config(state='normal')
        self.displaychat.insert(tk.END, msg + '\n\n')
        self.displaychat.config(state='disabled')

    def sendmsg(self, event=None):
        nowtime = time.time()
        timestamp = time.ctime(nowtime)
        name = self.nameentry.get()
        message = self.msgentry.get()

        package = ('%s\n%s: %s\n\n' % (timestamp, name, message)).encode('utf-8')
        if len(self.msgentry.get()):
            try:
                s.send(package)
                self.msgentry.delete(0, 'end')
            except BrokenPipeError:
                self.localmsg('Error: No connection to server.')
                


    def displayincoming(self):
        while True:
            incoming = s.recv(4096).decode('utf-8')
            self.displaychat.config(state='normal')
            self.displaychat.insert(tk.END, incoming)
            self.displaychat.see(tk.END)
            self.displaychat.config(state='disabled')
            time.sleep(0.1)

localip = socket.gethostbyname(socket.gethostname())
# wanip = urllib.request.urlopen("http://myip.dnsdynamic.org/").read()
host = SERVERIP
port = 5000
s = socket.socket()

try:
    print('attempting connection')
    s.connect((host, port))
    print('connected')
except ConnectionRefusedError:
    print('Couldnae connect')

client = Client()


s.close()
