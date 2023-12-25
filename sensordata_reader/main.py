import numpy as np
import os
import zmq
import time
import datetime
import logging
import csv


def start_logging():
    logging.basicConfig(filename='gorelik.log', level=logging.CRITICAL)


def loggi(message):
    logging.critical(f"{datetime.datetime.utcnow()} : {message}")
    time.sleep(0.03)


def connecting():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    try:
        socket.connect("tcp://192.168.0.102:5555")
    except zmq.ZMQError as e:
        loggi(f"Can't connect to server: {str(e)}")
        time.sleep(0.7)
        connecting()
    return socket


def write_to_csv(curr_time, sensor, value):
    with open(DATA_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([curr_time, sensor, value])


def analysing_data(recieved_data):
    try:
        if recieved_data[0] in ['p', 't', 'm']:
            if len(recieved_data) == 1:
                recieved_data.append('true')
            write_to_csv(datetime.datetime.utcnow(), recieved_data[0], recieved_data[1])
            print(recieved_data[0], recieved_data[1])
        else:
            loggi('Empty required data')
    except Exception as e:
        loggi(f'{str(e)}')
        time.sleep(0.05)


DATA_PATH = 'gorelik.csv'
start_logging()


def main():
    socket = connecting()

    while True:
        try:
            recieved_data = socket.recv_string().split()
            if recieved_data is not None:
                analysing_data(recieved_data)
            else:
                loggi("Didn't get the data")
        except Exception as e:
            loggi(f'{str(e)}')
            time.sleep(0.05)


if __name__ == "__main__":
    main()
