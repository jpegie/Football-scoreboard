from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
import sb_client
from DataClasses import ClientClass


class ClientApp(QtWidgets.QMainWindow, sb_client.Ui_MainWindow):
    curr_client = ClientClass.Client()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_bindings()
        self.curr_client.listen()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.curr_client.close()
        a0.accept()

    def setup_bindings(self):
        self.curr_client.set_chat(self.List_Log)
        self.curr_client.set_connect_button(self.Button_Connect)
        self.curr_client.set_ui_scores([self.Label_Score1, self.Label_Score2])
        self.curr_client.set_ui_time(self.Label_Time)
        self.curr_client.set_ui_teams([self.Label_Team1, self.Label_Team2])
        self.Button_Connect.clicked.connect(self.curr_client.connect)

        # self.Button_AddAttach.clicked.connect(self.select_file)
        # self.Button_Send.clicked.connect(lambda: self.curr_client.send(self.TextBox_Message.toPlainText(),
        #                                                                self.TextBox_Receiver.toPlainText()))
        # self.Button_Connect.clicked.connect(lambda: self.curr_client.connect(self.TextBox_Login.toPlainText()))
        # self.Button_Connect.clicked.connect(self.curr_client.listen)
        # self.Button_SetupFolder.clicked.connect(self.setup_folder)




