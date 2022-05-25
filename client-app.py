from PyQt5 import QtWidgets
from DataClasses.ClientAppClass import ClientApp
import sys


def main():

    app = QtWidgets.QApplication(sys.argv)
    window = ClientApp()

    window.show()
    window.setup_bindings()

    app.exec_()


if __name__ == '__main__':
    main()
