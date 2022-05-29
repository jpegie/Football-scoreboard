import pickle
import random
import socket
import threading
import time

from PyQt5 import QtWidgets
from DataClasses.Common.Match import SlimMatchInfo

UDP_MAX_SIZE = 1024  # 65535
SERVER_PORT = 6565


class Client:
    port = 0
    host = 'host'
    server_addr = ('255.255.255.255', SERVER_PORT)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    match_info = SlimMatchInfo

    ui_time = QtWidgets.QLabel
    ui_teams = []
    ui_log = QtWidgets.QListWidget
    ui_conn_button = QtWidgets.QPushButton
    ui_scores = []

    def __init__(self):
        self.port = random.randint(6000, 10000)
        self.host = socket.gethostbyname(socket.gethostname())

    def set_ui_connect_button(self, button):
        self.ui_conn_button = button

    def set_ui_log(self, chat_list_widget):
        self.ui_log = chat_list_widget

    def set_ui_time(self, ui):
        self.ui_time = ui

    def set_ui_scores(self, ui):
        self.ui_scores = ui

    def set_ui_teams(self, ui):
        self.ui_teams = ui

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((self.host, self.port))

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.server_socket.settimeout(5)
        self.server_socket.sendto('connect'.encode('utf-8'), self.server_addr)
        try:
            match_info_bin, sender = self.server_socket.recvfrom(UDP_MAX_SIZE)
        except Exception as e:
            print(f"Failed to receive data from server: {str(e)}")
            return
        match_info = pickle.loads(match_info_bin)
        if match_info:
            self.server_addr = sender
            self.match_info = match_info
            self.__start_listening()
            self.__update_ui()
        self.server_socket.settimeout(None)

    def close(self):
        try:
            self.client_socket.close()
        except:
            return

    def __update_log(self, new_records):
        current_records_amount = self.ui_log.count()
        # first_new_i = current_records_amount + (len(new_records) - current_records_amount)
        if len(new_records) > current_records_amount:
            amount_to_add = len(new_records) - current_records_amount
            for i in range(0, amount_to_add):
                new_record = new_records[current_records_amount + i]
                self.ui_log.addItem(new_record)
                self.ui_log.scrollToBottom()
        elif len(new_records) < current_records_amount:
            self.ui_log.clear()
            self.ui_log.addItems(new_records)
            self.ui_log.scrollToBottom()

    def __request_update(self):
        while True:
            time.sleep(1)
            try:
                self.server_socket.sendto('update'.encode('utf-8'), self.server_addr)
            except:
                continue

    def __update_ui(self):
        self.__update_log(self.match_info.log)
        self.ui_conn_button.setEnabled(False)
        self.ui_scores[0].setText(str(self.match_info.teams[0].score))
        self.ui_scores[1].setText(str(self.match_info.teams[1].score))
        self.ui_teams[0].setText(self.match_info.teams[0].name)
        self.ui_teams[1].setText(self.match_info.teams[1].name)
        self.ui_time.setText(self.match_info.time)

    def __start_listening(self):
        threading.Thread(target=self.__listen, daemon=True).start()
        threading.Thread(target=self.__request_update, daemon=True).start()

    def __listen(self):
        while True:
            match_info_bin, server = self.server_socket.recvfrom(UDP_MAX_SIZE)
            match_info = pickle.loads(match_info_bin)
            if match_info:
                self.match_info = match_info
                self.__update_ui()
            else:
                continue
