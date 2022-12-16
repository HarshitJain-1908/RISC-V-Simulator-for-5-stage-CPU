class Memory:
    operations = ["LW", "LOADNOC", "SW", "STORENOC"]
    currDelay = 1
    def Memory(self, set, dataMem):
        if set[0] is None:
            return [None, None]

        # if (set["instruction"] in self.operations):
        #     if self.currDelay == self.delay :
        memoryDict = set.copy()
        if (set[0]["instruction"] == "LW"):
            # Load operation
            addr = set[0]["result"]
            memoryDict[0]["memValue"] = self.Load(addr, dataMem)
            #return self.Load(addr, dataMem)
            return memoryDict

        if (set[0]["instruction"] == "LOADNOC"):
            if set[0]["result"] == "invalid":
                return memoryDict
            addr = set[0]["result"]
            data = set[0]["rs2"]
            self.Store(addr, data, dataMem)
            #return -1
            return memoryDict

        elif (set[0]["instruction"] == "SW" or set[0]["instruction"] == "STORENOC"):
            # Store operation
            addr = set[0]["result"]
            data = set[0]["rs2"]
            self.Store(addr, data, dataMem)
            #return -1
            return memoryDict
            # else:
            #     self.currDelay += 1
            #     return -1

        else:
            #return -1
            return memoryDict
    
    def Load(self, addr, dataMem): # assuming addr is a string
        return dataMem.memory[addr] 
        

    def Store(self, addr, data, dataMem): # for SW instruction
        self.Data_write = data
        dataMem.memory[addr] = self.Data_write

    def setDelay(self,delay):
        self.delay = delay
