import socket
import pickle
import struct


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "34.125.218.56"
        # self.server = "34.16.141.101"
        self.port = 3389
        self.addr = (self.server, self.port)
        # self.p = self.connect()
        self.player_id_and_cards = self.connect()

    # def getP(self):
    #     return self.p

    def getPlayerIdAndCards(self):
        return self.player_id_and_cards

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096*2000))
        except:
            pass

    def send(self, data):
        # try:
        #     packet = pickle.dumps(data)
        #     length = struct.pack('!I', len(packet))
        #     packet = length + packet
        #     buf = b''
        #     while len(buf) < 4:
        #         buf += socket.recv(4 - len(buf))
        #
        #     length = struct.unpack('!I', buf)[0]
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096*2000))
        except socket.error as e:
            print(e)

    # def send_data(self, data):
    #     serialized_data = pickle.dumps(data)
    #     # send data size, data identifier and payload
    #     self.client.sendall(struct.pack('>I', len(data)))
    #     self.client.sendall(serialized_data)
    #
    # def receive_data(self):
    #     '''
    #     @brief: receive data from the connection assuming that
    #         first 4 bytes represents data size,
    #         next 4 bytes represents data identifier and
    #         successive bytes of the size 'data size'is payload
    #     @args[in]:
    #         conn: socket object for conection from which data is supposed to be received
    #     '''
    #     # receive first 4 bytes of data as data size of payload
    #     data_size = struct.unpack('>I', self.client.recv(4))[0]
    #     # receive payload till received payload size is equal to data_size received
    #     received_data = b""
    #     reamining_data_size = data_size
    #     while reamining_data_size != 0:
    #         received_data += self.client.recv(reamining_data_size)
    #         reamining_data_size_size = data_size - len(received_data)
    #     data = pickle.loads(received_data)
    #     return (data)