import socket
import pickle
from pydantic import BaseModel

from datetime import datetime
from enum import Enum


class SensorData(BaseModel):
    datetime: str
    payload: int


class Status(Enum):
    """
    This enumeration represents the status of the manipulator.
    It can be either UP or DOWN.
    """
    UP = "up"
    DOWN = "down"


class ControllerSignal(BaseModel):
    """
    This pydantic model represents the signals from the controller.

    attributes:
        datetime: the datetime when the signal was sent
        status: the status of the manipulator
    """
    date_time: datetime
    status: Status


HEADER_SIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 1236))
s.listen(5)

while True:
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established.")

    while True:
        # TODO: read not 1024 bytes, but the amount of bytes specified in the header
        msg = client_socket.recv(1024)

        if len(msg) <= 0:
            continue

        signal = pickle.loads(msg)
        print(ControllerSignal.parse_raw(signal))
