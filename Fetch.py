class Fetch:
    currentDelay = 1
    done = False

    def __init__(self, delay):
        self.delay = delay
    
    def fetch(self, InstructionMemory, PC):
        
        if self.currentDelay == self.delay:
            inst = InstructionMemory.read_block(PC)
            old_PC = int(PC.getValue(), 2)
            PC.setValue(format(old_PC + 1 , "032b"))
            self.done = True
            self.currentDelay = 1
            return [inst, old_PC]
        
        else:
            self.done = False
            self.currentDelay += 1 #handling instruction memory delay
            return ["1"*32 , int(PC.getValue(), 2), InstructionMemory.read_block(PC)]
            
    def getDelay(self):
        return self.delay