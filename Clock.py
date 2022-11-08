class Clock:
    def __init__(self):
        self.cycle = 0

    def getCycle(self):
        return self.cycle

    def setCycle(self):
        self.cycle += 1