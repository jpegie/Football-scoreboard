from PyQt5 import QtWidgets, QtGui
from Ui.Py import sb_client
from DataClasses.Client import Client


class ClientApp(QtWidgets.QMainWindow, sb_client.Ui_MainWindow):
    curr_client = Client.Client()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_bindings()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.curr_client.close()
        a0.accept()

    def setup_bindings(self):
        self.curr_client.set_ui_log(self.List_Log)
        self.curr_client.set_ui_connect_button(self.Button_Connect)
        self.curr_client.set_ui_scores([self.Label_Score1, self.Label_Score2])
        self.curr_client.set_ui_time(self.Label_Time)
        self.curr_client.set_ui_teams([self.Label_Team1, self.Label_Team2])
        self.Button_Connect.clicked.connect(self.curr_client.connect)
