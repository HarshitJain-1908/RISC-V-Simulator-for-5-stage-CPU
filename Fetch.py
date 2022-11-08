class Fetch:     
    
    def fetch(self, InstructionMemory, PC):

        inst = InstructionMemory.read_block(PC)
        old_PC = int(PC.getValue(), 2)
        PC.setValue(format(old_PC + 1 , "032b"))
        return [inst, old_PC]