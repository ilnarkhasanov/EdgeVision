import socket
import pickle
from pydantic import BaseModel


class SensorData(BaseModel):
    datetime: str
    payload: int


HEADER_SIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 1235))
s.listen(5)

while True:
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established.")

    while True:
        # TODO: read not 1024 bytes, but the amount of bytes specified in the header
        msg = client_socket.recv(1024)

        if len(msg) <= 0:
            break

        for parsed_signal in pickle.loads(msg):
            print(SensorData.parse_raw(parsed_signal))
        print()
