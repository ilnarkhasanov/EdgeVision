import pickle
import socket
from typing import List
from enum import Enum

from fastapi import FastAPI
import asyncio
from pydantic import BaseModel


class Status(Enum):
    """
    This enumeration represents the status of the manipulator.
    It can be either UP or DOWN.
    """
    UP = "up"
    DOWN = "down"


class SensorSignal(BaseModel):
    """
    This pydantic model represents a signal from the sensors.

    attributes:
        datetime: the datetime when the signal was sent
        payload: the payload of the signal
    """
    datetime: str
    payload: int


class ControllerSignals(BaseModel):
    """
    This pydantic model represents the signals from the controller.

    attributes:
        datetime: the datetime when the signal was sent
        status: the status of the manipulator
    """
    datetime: str
    status: Status


app = FastAPI()  # a FastAPI app instance
sensor_signals = []  # this list will contain the signals from the sensors

client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # declare a socket for the client-server
client_server.connect(('localhost', 1235))  # connect to the manipulator server


async def send_data() -> None:
    """
    This function waits for 5 seconds and then send the data to the manipulator server.
    :return: None
    """
    global sensor_signals

    while True:
        await asyncio.sleep(5)  # wait for 5 seconds, but don't block the event loop
        sensor_signals_b = pickle.dumps(sensor_signals)  # serialize signals
        client_server.send(sensor_signals_b)  # send serialized signals to the manipulator server
        sensor_signals = []  # clear the list


@app.post("/sensor_data")
async def receive_sensor_signal(signal: SensorSignal) -> SensorSignal:
    """
    This function receives a signal from the sensors and adds it to the sensor_signals list.
    param signal: signal from the sensors
    :return: sent signal
    """
    sensor_signals.append(signal.json())
    return signal


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(send_data())
