import socket
import sys
import threading
import subprocess
import struct
import pickle

#test 6
# test branch

class Chat:
    def __init__(self):
        self.__pseudo = input("enter username: \n")
        self.__port = 5000
        self.__ip = None
        self._lsUser = {}

    def run(self):
        self.__address = None
        self.__running = True
        #threading.Thread(target=self._receive).start()
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/address': self._client,
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
        #threading.Thread(target=self._receive).start()

    def _exit(self):
        self._send("disconnect")
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        tokens = self._lsUser[param]
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
                    print(data.decode())
                except socket.timeout:
                    pass
                except OSError:
                    return

    def _client(self):
        print(self.__address)

    def _user(self):
        self.__user = subprocess.Popen(["whoami"], stdout=subprocess.PIPE)
        print(self.__user.communicate()[0].decode().rstrip())

    def _server(self, param):
        self.__s = socket.socket()
        tokens = param.split(' ')
        print(tokens)
        if len(tokens) == 2:
            try:
                self.__s.connect((tokens[0], int(tokens[1])))
                totalsent = 0
                msg = pickle.dumps(self.__pseudo.encode())
                self.__s.send(struct.pack('I', len(msg)))
                while totalsent < len(msg):
                    sent = self.__s.send(msg[totalsent:])
                    totalsent += sent
                data = self.__s.recv(1024).decode()
                return data
            except OSError:
                print("Communication error with the server")

    def _send_pseudo(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat().run()
    else:
        Chat().run()
