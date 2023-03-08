import tkinter


class setIntervalTk:
    def __init__(self, interval: float, action, tkObj: tkinter.Tk):
        self.interval = int(interval * 1000)
        if self.interval <= 0:
            self.interval = 1
        self.action = action
        self.tkObj = tkObj
        self.stopped = True

    def start(self):
        self.stopped = False
        self.tkObj.after(self.interval, self.actionTimer)

    def actionTimer(self):
        if not self.stopped:
            self.action()
            self.tkObj.after(self.interval, self.actionTimer)

    def cancel(self):
        self.stopped = True
