# Instruction memory is 4 byte addressable.

class InstructionMemory:

    def __init__(self):
        self.num_blocks = pow(2, 16) 
        self.memory = ['0' * 32] * self.num_blocks
        print('Enter Instruction Memory Delay (in clock cyles): ')
        self.clock_cycle_time = 0.5  # in seconds. Value must be taken from Clock class
        # input(self.delay)

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