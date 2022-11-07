class DataMemory:

    def __init__(self):
        self.memory = {}
        self.Data_write = "0"*32

        for i in range(2**14):
            addr = format(i, "016b")
            self.memory[addr] = "0"*32              # 4 byte addressable

        self.isRead = False

        print('Enter Data Memory Delay (in clock cyles): ')
        self.clock_cycle_time = 0.5                 # in seconds. Value must be taken from Clock class
        # input(self.delay)
        
    def Memory(self, set):

        if (set["instruction"] == "LW"):
            # Load operation
            addr = set["result"]
            return self.Load(addr)

        elif (set["instruction"] == "SW"):
            # Store operation
            addr = set["result"]
            data = set["rs1"]
            self.Store(addr, data)
            return -1

        else:
            return -1
    
    def Load(self, addr): # assuming addr is a string
        # sleep(self.clock_cycle_time * self.delay)
        return self.memory[addr] 
        

    def Store(self, addr, data): # for SW instruction
        self.Data_write = data
        self.memory[addr] = self.Data_write
        # sleep(self.clock_cycle_time * self.delay)

    def printMemory(self):
        for key in self.memory.keys():
            print(key, self.memory[key])