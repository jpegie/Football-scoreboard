from PyQt5.QtWidgets import QMainWindow

import sb_server
from DataClasses import ServerClass


class ServerApp(QMainWindow, sb_server.Ui_MainWindow):
    curr_server = ServerClass.Server()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_bindings()

    def setup_bindings(self):
        self.Button_Start.clicked.connect(self.curr_server.start_stop_match)
        self.Button_Pause.clicked.connect(self.curr_server.pause_match)
        self.Button_SetScore1.clicked.connect(lambda: self.curr_server.set_score(0, int(self.SpinBox_Score1.value())))
        self.Button_SetScore2.clicked.connect(lambda: self.curr_server.set_score(1, int(self.SpinBox_Score2.value())))
        self.Button_Goal1.clicked.connect(lambda: self.curr_server.do_goal(0))
        self.Button_Goal2.clicked.connect(lambda: self.curr_server.do_goal(1))
        self.Button_SetTeam1.clicked.connect(lambda: self.curr_server.set_team(0, self.TextBox_Team1.toPlainText()))
        self.Button_SetTeam2.clicked.connect(lambda: self.curr_server.set_team(1, self.TextBox_Team2.toPlainText()))
        self.Button_SetTime.clicked.connect(lambda: self.curr_server.set_time(self.TimeEdit.time().minute(),
                                                                              self.TimeEdit.time().second()))
        self.curr_server.set_ui_scores([self.Label_Score1, self.Label_Score2])
        self.curr_server.set_ui_time(self.Label_Time)
        self.curr_server.set_ui_ss_button(self.Button_Start)
        self.curr_server.set_ui_pause_button(self.Button_Pause)
        self.curr_server.set_ui_log(self.List_Log)
        self.curr_server.set_ui_surnames([self.TextBox_WhoGoaled1, self.TextBox_WhoGoaled2])





