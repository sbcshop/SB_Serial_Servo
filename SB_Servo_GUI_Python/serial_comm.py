#!/usr/bin/python3

"""
This file handle serial read and write
Developed by - SB Components
http://sb-components.co.uk
"""

from checksum import CheckSum
import serial
import logging
import threading
from tkinter import messagebox


class SerialComm(CheckSum):
    """
    Low level serial operations
    """
    log = logging.getLogger('SerialComm')

    def __init__(self, handlerNotification=None, *args, **kwargs):
        super(SerialComm, self).__init__()

        self.ser = None

        self.alive = False
        self.timeout = 0.01
        self.rxThread = None
        self._dataRecieved = False
        self._responseEvent = None
        self._expectResponse = None
        self._response = None
        self._rxData = []
        self._notification = []
        self._txLock = threading.Lock()
        self.handlerNotification = handlerNotification

    def connect_port(self, port='/dev/ttyS0', baud_rate=115200, timeout=0.5):
        """
        Connects to the Comm Port
        """
        try:
            # open serial port
            self.ser = serial.Serial(port=port, baudrate=baud_rate,
                                     timeout=timeout)
            self.alive = True
            self.rxThread = threading.Thread(target=self._readLoop)
            self.rxThread.daemon = True
            self.rxThread.start()
            return True
        except serial.serialutil.SerialException:
            messagebox.showerror("Port Error", "Couldn't Open Port..!!")
            return False

    def read_port(self, n=1):
        """
        Read n number of bytes from serial port
        :param n: Number of bytes to read
        :return: read bytes
        """
        return self.ser.read(n)

    def write_port(self, data):
        """
        :param data: data to send to servo, type: bytearray
        :return: Number of bits sent
        """
        return self.ser.write(data)

    def flush_input(self):
        self.ser.reset_input_buffer()

    def flush_output(self):
        self.ser.reset_output_buffer()

    def close_port(self):
        """
        Check if the port is open.
        Close the Port if open
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.alive = False

    def disconnect(self):
        """
        Stops read thread, waits for it to exit cleanly and close serial port
        """
        self.alive = False
        self.rxThread.join()
        self.close_port()
        self.log.info("Disconnected Successfully..!")

    def _handleLineRead(self, line, checkResponse=True):
        """
        Handle serially received data
        """
        if self._responseEvent and not self._responseEvent.is_set():
            self._response = line
            if not checkResponse:
                # End of response reached; notify waiting thread
                self.log.debug('Response: %s', self._response)
                self._responseEvent.set()
        else:
            # Nothing was waiting for this - treat it as notification
            self._notification.append(line)
            if self.ser.inWaiting() == 0:
                # No more chars for this notification
                self.log.debug('Notification: %s', self._notification)
                self.log.debug('No Response From Motor: Serial Device '
                               'Connected')
                self._notification = []

    def _readLoop(self):
        """
        Read thread main loop
        """
        try:
            while self.alive:
                data = self.read_port(1)
                if data != b'':
                    self._dataRecieved = True
                    self._rxData.append(data)
                elif data == b'' and self._dataRecieved:
                    self._dataRecieved = False
                    self._handleLineRead(self._rxData, checkResponse=False)
                    #  Empty the Receiving list
                    self._rxData = []
        except serial.SerialException as Se:
            print("Serial Exception: ", Se)
            self.close_port()

    def write(self, data, waitForResponse=True, timeout=1):
        """
        Write data to serial port
        """
        with self._txLock:
            if waitForResponse:
                self._response = []
                self._responseEvent = threading.Event()
                self.log.debug('Data to Servo: %s', data)
                self.write_port(data)
                if self._responseEvent.wait(timeout):
                    self._responseEvent = None
                    self._expectResponse = False
                    return self._response
                else:
                    self._responseEvent = None
                    self._expectResponse = False
            else:
                self.log.debug('Data to Servo: %s', data)
                self.write_port(data)
                self.flush_input()

