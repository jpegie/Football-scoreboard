from PyQt5.QtWidgets import QApplication
from DataClasses.ServerAppClass import ServerApp
import sys

def main():

    app = QApplication(sys.argv)

    window = ServerApp()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
