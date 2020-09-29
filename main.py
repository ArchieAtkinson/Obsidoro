import getopt
import os
import sys
import time
from enum import Enum

interval_max = 4

vault_path = ''

class activity:

    def __init__(self, duration, state):
        self.duration = 60 * duration
        self.state = state


class Tracking:

    def __init__(self, now, start, duration, state, interval):
        self.now = now
        self.start = start
        self.duration = duration
        self.state = state
        self.interval = interval

    def __str__(self):
        return str(self)


class status(Enum):
    work_state = 1
    short_break_state = 2
    long_break_state = 3


def main(argv):

    global vault_path
    print(os.path.exists(argv[1]))
    if os.path.exists(argv[1]):
        vault_path = argv[1]
    else:
        print("py main.py <vault path>")
        exit()

    work = activity(25, status.work_state)

    short_break = activity(5, status.short_break_state)

    long_break = activity(15, status.long_break_state)

    Pomo = Tracking(work.duration, work.duration, work.duration, work.state, 0)

    DisplayTimer(Pomo, 'x')

    PauseManager()

    while True:

        while Pomo.now != 0:

            PauseManager()

            DisplayTimer(Pomo, ' ')

            Pomo.now -= 1

            time.sleep(1)

        if Pomo.state == status.work_state:
            Pomo.interval += 1

        if Pomo.state != status.work_state:
            ConfigNewInterval(work, Pomo)

        elif Pomo.interval < interval_max and Pomo.state == status.work_state:
            ConfigNewInterval(short_break, Pomo)

        elif Pomo.interval == interval_max and Pomo.state == status.work_state:

            ConfigNewInterval(long_break, Pomo)
            Pomo.interval = 0

        DisplayTimer(Pomo)

        while True:
            lines = ReadFileLines()
            if len(lines) == 0 or lines[3] == ' - [ ] -- Start/Pause':
                break


def ConfigNewInterval(activity, Pomo):
    Pomo.state = activity.state

    Pomo.start = activity.duration
    Pomo.now = activity.duration


def GetStateString(state):
    if state == status.work_state:
        return 'Work'
    if state == status.short_break_state:
        return 'Short Break'
    if state == status.long_break_state:
        return 'Long Break'


def SecsToPrettyString(time):
    mins, secs = divmod(time, 60)
    return '{:02d}:{:02d}'.format(mins, secs)


def ReadFileLines():
    while True:
        try:
            file = open(vault_path+"\\Obsidoro.md", 'r', encoding="utf-8")
            break
        except:
            pass

    lines = file.readlines()

    file.close()

    return lines


def WriteFile(data):
    while True:
        try:
            file = open(vault_path+"\\Obsidoro.md", 'w', encoding="utf-8")
            break
        except:
            pass

    file.write(data)

    file.close()


def PauseManager():
    lines = ReadFileLines()

    if len(lines) == 0 or lines[3] == ' - [x] -- Start/Pause':

        while True:

            lines = ReadFileLines()

            if len(lines) == 0 or lines[3] == ' - [ ] -- Start/Pause':
                break


def DisplayTimer(Pomo, tickbox):

    table = '|Status| Total Time| Time Left| Intervals|\n' \
            '|:-:|:-:|:-:|:-:|\n' \
            '|{}|{}|{}|{}|\n'.format(GetStateString(Pomo.state),
                                     SecsToPrettyString(Pomo.start),
                                     SecsToPrettyString(Pomo.now), Pomo.interval)

    start_button = ' - [{}] -- Start/Pause'.format(tickbox)

    new_file_data = table + start_button

    WriteFile(new_file_data)


if __name__ == '__main__':
    main(sys.argv)
