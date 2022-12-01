import multiprocessing as mp
import os
import random
import datetime
import time

import requests

CONTROLLER_HOST = os.environ.get("CONTROLLER_HOST")  # get the host of the controller from environment variables
CONTROLLER_PORT = os.environ.get("CONTROLLER_PORT")  # get the port of the controller from environment variables


def make_request() -> None:
    """
    This function makes a request to the controller in an infinite loop once per 1/300 second.
    :return:
    """
    while True:
        url = f"http://{CONTROLLER_HOST}:{CONTROLLER_PORT}/sensor_data"  # get the URL of the controller
        raw = {'date_time': datetime.datetime.now().__str__(),
               'payload': random.choice([0, 1])}  # generate a signal for the controller
        requests.post(url, json=raw)  # make a POST request to the controller

        time.sleep(1 / 300)  # wait for 1/300 second


if __name__ == '__main__':
    processes = [mp.Process(target=make_request) for _ in range(8)]  # 8 processes will generate requests

    for process in processes:
        process.start()  # start the processes

    for process in processes:
        process.join()  # wait for the processes to finish
