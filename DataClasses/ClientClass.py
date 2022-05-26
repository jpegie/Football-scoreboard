import pickle
import random
import socket
import threading
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget

from DataClasses.SlimInfo import SlimMatchInfo
from DataClasses.DataClass import MatchInfo
from DataClasses.DataClass import MatchStatus
from DataClasses.StopwatchClass import Stopwatch


class Client:
    UDP_MAX_SIZE = 1024  # 65535
    name = ''
    port = 6565
    host = 'host'
    server_addr = ('255.255.255.255', 6565)

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

    def set_connect_button(self, button):
        self.ui_conn_button = button

    def set_chat(self, chat_list_widget):
        self.ui_log = chat_list_widget

    def set_ui_time(self, ui):
        self.ui_time = ui

    def set_ui_scores(self, ui):
        self.ui_scores = ui

    def set_ui_teams(self, ui):
        self.ui_teams = ui

    def __update_log(self, records):
        # self.ui_log.clear()
        current_records_amount = self.ui_log.count()
        first_unique_index = len(records) - 1

        if len(records) > current_records_amount:
            for i in range(0, len(records) - current_records_amount):
                new_record = records[first_unique_index + i]
                self.ui_log.addItem(new_record)
                self.ui_log.scrollToBottom()
        elif len(records) < current_records_amount:
            self.ui_log.clear()
            self.ui_log.addItems(records)
            self.ui_log.scrollToBottom()

    def connect(self):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((self.host, self.port))

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while True:
            self.server_socket.sendto('connect'.encode('utf-8'), self.server_addr)
            match_info_bin, server = self.server_socket.recvfrom(self.UDP_MAX_SIZE)
            match_info = pickle.loads(match_info_bin)
            # print('Received confirmation')
            # print(f"Server ip:{str(server[0])}, port: {str(server[1])}")
            if match_info:
                self.match_info = match_info
                self.__update_ui()
                server_addr = server
                break
            else:
                print('Verification failed')
            print('Trying again...')
        self.ui_conn_button.setEnabled(False)

    def __update(self):
        while True:
            time.sleep(1)
            try:
                self.server_socket.sendto('update'.encode('utf-8'), self.server_addr)
            except:
                continue

    def __update_ui(self):
        self.__update_log(self.match_info.log)
        self.ui_scores[0].setText(str(self.match_info.teams[0].score))
        self.ui_scores[1].setText(str(self.match_info.teams[1].score))
        self.ui_teams[0].setText(self.match_info.teams[0].name)
        self.ui_teams[1].setText(self.match_info.teams[1].name)
        self.ui_time.setText(self.match_info.time)

    def listen(self):
        threading.Thread(target=self.__listen, daemon=True).start()
        threading.Thread(target=self.__update, daemon=True).start()

    def close(self):
        try:
            self.client_socket.close()
        except:
            return

    def __listen(self):
        while True:
            match_info_bin, server = self.server_socket.recvfrom(self.UDP_MAX_SIZE)
            match_info = pickle.loads(match_info_bin)
            if match_info:
                self.match_info = match_info
                self.__update_ui()
            else:
                continue

