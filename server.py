import socket
import time
from threading import Thread


def send(msg):
    if msg:
        for client in clientslist:
            print('sending %s to %s' % (msg, client[0]))
            client[0].send(msg.encode('utf-8'))
    else:
##        print('no data to send')
        pass

def clienthandling():
    global clientlist
    try:
##        print('checking for new clients')
        c, addr = s.accept()
        if (c, addr) not in clientslist:
            print(str(addr) + ' joined.')
            send('%s has joined.\n\n' % str(addr))
            clientslist.append((c, addr))
            c.send(joinmsg.encode('utf-8'))
    except socket.error:
        pass

def recv():
    global data
    for client in clientslist:
##        print('seeing if any data is arriving')
        try:
            data = client[0].recv(4096)
            data = data.decode('utf-8')
            print('RECIEVED from %s: \n%s' % (client, data))
            if data == '':
                send('%s has disconnected.\n\n' % str(client[1]))
                clientslist.remove(client)
                
        except socket.error:
##            print('nothing to recv')
            pass

localip = socket.gethostbyname(socket.gethostname())
host = '0.0.0.0'
port = 5000

print('Server started on %s:%d' % (host, port))
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.setblocking(False)

running = True
data = None

clientslist = []
joinmsg = 'Ur connected!!\n\n'

while running:
    s.listen(10)
    clienthandling()
    recv()
    send(data)
    data = None
    time.sleep(0.1)


for c in clientslist:
    c[0].close()




