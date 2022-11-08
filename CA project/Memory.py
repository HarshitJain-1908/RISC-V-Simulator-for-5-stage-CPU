class Memory:

    def Memory(self, set, dataMem):
        if set is None:
            return -1

        if (set["instruction"] == "LW"):
            # Load operation
            addr = set["result"]
            return self.Load(addr, dataMem)

        elif (set["instruction"] == "SW"):
            # Store operation
            addr = set["result"]
            data = set["rs1"]
            self.Store(addr, data, dataMem)
            return -1

        else:
            return -1
    
    def Load(self, addr, dataMem): # assuming addr is a string
        # sleep(self.clock_cycle_time * self.delay)
        return dataMem.memory[addr] 
        

    def Store(self, addr, data, dataMem): # for SW instruction
        self.Data_write = data
        dataMem.memory[addr] = self.Data_write
        # sleep(self.clock_cycle_time * self.delay)