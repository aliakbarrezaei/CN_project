import threading
import socket
import re

class Proxy:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind(("192.168.1.105", 6000))
        self.serverSocket.listen(5)

    def proxy_thread(self, conn, addr):

        request = conn.recv(1024)

        first_line = request.decode().split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")

        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:

            port = 80
            webserver = temp[:webserver_pos]

        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(20)
            s.connect((webserver, port))
            request=request.decode()
            request=re.sub(r'http://.*?/','/',request)
            s.sendall(request.encode())


            while True:
                data = s.recv(1024)
                if len(data) > 0:
                    conn.send(data)
                else:
                    break

            s.close()
            conn.close()
        except socket.error as error_msg:
            if s:
                s.close()
            if conn:
                conn.close()
            print(error_msg)

    def start(self):
        while True:
            client_socket, client_address = self.serverSocket.accept()
            print('Got connection from', client_address)
            d = threading.Thread(target=self.proxy_thread, args=(client_socket, client_address))
            d.daemon=True
            d.start()


def __init__():
    proxy = Proxy()
    proxy.start()


__init__()
