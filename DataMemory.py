class DataMemory:

    def __init__(self, delay):
        self.memory = {}
        self.Data_write = "0"*32

        for i in range(2**14 + 5):
            addr = format(i, "032b")
            self.memory[addr] = "0"*32              # 4 byte addressable

        self.isRead = False
        self.delay = delay
        
    
    def printMemory(self):
        for key in self.memory.keys():
            print(key, self.memory[key])