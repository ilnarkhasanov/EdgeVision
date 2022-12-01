import os
import pickle
import socket
import logging
from typing import List
from enum import Enum
from datetime import datetime

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
    date_time: datetime
    payload: int


class ControllerSignal(BaseModel):
    """
    This pydantic model represents the signals from the controller.

    attributes:
        datetime: the datetime when the signal was sent
        status: the status of the manipulator
    """
    date_time: datetime
    status: Status


logging.basicConfig(filename='logs/controller.log', level=logging.INFO)
app = FastAPI()  # a FastAPI app instance
sensor_signals = []  # this list will contain the signals from the sensors

client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # declare a socket for the client-server

MANIPULATOR_HOST = os.environ.get("MANIPULATOR_HOST")  # get the host of the manipulator
MANIPULATOR_PORT = int(os.environ.get("MANIPULATOR_PORT"))  # get the port of the manipulator
client_server.connect((MANIPULATOR_HOST, MANIPULATOR_PORT))  # connect to the manipulator server


async def decision(signals_from_sensors: List[SensorSignal]) -> ControllerSignal:
    """
    This function makes a decision based on the signals from the sensors.

    Idea:
    If the sum of the payloads is even number, then the status should be UP.
    Otherwise, the status should be DOWN.

    param sensor_signals: list of signals from the sensors
    :return: the controller signal that will be sent to the manipulator server
    """
    total_payload = sum(signal.payload for signal in signals_from_sensors)  # sum the payloads of the signals
    if total_payload % 2 == 0:
        return ControllerSignal(date_time=datetime.now(), status=Status.UP)
    else:
        return ControllerSignal(date_time=datetime.now(), status=Status.DOWN)


async def send_data() -> None:
    """
    This function waits for 5 seconds and then send the data to the manipulator server.
    :return: None
    """
    global sensor_signals

    while True:
        await asyncio.sleep(5)  # wait for 5 seconds, but don't block the event loop

        decision_signal = await decision(sensor_signals)  # get the decision signal
        sensor_signals_b = pickle.dumps(decision_signal.json())  # serialize signals
        logging.info(decision_signal.json())  # log the signal

        client_server.send(sensor_signals_b)  # send serialized signals to the manipulator server

        sensor_signals = []  # clear the list


@app.post("/sensor_data")
async def receive_sensor_signal(signal: SensorSignal) -> SensorSignal:
    """
    This function receives a signal from the sensors and adds it to the sensor_signals list.
    param signal: signal from the sensors
    :return: sent signal
    """
    sensor_signals.append(signal)  # add the signal to the signals list
    print(signal.json())  # print the signal
    return signal


@app.on_event("startup")
async def startup_event() -> None:
    """
    This function is called when the app starts.
    :return: None
    """
    asyncio.create_task(send_data())
