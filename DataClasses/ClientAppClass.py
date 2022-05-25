from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sb_client
from DataClasses import ClientClass


class ClientApp(QtWidgets.QMainWindow, sb_client.Ui_Window_Main):
    curr_client = ClientClass.Client()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setup_bindings(self):
        pass
        # self.Button_AddAttach.clicked.connect(self.select_file)
        # self.Button_Send.clicked.connect(lambda: self.curr_client.send(self.TextBox_Message.toPlainText(),
        #                                                                self.TextBox_Receiver.toPlainText()))
        # self.Button_Connect.clicked.connect(lambda: self.curr_client.connect(self.TextBox_Login.toPlainText()))
        # self.Button_Connect.clicked.connect(self.curr_client.listen)
        # self.Button_SetupFolder.clicked.connect(self.setup_folder)




