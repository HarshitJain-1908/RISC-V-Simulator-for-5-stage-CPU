# Instruction memory is 4 byte addressable.

class InstructionMemory:

    def __init__(self):
        self.num_blocks = pow(2, 14) 
        self.memory = ['0' * 32] * self.num_blocks

    def read_block(self, PC):
        # assuming (PC)program_counter is a binary address in string form.
        # returns a string of size 4 bytes
        
        # sleep(self.delay * self.clock_cycle_time)
        return self.memory[int(PC.getValue(), 2)]

    def put_data(self, data): 
        #assuming data is a list of strings, with each string of size 32 bits
        #Call this function to put test_binary's inputs to instruction memory
        
        i = 0
        for d in data:
            self.memory[i] = d
            i = i + 1