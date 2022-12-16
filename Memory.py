class Memory:
    operations = ["LW", "LOADNOC", "SW", "STORENOC"]
    currDelay = 1
    def Memory(self, set, dataMem):
        if set is None:
            return -1

        # if (set["instruction"] in self.operations):
        #     if self.currDelay == self.delay :

        if (set["instruction"] == "LW"):
            # Load operation
            addr = set["result"]
            return self.Load(addr, dataMem)

        if (set["instruction"] == "LOADNOC"):
            if set["result"] == "invalid":
                return -1
            addr = set["result"]
            data = set["rs2"]
            self.Store(addr, data, dataMem)
            return -1 

        elif (set["instruction"] == "SW" or set["instruction"] == "STORENOC"):
            # Store operation
            addr = set["result"]
            data = set["rs2"]
            self.Store(addr, data, dataMem)
            return -1
            # else:
            #     self.currDelay += 1
            #     return -1

        else:
            return -1
    
    def Load(self, addr, dataMem): # assuming addr is a string
        return dataMem.memory[addr] 
        

    def Store(self, addr, data, dataMem): # for SW instruction
        self.Data_write = data
        dataMem.memory[addr] = self.Data_write

    def setDelay(self,delay):
        self.delay = delay
