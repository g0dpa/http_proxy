import socket
from threading import Thread
import sys
import time

def usage():
    print('syntax : http_proxy <port>')
    print('sample : http_proxy 8080')

def setServer():
    print('+++ Proxy Server Running')
    print('+++ If you want to Quit, Press Ctrl-C')

    HOST = 'localhost'
    try:
        PORT = int(sys.argv[1])
    except:
        usage()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)

    return sock

def runProxy(sock):

    sock.settimeout(60)
    while True:
        req = sock.recv(1024)
        try:
            reqHost =   req[req.index("Host"):]
            reqHost =   reqHost[len("Host: "):reqHost.index("\r\n")]
            serverDNS = reqHost
            serverPort= 80     #http

            pSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pSock.connect((serverDNS, serverPort))
            pSock.send(req)
            msg = pSock.recv(10000)

            sock.send(msg)
        except Exception as e:
            sock.close()
            print(e)

if __name__=='__main__':

    sock = setServer()
    conn_list = []

    while True:
        try:
            conn, addr = sock.accept()
            t = Thread(target = runProxy, args = (conn,))
            #Daemon Thread dies if main thread dies > Don't need to kill background thread
            t.daemon = True
            conn_list.append(t)
            t.start()

        except KeyboardInterrupt:
            sock.close()
            print("--- Proxy Server OUT...")
            sys.exit(1)
