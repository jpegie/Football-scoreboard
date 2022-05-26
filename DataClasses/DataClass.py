import datetime
from enum import Enum
from DataClasses.StopwatchClass import Stopwatch


class MatchStatus(Enum):
    STARTED = 1
    PAUSED = 2
    CONTINUED = 3
    STOPPED = 4
    NO_MATCH = -1


class Team:
    name = ''
    score = 0

    def __init__(self, name='', score=0):
        self.name = name
        self.score = score


class MatchInfo:
    __status = MatchStatus.NO_MATCH
    __teams = []
    __match_time = Stopwatch()
    __log = []
    __viewers = 0

    def __init__(self, teams=None, match_time=None, log=None, viewers=0, status=MatchStatus.NO_MATCH):
        if (teams is not None) and (match_time is not None) and (log is None) and (status is not MatchStatus.NO_MATCH):
            self.__teams = teams
            self.__match_time = match_time
            self.__log = log
            self.__viewers = viewers
            self.__status = status
        else:
            self.__teams.append(Team())
            self.__teams.append(Team())

    @property
    def status(self):
        return self.__status

    @property
    def log(self):
        return self.__log

    @property
    def current_time(self):
        return self.__match_time.get_elapsed_as_str()

    @property
    def teams(self):
        return self.__teams

    def get_score(self, index=0):
        return self.__teams[index].score

    def get_team_name(self, index=0):
        return self.__teams[index].name

    def start(self):
        self.__status = MatchStatus.STARTED
        self.__match_time.start()
        self.add_log_record("Match started!")

    def pause(self):
        self.__status = MatchStatus.PAUSED
        self.__match_time.pause()
        self.add_log_record("Match paused!")

    def unpause(self):
        self.__status = MatchStatus.STARTED
        self.__match_time.unpause()
        self.add_log_record("Match unpaused!")

    def stop(self):
        self.__status = MatchStatus.STOPPED
        self.__match_time.stop()
        self.add_log_record("Match stopped!")

    def update_viewers(self, value):
        self.__viewers = value

    def update_status(self, status):
        self.__status = status

    def update_time(self, time):
        self.__match_time = time

    def set_time(self, minutes, seconds):
        self.__match_time.set_time(minutes, seconds)

    def set_team(self, team, index=0):
        self.__teams[index] = team

    def set_team_name(self, index=0, name=''):
        self.__teams[index].name = name

    def set_score(self, score=0, index=0):
        self.__teams[index].score = score

    def do_goal(self, index=0, player=""):
        self.__teams[index].score = self.__teams[index].score + 1
        self.add_log_record(f"Goal by {player} of team {self.get_team_name(index)}")

    def add_log_record(self, record):
        self.__log.append(f"🌈 {record}")

    def set_time_ui(self, ui):
        self.__match_time.set_ui(ui)
