import Clock
import Register
import Fetch
import Decode
import Execute
import Memory
import WriteBack
import InstructionMemory
import DataMemory

class CPU:
    
    def __init__(self):

        self.RegisterFile = []
        
        for i in range(32):
            name = format(i, '05b')       
            r = Register.Register(name, "0"*32)
            self.RegisterFile.append(r)

        self.PC = Register.Register("100000", "0"*32)

        self.data_read = "0"*32
        self.data_write = "0"*32
        self.addr_read = "0"*32
        self.data_write = "0"*32

        # Pipeline elements
        self.F = Fetch.Fetch()
        self.D = Decode.Decode()
        self.X = Execute.Execute()
        self.M = Memory.Memory()
        self.W = WriteBack.WriteBack()


    def printRegisterFile(self):

        for i in range(len(self.RegisterFile)):
            print(self.RegisterFile[i].name, self.RegisterFile[i].getValue())

    def simulate(self, program, instn_mem, data_mem):
        


        clk = Clock.Clock()

        decodeDict = []
        executeDict = []
        memoryDict = []

        while True:

            #print("cycle", clk.getCycle(), "PC", self.PC.getValue())
            
            # running Fetch
            fetchList = self.F.fetch(instn_mem, self.PC)
            #print("f")
            # self.PC = fetchList[1]
            
            # running Decode
            if (clk.getCycle() > 0):
                #print("d")
                # print("R1", self.RegisterFile[1].getValue())
                # print("R2", self.RegisterFile[2].getValue())
                decodeDict = self.D.decode(decode_input, self.RegisterFile)
                # print("decode dict", decodeDict)
                
            # running Execute
            if (clk.getCycle() > 1):
                #print("e")
                executeDict = self.X.execute(execute_input)
                print("exec dic", executeDict)
                
            # running Memory
            if (clk.getCycle() > 2):
                #print("m")
                value = self.M.Memory(memory_input, data_mem)
                memoryDict = memory_input
                if (value != -1):
                    memoryDict["memValue"] = value

            # running Writeback
            if (clk.getCycle() > 3):
                #print("w")
                self.W.writeback(self.RegisterFile, writeback_input)

            decode_input = fetchList[0]
            execute_input = decodeDict
            memory_input = executeDict
            writeback_input = memoryDict

            if clk.getCycle()+1 == (4+len(program)):
                break

            clk.setCycle()


cpu = CPU()
delay = int(input('Enter Instruction Memory Delay (in clock cyles): '))
instn_mem = InstructionMemory.InstructionMemory(delay)
delay = int(input('Enter Data Memory Delay (in clock cyles): '))
data_mem = DataMemory.DataMemory(delay)

file = open('test_binary.txt', 'r')
program = []

for instn in file:
    if len(instn) == 33:
        program.append(instn[:-1])
    else:
        program.append(instn)

#loading program
instn_mem.put_data(program)

cpu.simulate(program, instn_mem, data_mem)
print(cpu.printRegisterFile())
print("memory", data_mem.memory[format(15, "032b")])