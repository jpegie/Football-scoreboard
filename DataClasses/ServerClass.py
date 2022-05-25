import socket
import pickle
import threading
import time

from PyQt5.QtWidgets import QLabel, QPushButton, QListWidget

from DataClasses.DataClass import MatchInfo
from DataClasses.DataClass import MatchStatus
from DataClasses.DataClass import Team


def first(iterable, default=None):
    for item in iterable:
        return item
    return default


class Server:

    UDP_MAX_SIZE = 65535
    server_socket = socket.socket()
    host = ''
    port = 6969

    viewers = []  # array of tuple[str, int] (ip, port)
    match = MatchInfo()

    ui_scores = []
    ui_time = QLabel
    ui_button_ss = QPushButton
    ui_button_pause = QPushButton
    ui_log = QListWidget
    ui_surnames = []

    def listen(self):
        threading.Thread(target=self.__listen_to_new_viewers).start()
        threading.Thread(target=self.__notify_viewers).start()

    def start_stop_match(self):
        if self.match.status == MatchStatus.NO_MATCH or self.match.status == MatchStatus.STOPPED:
            self.match.start()
            self.ui_button_ss.setText("Stop")
        else:
            self.match.unpause()
            self.match.stop()
            self.ui_button_pause.setText("Pause")
            self.ui_button_ss.setText("Start")

    def pause_match(self):
        if self.match.status == MatchStatus.CONTINUED or self.match.status == MatchStatus.STARTED:
            self.match.pause()
            self.ui_button_pause.setText("Unpause")
        elif self.match.status == MatchStatus.PAUSED:
            self.match.unpause()
            self.ui_button_pause.setText("Pause")

    def set_ui_scores(self, ui):
        self.ui_scores = ui

    def set_ui_time(self, ui):
        self.ui_time = ui
        self.match.set_time_ui(ui)

    def set_ui_ss_button(self, ui):
        self.ui_button_ss = ui

    def set_ui_surnames(self, ui):
        self.ui_surnames = ui

    def set_ui_pause_button(self, ui):
        self.ui_button_pause = ui

    def set_ui_log(self, ui):
        self.ui_log = ui

    def set_score(self, index=0, score=0):
        self.match.set_score(index=index, score=score)
        self.__update_ui_score(index)

    def set_team(self, index=0, name=0):
        self.match.set_team(Team(name=name, score=0), index)

    def set_time(self, minutes, seconds):
        self.match.set_time(minutes, seconds)

    def do_goal(self, index=0):
        self.match.do_goal(index)
        self.__update_ui_score(index)
        self.__add_log_record(f"Goal by player {self.ui_surnames[index].toPlainText()} " +
                              f"of team '{self.match.get_team_name(index)}'")

    def __add_log_record(self, record):
        self.match.add_log_record(record)
        self.ui_log.addItem(record)

    def __update_ui_score(self, index):
        self.ui_scores[index].setText(str(self.match.get_score(index)))

    def __send_message(self, receiver, pickled_data=None):  # receiver = (str, int)
        if pickled_data is None:
            pickled_data = pickle.dumps(self.match)
        self.server_socket.sendto(pickled_data, receiver)

    def __send_to_all(self, viewers):
        pickled_data = pickle.dumps(self.match)
        for v in viewers:
            self.__send_message(v, pickled_data)

    def __notify_viewers(self):
        while True:
            time.sleep(1000)
            buf_viewers = self.viewers.copy()
            self.__send_to_all(buf_viewers)

    def __listen_to_new_viewers(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

        while True:
            message, viewer = self.server_socket.recvfrom(self.UDP_MAX_SIZE)
            if message.decode('utf-8') == 'want to join!':
                if first(x for x in self.viewers if x == viewer) is None:
                    self.viewers.append(viewer)
                self.__send_message(viewer)
