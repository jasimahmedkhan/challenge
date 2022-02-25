import socket
import numpy as np
import config

class SendData:
    def __init__(self, port: int = 4210, addr: str = "127.0.0.1"):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.__port = port
        self.__addr = addr

    def send_data(self, data:list):

        if data.shape != (3,config.LENGTH):
             raise Exception("Invalid data shape")

        pix = np.clip(data, 0, 255).astype(int)

        formated_data = []
        for i in range(config.LENGTH):
            formated_data.append(pix[0][i])
            formated_data.append(pix[1][i])
            formated_data.append(pix[2][i])
        byte_data = bytes(formated_data)

        self.__sock.sendto(byte_data, (self.__addr, self.__port))