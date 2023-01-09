class Memory:

    operations = ["LW", "LOADNOC", "SW", "STORENOC"]

    def __init__(self, delay):
        self.delay = delay
     
    def Memory(self, set, dataMem):
        if set[0] is None:
            return [None, None]

        memoryDict = set.copy()
        if (set[0]["instruction"] == "LW"):
            # Load operation
            addr = set[0]["result"]
            if "delay" not in memoryDict[0]:
                memoryDict[0]["delay"] = 1
            else:
                memoryDict[0]["delay"] += 1
            memoryDict[0]["memValue"] = self.Load(addr, dataMem, memoryDict)
            return memoryDict

        if (set[0]["instruction"] == "LOADNOC"):
            if set[0]["result"] == "invalid":
                return memoryDict
            addr = set[0]["result"]
            data = set[0]["rs2"]
            self.Store(addr, data, dataMem)
            return memoryDict

        elif (set[0]["instruction"] == "SW" or set[0]["instruction"] == "STORENOC"):
            # Store operation
            addr = set[0]["result"]
            data = set[0]["rs2"]
            self.Store(addr, data, dataMem)
            return memoryDict

        else:
            return memoryDict
    
    def getDelay(self):
        return self.delay

    def Load(self, addr, dataMem, memoryDict): # assuming addr is a string
        if memoryDict[0]["delay"] == self.delay:
            return dataMem.memory[addr]
        else:
            return "0" 

    def Store(self, addr, data, dataMem): # for SW instruction
        self.Data_write = data
        dataMem.memory[addr] = self.Data_write

    def setDelay(self,delay):
        self.delay = delay