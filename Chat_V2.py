import socket
import sys
import threading
import struct
import pickle
from datetime import datetime


class Chat:
    def __init__(self):
        self.__pseudo = input("enter username: \n")
        self.__SERVER = None
        self.__state = False
        self.__port = None
        self.__ip = None
        self.__lsUser = {}

    def run(self):
        self.__address = None
        self.__running = True

        handlers = {
            '/exit': self._exit,  # exit chat application
            '/quit': self._quit,  # quit connection with user
            '/join': self._join,  # join a user to chat
            '/send': self._send,  # send message to user
            '/client': self._client,  # refresh user list
            '/user': self._user,  # show user connected to server
            '/server': self._server,  # connection to the server
            '/off': self._off_serv,  # disconnection to the server
        }
        print('\n''list of command: ')
        for i in handlers.keys():
            print(i)
        print('\n'"first connect to the server by typing /server ip ports")
        print("type /off to disconnect from de server")

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
        host = self.__lsUser[self.__pseudo]["ip"]
        port = self.__lsUser[self.__pseudo]["port"]
        s.bind((host, int(port)))
        print("listen on {} {}".format(host, port))
        self.__s = s
        threading.Thread(target=self._receive).start()

    def _off_serv(self):
        self._send_request("disconnect")

    def _exit(self):
        try:
            self.__running = False
            self.__address = None
            self.__s.close()
            self._send_request("disconnect")
            self.__t.close()

        except:
            pass

    def _quit(self):
        try:
            print("Disconnected from " + str(self.__address[0]))
            self.__address = None
        except TypeError:
            print("You're not connected to anyone")

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
                print("To " + "[" + self.__address[0] + "]" + ": " + param)
                message = (self.__pseudo + "|" + param).encode()
                print(self.__address[1])
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address[1])
                    totalsent += sent
            except OSError:
                print('Error while sending the message')

    def _receive(self):
        if self.__s is not None:
            while self.__running:
                try:
                    data, address = self.__s.recvfrom(1024)
                    msg = data.decode()
                    pseudo = msg.split("|")[0]
                    message = msg.split("|")[1]
                    print(datetime.now().strftime('%H:%M:%S') + " [" + pseudo + "]" + ": " + message)
                    if pseudo not in self.__lsUser:
                        print("Type \"/join " + pseudo + "\" to start chatting with " + pseudo)
                        self._client()

                except socket.timeout:
                    pass
                except OSError:
                    return

    def _client(self):
        Client_List = self._send_request('clients')
        lsUser = {}
        for i in Client_List.split('|')[:-1]:
            data = i.split(" ")
            name = data[0]
            ip = data[1]
            port = data[2]
            coord = {"ip": ip, "port": port}
            lsUser[name] = coord
            self.__lsUser = lsUser
        return self.__lsUser

    def _user(self):
        self._client()
        for i in self.__lsUser.keys():
            print(i)

    def _server(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__SERVER = (tokens[0], int(tokens[1]))
                data = self._send_request(self.__pseudo)
                self.__ip = data[1]
                self.__port = data[2]
                self.__lsUser[self.__pseudo] = {"ip": self.__ip, "port": self.__port}
                self._user()
                self._chat()
            except OSError:
                print("Communication error with the server")

    def _send_request(self, message):
        self.__t = socket.socket()
        if not self.__state:
            self.__t.connect(self.__SERVER)
        totalsent = 0
        msg = pickle.dumps(message.encode())
        self.__t.send(struct.pack('I', len(msg)))
        while totalsent < len(msg):
            sent = self.__t.send(msg[totalsent:])
            totalsent += sent
        data = self.__t.recv(1024).decode()
        self.__t.close()
        self.__state = False
        return data


if __name__ == '__main__':
    Chat().run()
