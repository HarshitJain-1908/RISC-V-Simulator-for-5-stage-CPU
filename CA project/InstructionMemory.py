# Instruction memory is 4 byte addressable.

class InstructionMemory:

    def __init__(self, delay):

        self.num_blocks = pow(2, 14) 
        self.memory = ['0' * 32] * self.num_blocks
        self.delay = delay

    def put_data(self, data): 
        #assuming data is a list of strings, with each string of size 32 bits
        #Call this function to put test_binary's inputs to instruction memory
        
        i = 0
        for d in data:
            self.memory[i] = d
            i = i + 1