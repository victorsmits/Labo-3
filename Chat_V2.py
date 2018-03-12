import socket
import sys
import threading
import subprocess
import struct
import pickle
from datetime import datetime


#test 8
# test branch

class Chat:
    def __init__(self):
        self.__s = socket.socket()
        self.__pseudo = input("enter username: \n")
        self.__port = 5000
        self.__ip = None
        self.__lsUser = {}

    def run(self):
        self.__address = None
        self.__running = True
        threading.Thread(target=self._receive).start()
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/client': self._client,
            '/user': self._user,
            '/server': self._server,
        }

        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ') + 1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur lors de l'exécution de la commande.")
            else:
                print('Command inconnue:', command)

    def _chat(self):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        host = socket.gethostname()
        port = self.__port
        s.bind((host, port))
        self.__s = s
        print('Écoute sur {}:{}'.format(host, port))
        threading.Thread(target=self._receive).start()

    def _exit(self):
        self._send("disconnect")
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        tokens = self.__lsUser[param]
        if len(tokens) == 2:
            try:
                self.__address = (param, (tokens['ip'], int(tokens['port'])))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")

    def _send(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')

    def _receive(self):
        if self.__s is not None:
            while self.__running:
                try:
                    data, address = self.__s.recvfrom(1024)
                    msg = data.decode()
                    pseudo = msg.split(" ")[0]
                    message = msg.split(" ")[1]
                    print(datetime.now().strftime('%H:%M:%S') + " [" + pseudo + "]" + ": " + message)
                    if pseudo not in self.__lsUser:
                        print("Type \"/join " + pseudo + "\" to start chatting with " + pseudo)
                        self._client()

                except socket.timeout:
                    pass
                except OSError:
                    return

    def _client(self):
        list = self._send_request("clients")
        lsUser = {}
        for i in list.split('\n')[:-1]:
            data = i.split(" ")
            name = data[0]
            ip = data[1]
            port = data[2]
            coord = {'ip': ip, 'port': port}
            coord["ip"] = ip
            coord["port"] = port
            lsUser[name] = coord
            self.__lsUser = lsUser
            print(lsUser)
            return self.__lsUser

    def _user(self):
        self._client()
        for i in self.__lsUser.keys():
            print(i)

    def _server(self, param):
        self.__s = socket.socket()
        tokens = param.split(' ')
        print(tokens)
        if len(tokens) == 2:
            try:
                self.__s.connect((tokens[0], int(tokens[1])))
                data = self._send_request(self.__pseudo)
                self.__pseudo = data[0]
                self.__ip = data[1]
                self.__port = data[2]
                self.__lsUser[data[0]] = {"ip": self.__ip, "port": self.__port}
                return self.__lsUser
            except OSError:
                print("Communication error with the server")

    def _send_request(self, message):
        totalsent = 0
        msg = pickle.dumps(message.encode())
        self.__s.send(struct.pack('I', len(msg)))
        while totalsent < len(msg):
            sent = self.__s.send(msg[totalsent:])
            totalsent += sent
        data = self.__s.recv(1024).decode()
        print(data)
        return data


if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat().run()
    else:
        Chat().run()
