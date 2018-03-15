import socket
import struct
import pickle

#SERVERADDRESS = (socket.gethostname(), 7000)
SERVERADDRESS = ('0.0.0.0', 7000)


# python main.py server

class Server:
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__clients = {}

    def run(self):
        self.__s.listen()
        while True:
            print("while True")
            client, addr = self.__s.accept()
            clt = self._receive(client)
            print('data:', clt)
            try:
                if clt == 'clients':
                    print('clients request')
                    self._handle(client)

                elif clt == 'disconnect':
                    for i, j in self.__clients.items():
                        if j[0] == addr[0]:
                            del self.__clients[i]
                else:
                    self.__clients[clt] = addr
                    client.send(("{} {} {}".format(clt, addr[0], addr[1])).encode())
                print(self.__clients, '\n')
                client.close()
            except OSError:
               print('Error with the reception of message')

    # fonction receive to get a message from the client
    def _receive(self, client):
        size = struct.unpack('I', client.recv(4))[0]
        data = pickle.loads(client.recv(size)).decode()
        print(data, size, client)
        return data

    def _handle(self, client):
        clt = ""
        print(client)
        for i, j in self.__clients.items():
            clt += ("{} {} {}|".format(i, j[0], j[1]))
        print(clt)
        client.send(clt.encode())


if __name__ == '__main__':
    Server().run()
