import threading
import time as t
from PyQt5.QtWidgets import QLabel


class Stopwatch:

    __ui = QLabel
    __stopped = False
    __paused = False
    __time_elapsed = [0, 0]
    __time_set = False

    def set_ui(self, ui):
        self.__ui = ui

    def set_time(self, minutes, seconds):
        self.__time_set = True
        self.__time_elapsed[0] = minutes
        self.__time_elapsed[1] = seconds
        self.__update_ui()

    def start(self):
        self.__stopped = False
        threading.Thread(target=self.__start).start()

    def stop(self):
        self.__stopped = True

    def pause(self):
        self.__paused = True

    def unpause(self):
        self.__paused = False

    def get_elapsed(self):
        return self.__time_elapsed

    def get_elapsed_as_str(self):
        seconds = str(self.__time_elapsed[1])
        minutes = str(self.__time_elapsed[0])
        if len(seconds) < 2:
            seconds = f"0{seconds}"
        if len(minutes) < 2:
            minutes = f"0{minutes}"
        return f"{minutes}:{seconds}"

    def __start(self):
        total_seconds = 0
        if self.__time_set is True:
            total_seconds = self.__time_elapsed[0]*60 + self.__time_elapsed[1]
            self.__time_set = False
        else:
            self.__time_elapsed[0] = 0
            self.__time_elapsed[1] = 0
            self.__update_ui()
            t.sleep(1)

        while not self.__stopped:
            if not self.__paused:
                total_seconds = total_seconds + 1
                self.__time_elapsed[0] = int(total_seconds/60)
                self.__time_elapsed[1] = total_seconds - (self.__time_elapsed[0]*60)
                self.__update_ui()
                t.sleep(1)

    def __update_ui(self):
        time_str = self.get_elapsed_as_str()
        self.__ui.setText(time_str)
