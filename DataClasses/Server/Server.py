import socket
import pickle
import threading

from PyQt5.QtWidgets import QLabel, QPushButton, QListWidget

from DataClasses.Common.Match import MatchInfo
from DataClasses.Common.Match import MatchStatus
from DataClasses.Common.Match import Team
from DataClasses.Common.Match import SlimMatchInfo


def first(iterable, default=None):
    for item in iterable:
        return item
    return default


UDP_MAX_SIZE = 1024  # 65535


class Server:

    server_socket = socket.socket()
    host = ''
    port = 6565

    viewers = []  # array of tuple[str, int] (ip, port)
    match = MatchInfo()

    ui_scores = []
    ui_time = QLabel
    ui_button_ss = QPushButton
    ui_button_pause = QPushButton
    ui_log = QListWidget
    ui_surnames = []

    def __init__(self):
        self.start_listening()

    def close(self):
        try:
            self.server_socket.close()
        except:
            return

    def start_listening(self):
        threading.Thread(target=self.__listen, daemon=True).start()
        # threading.Thread(target=self.__notify_viewers).start()

    def start_stop_match(self):
        if self.match.status == MatchStatus.NO_MATCH or self.match.status == MatchStatus.STOPPED:
            self.match.start()
            self.ui_button_ss.setText("Stop")
            self.__add_log_record("Match started!")
        else:
            self.match.unpause()
            self.match.stop()
            self.ui_button_pause.setText("Pause")
            self.ui_button_ss.setText("Start")
            self.__add_log_record("Match stopped!")

    def pause_match(self):
        if self.match.status == MatchStatus.CONTINUED or self.match.status == MatchStatus.STARTED:
            self.match.pause()
            self.ui_button_pause.setText("Unpause")
            self.__add_log_record("Match paused!")
        elif self.match.status == MatchStatus.PAUSED:
            self.match.unpause()
            self.ui_button_pause.setText("Pause")
            self.__add_log_record("Match unpaused!")

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
        self.match.do_goal(index, self.ui_surnames[index].toPlainText())
        self.__update_ui_score(index)
        self.__add_log_record(f"Goal by player {self.ui_surnames[index].toPlainText()} " +
                              f"of team '{self.match.get_team_name(index)}'")

    def __add_log_record(self, record):
        self.ui_log.addItem(f"🌈 {record}")
        self.ui_log.scrollToBottom()

    def __update_ui_score(self, index):
        self.ui_scores[index].setText(str(self.match.get_score(index)))

    def __get_slim(self):
        slim_info = SlimMatchInfo()
        slim_info.log = self.match.log
        slim_info.time = self.match.current_time
        slim_info.teams = self.match.teams
        return slim_info

    def __send_message(self, receiver, pickled_data=None):  # receiver = (str, int)
        if pickled_data is None:
            pickled_data = pickle.dumps(self.__get_slim())
        self.server_socket.sendto(pickled_data, receiver)

    def __send_to_all(self, viewers):
        pickled_data = pickle.dumps(self.__get_slim())
        for v in viewers:
            self.__send_message(v, pickled_data)

    def __listen(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))

        while True:
            message, viewer = self.server_socket.recvfrom(UDP_MAX_SIZE)
            decoded_message = message.decode('utf-8')

            if decoded_message == 'connect':
                if first(x for x in self.viewers if x == viewer) is None:
                    self.viewers.append(viewer)
                self.__send_message(viewer)
            elif decoded_message == 'update':
                self.__send_message(viewer)
