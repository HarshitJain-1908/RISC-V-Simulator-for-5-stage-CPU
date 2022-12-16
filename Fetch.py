class Fetch:
    currentDelay = 1
     
    def setdelay(self, delay):
        self.delay = delay
    
    def fetch(self, InstructionMemory, PC):
        if self.currentDelay == self.delay:
            inst = InstructionMemory.read_block(PC)
            old_PC = int(PC.getValue(), 2)
            PC.setValue(format(old_PC + 1 , "032b"))
            self.currentDelay = 1
            return [inst, old_PC]
        
        else:
            self.currentDelay += 1
            return ["0"*32,int(PC.getValue(), 2)]
        