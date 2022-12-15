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

        # Pipeline elements
        self.F = Fetch.Fetch()
        self.D = Decode.Decode()
        self.X = Execute.Execute()
        self.M = Memory.Memory()
        self.W = WriteBack.WriteBack()


    def logRegisterFile(self, log):
        for i in range(len(self.RegisterFile)):
            if (i in [5, 10, 15, 20, 25, 30]):
                log.write("\n")
            reg = "R" + str(int(self.RegisterFile[i].name, 2))
            if (i >=0 and i <= 9):
                log.write("\t\t"+ reg + ":  "+  str(int(self.RegisterFile[i].getValue(), 2)) + "  ")
            else:
                log.write("\t\t"+ reg + ": "+  str(int(self.RegisterFile[i].getValue(), 2)) + "  ")
        log.write("\n")
    
    def log_write(self, log, stage_name, inst_num, dict):
        if dict == None:
            return
        if (stage_name == "DECODE"):
            log.write(stage_name + ":    " + "Inst " + inst_num + ": ")
        if (stage_name == "EXECUTE"):
            log.write(stage_name + ":   " + "Inst " + inst_num + ": ")
        if (stage_name == "MEMORY"):
            log.write(stage_name + ":    " + "Inst " + inst_num + ": ")
        if (stage_name == "WRITEBACK"):
            log.write(stage_name + ": " + "Inst " + inst_num + ": ")
        for key in dict:
            if key in  ["_rd", "_rs1", "_rs2"]:
                continue
            if dict[key].isdigit() != True:
                if (key=="BranchTaken?"):
                    log.write(key + ": " + dict[key])
                else:
                    log.write(str(dict[key]) + "    ")
            else:
                
                if key == "rd":
                    log.write(key + ": " + dict["_rd"] + "    ")
                    
                    #log.write("rd_num: " + dict[key] + "    ")
                else:
                    if key == "rs1":
                        log.write(dict["_rs1"] + ": " + str(int(dict[key], 2)) + "    ")
                        
                    elif key == "rs2":
                        log.write(dict["_rs2"] + ": " + str(int(dict[key], 2)) + "    ")
                        
                    else:
                        log.write(key + ": " + str(int(dict[key], 2)) + "    ")
        log.write("\n")
    
    def simulate(self, program, log, instn_mem, data_mem):
        log.write("""General Instructions:
        \tAll register values are given in integers in base 10.
        \tRegisters are numbered from 0 to 31.
        \trd gives the destination register in an instruction that uses it.
        \tresult field gives the output after the EXECUTE unit executes the given instruction.""")
        decodeDict = []
        executeDict = []
        memoryDict = []

        #storing program in instruction memory
        instn_mem.put_data(program)
        bto = 0 #This will eventually store the cumulative sum of all branch target offsets in the program
        while True:
            log.write("\n-------------------------------------------------------------------------------\n")
            log.write("Cycle = " + str(self.clk.getCycle()) )
            log.write("\n-------------------------------------------------------------------------------\n")

            # Fetch
            fetchList = self.F.fetch(instn_mem, self.PC)

            if (int(fetchList[0], 2) == 0):
                fetchList = None
                log.write("FETCH:     -\n")
            else:
                log.write("FETCH:     Inst " + str(fetchList[1]) + ": " + fetchList[0] + "\n")
            
            # Decode
            if (self.clk.getCycle() > 0 and decode_input != None):
                decodeDict = self.D.decode(decode_input[0], self.RegisterFile)
                decodeDict = [decodeDict, decode_input[1]]
                self.log_write(log, "DECODE", str(decode_input[1]), decodeDict[0])
                if decodeDict[0]["instruction"] == "BEQ" and decodeDict[0]["BranchTaken?"] == "YES":
                    self.PC.setValue(format(int(self.PC.getValue(), 2) + int(decodeDict[0]["BranchOffset"], 2), "032b"))
                    bto = bto + int(decodeDict[0]["BranchOffset"], 2)
            else:
                decodeDict = None
                log.write("DECODE:    -\n")
                
            # Execute
            if (self.clk.getCycle() > 1 and execute_input != None):
                executeDict = self.X.execute(execute_input[0])
                executeDict = [executeDict, execute_input[1]]
                self.log_write(log, "EXECUTE", str(execute_input[1]), executeDict[0])
            else:
                executeDict = None
                log.write("EXECUTE:   -\n")
                
            # Memory
            if (self.clk.getCycle() > 2 and memory_input != None):
                value = self.M.Memory(memory_input[0], data_mem)
                memoryDict = memory_input
                
                if (value != -1):
                    memoryDict[0]["memValue"] = value
                self.log_write(log, "MEMORY", str(memory_input[1]), memoryDict[0])
            else:
                memoryDict = None
                log.write("MEMORY:    -\n")

            # Writeback
            if (self.clk.getCycle() > 3 and writeback_input != None):
                self.W.writeback(self.RegisterFile, writeback_input[0])
                self.log_write(log, "WRITEBACK", str(writeback_input[1]), writeback_input[0])
            else:
                log.write("WRITEBACK: -\n")
            
            if (self.clk.getCycle() < len(program)):
                if decodeDict != None and decodeDict[0]["instruction"] == "BEQ" and decodeDict[0]["BranchTaken?"] == "YES":
                    decode_input = None
                else:
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

            if self.clk.getCycle() + 1 == (4 + len(program) - bto):
                break
            
            log.write("\nRegister File printed below. Format <reg_name>: <reg_val_decimal>\n")
            self.logRegisterFile(log)

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
    log.write("\n---------------------------------------------------------------------------"+
    "\nProgram execution completed in " + str(cpu.clk.getCycle()+1) + 
    " cycles.\n---------------------------------------------------------------------------")
    log.write("\nMemory state after the execution of program; Format <mem_addr_base16>: <mem_val_base10>\n")
    log.write("---------------------------------------------------------------------------\n")

    for i in range(0, len(data_mem.memory)):
        if (i % 5 == 0):
            log.write("\n")
        log.write("\t\t"+ hex(i) + ": " + str(int(data_mem.memory[format(i, "032b")], 2)) + "\t")

    print("\nSimulation successful.\nLog file generated: log.txt.")
    log.close()