import Clock
import Register
import Fetch
import Decode
import Execute
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
        self.M = DataMemory.DataMemory()
        self.W = WriteBack.WriteBack()

        self.instn_mem = InstructionMemory.InstructionMemory()


    def printRegisterFile(self):

        for i in range(len(self.RegisterFile)):
            print(self.RegisterFile[i].name, self.RegisterFile[i].getValue())

    def simulate(self, program):
        


        clk = Clock.Clock()

        decodeDict = []
        executeDict = []
        memoryDict = []

        while True:

            #loading program
            self.instn_mem.put_data(program)

            #print("cycle", clk.getCycle(), "PC", self.PC.getValue())
            
            # running Fetch
            fetchList = self.F.fetch(self.instn_mem, self.PC)
            #print("f")
            # self.PC = fetchList[1]
            
            # running Decode
            if (clk.getCycle() > 0):
                #print("d")
                decodeDict = self.D.decode(decode_input, self.RegisterFile)
                
            # running Execute
            if (clk.getCycle() > 1):
                #print("e")
                executeDict = self.X.execute(execute_input)
                
            # running Memory
            if (clk.getCycle() > 2):
                #print("m")
                value = self.M.Memory(memory_input)
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

            clk.setCycle()
            if int(self.PC.getValue(), 2) == 10:
                break


cpu = CPU()

file = open('test_binary.txt', 'r')
program = []
for instn in file:
    program.append(instn[:-1])
print(len(program))
cpu.simulate(program)
# print(cpu.printRegisterFile())