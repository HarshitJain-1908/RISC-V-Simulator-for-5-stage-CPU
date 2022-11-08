class Fetch:     
    
    def fetch(self, InstructionMemory, PC):
        # assuming (PC)program_counter is a binary address in string form.
        # returns a string of size 4 bytes

        inst = InstructionMemory.memory[int(PC.getValue(), 2)]
        old_PC = int(PC.getValue(), 2)
        PC.setValue(format(old_PC + 1 , "032b"))

        return [inst, PC]
