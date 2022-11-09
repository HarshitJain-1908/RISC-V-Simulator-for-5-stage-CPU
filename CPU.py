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

        self.clk = Clock.Clock()

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


    def logRegisterFile(self, log):
        for i in range(len(self.RegisterFile)):
            reg = "R" + str(int(self.RegisterFile[i].name, 2))
            log.write("\t\t"+ reg + ": "+  str(int(self.RegisterFile[i].getValue(), 2)) + "\n")
        log.write("\n")
    
    def log_write(self, log, stage_name, inst_num, dict):
        if dict == None:
            return
        log.write(stage_name + ": " + "Inst " + inst_num + ": ")
        for key in dict:
            if dict[key].isdigit() != True:
                log.write(str(dict[key]) + "    ")
            else:
                if key == "rd":
                    log.write("rd_num: " + dict[key] + "    ")
                else:
                    log.write(key + ": " + str(int(dict[key], 2)) + "    ")
        log.write("\n")
    
    def simulate(self, program, log, instn_mem, data_mem):
        log.write("""General Instructions:
        \tAll register values are given in integers in base 10.
        \tRegisters are numbered from 0 to 31.
        \trd_num gives the destination register number in an instruction that uses it.
        \tresult field gives the output after the EXECUTE unit executes the given instruction.""")
        decodeDict = []
        executeDict = []
        memoryDict = []

        #storing program in instruction memory
        instn_mem.put_data(program)

        while True:
            log.write("\n---------------------------------------------------------------------------\n")
            log.write("Cycle = " + str(self.clk.getCycle()) )
            log.write("\n---------------------------------------------------------------------------\n")

            # running Fetch
            fetchList = self.F.fetch(instn_mem, self.PC)
            if (int(fetchList[0], 2) == 0):
                fetchList = None
                log.write("FETCH:     -\n")
            else:
                log.write("FETCH: Inst " + str(fetchList[1]) + ": " + fetchList[0] + "\n")
            
            # running Decode
            if (self.clk.getCycle() > 0 and decode_input != None):
                # log.write(str(decode_input))
                decodeDict = self.D.decode(decode_input[0], self.RegisterFile)
                decodeDict = [decodeDict, decode_input[1]]
                # log.write("decode" + str(decodeDict))
                self.log_write(log, "DECODE", str(decode_input[1]), decodeDict[0])
            else:
                log.write("DECODE:    -\n")
                
            # running Execute
            if (self.clk.getCycle() > 1 and execute_input != None):
                executeDict = self.X.execute(execute_input[0])
                executeDict = [executeDict, execute_input[1]]
                self.log_write(log, "EXECUTE", str(execute_input[1]), executeDict[0])
            else:
                log.write("EXECUTE:   -\n")
                
            # running Memory
            if (self.clk.getCycle() > 2 and memory_input != None):
                value = self.M.Memory(memory_input[0], data_mem)
                memoryDict = memory_input
                if (value != -1):
                    memoryDict[0]["memValue"] = value
                self.log_write(log, "MEMORY", str(memory_input[1]), memoryDict[0])
            else:
                log.write("MEMORY:    -\n")

            # running Writeback
            if (self.clk.getCycle() > 3 and writeback_input != None):
                self.W.writeback(self.RegisterFile, writeback_input[0])
                log.write("WRITEBACK: Inst " + str(writeback_input[1]) + ": (Register File printed below. Format <reg_num_base2> <reg_val_base10>)\n")
                self.logRegisterFile(log)
            else:
                log.write("WRITEBACK: -\n")
            
            if (self.clk.getCycle() < len(program)):
                decode_input = fetchList
            else:
                decode_input = None
            
            if (self.clk.getCycle() < len(program) + 1):
                execute_input = decodeDict
            else:
                execute_input = None
            
            if (self.clk.getCycle() < len(program) + 2):
                memory_input = executeDict
            else:
                memory_input = None

            if (self.clk.getCycle() < len(program) + 3):
                writeback_input = memoryDict
            else:
                writeback_input = None

            if self.clk.getCycle()+1 == (4+len(program)):
                break

            self.clk.setCycle()


if __name__ == '__main__':

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

    log = open('log.txt', "w")
    print("\nStarting Simulation...")
    cpu.simulate(program, log, instn_mem, data_mem)
    log.write("\nProgram execution completed\n---------------------------------------------------------------------------")
    log.write("\nMemory state after the execution of program; Format <mem_addr_base2>\t<mem_val_base10>\n")
    log.write("---------------------------------------------------------------------------\n")
    for i in range(0, len(data_mem.memory)):
        addr = format(i, "032b")
        log.write("\t\t"+addr[-15: ] + "\t" + str(int(data_mem.memory[addr], 2)) + "\n")

    print("\nSimulation successful.\nLog file generated: log.txt.")
    log.close()
