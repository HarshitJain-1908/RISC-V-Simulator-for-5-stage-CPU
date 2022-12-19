import Clock
import Register
import Fetch
import Decode
import Execute
import Memory
import WriteBack
import InstructionMemory
import DataMemory
import GraphPlotter

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
        self.isCPUstalled = False
        self.scoreboard = dict()

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
            if (dict[key] == "STORENOC"):
                log.write("STORENOC   store 1 in (0x4004)MMR4")
                break
            if key == "BranchOffset":
                log.write(key + ": " + str(dict[key]) + "    ")
                continue
            if key == "bypassing":
                continue
            if type(dict[key]) != type(True) and dict[key].isdigit() != True:
                if (key=="BranchTaken?"):
                    log.write(key + ": " + dict[key])
                else:
                    log.write(str(dict[key]) + "    ")
            else:
                
                if key == "rd":
                    log.write(key + ": " + dict["_rd"] + "    ")
                else:
                    if key == "rs1":
                        log.write(dict["_rs1"] + ": " + str(int(dict[key], 2)) + "    ")
                        
                    elif key == "rs2":
                        log.write(dict["_rs2"] + ": " + str(int(dict[key], 2)) + "    ")
                        
                    else:
                        log.write(key + ": " + str(int(dict[key], 2)) + "    ")
        log.write("\n")


    def dump(self, log, fetchList, decode_input, decodeDict, execute_input, executeDict, memory_input, memoryDict, writeback_input):
        log.write("\n-------------------------------------------------------------------------------\n")
        log.write("Cycle " + str(self.clk.getCycle()) )
        log.write("\n-------------------------------------------------------------------------------\n")
        # log.write("PC value "+ str(int(self.PC.getValue(), 2)) + "\n")
        if (fetchList[0] == "1"*32):
            if (fetchList[2] != "0"*32):
                log.write("FETCH:     Inst " + str(fetchList[1]) + ": " + fetchList[2] + "\n")
            else:
                log.write("FETCH:     -\n")
        elif (fetchList[0] ==  "0" * 32):
            log.write("FETCH:     -\n")
        else:
            log.write("FETCH:     Inst " + str(fetchList[1]) + ": " + fetchList[0] + "\n")
        
        if decode_input[0] != "0"*32 and decodeDict[0] != None:
            self.log_write(log, "DECODE", str(decode_input[1]), decodeDict[0])
        else:
            log.write("DECODE:    -\n")
        
        if execute_input[0] == None:
            log.write("EXECUTE:   -\n")
        else:
            self.log_write(log, "EXECUTE", str(execute_input[1]), executeDict[0])
        
        if memory_input[0] != None:
            self.log_write(log, "MEMORY", str(memory_input[1]), memoryDict[0])
        else:
            log.write("MEMORY:    -\n")

        if writeback_input[0] != None:
            self.log_write(log, "WRITEBACK", str(writeback_input[1]), writeback_input[0])
        else:
            log.write("WRITEBACK: -\n")
        log.write("\nIs CPU stalled during this cycle? " + str(self.isCPUstalled))
        log.write("\n-------------------------------------------------------------------------------")
        log.write("\nRegister File after cycle " + str(self.clk.getCycle())+ ":\n")
        self.logRegisterFile(log)

    def bypassing(self, decodeDict, executeDict):
        # if executeDict != None:
        #     self.updateScoreboard(executeDict)
        # print("*********************")
        print(self.scoreboard)
        if '_rs1' in decodeDict.keys():
            decodeDict['rs1'] = self.scoreboard[decodeDict['_rs1']][1]
        if '_rs2' in decodeDict.keys():
            decodeDict['rs2'] = self.scoreboard[decodeDict['_rs2']][1]
        # if 'BranchTaken?' in decodeDict.keys() :
        
        #     if decodeDict["rs1"] == decodeDict["rs2"]:
        #         #branch_target should change the PC value to [(current PC) +  Dict["BranchOffset"]]
        #         print("yessssssss")
        #         decodeDict["BranchTaken?"] = "YES"
        #     else:
        #         print("noooooooooo")
        #         decodeDict["BranchTaken?"] = "NO"
        # print("abxdsasda", decodeDict["_rs1"], decodeDict["_rs2"])

    def updateScoreboard(self, executeDict):
        # if (self.clk.getCycle() > 15):
        #     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #     print(executeDict)
        # print("!!!!!!!!!!!!!!!",executeDict)
        if "_rd" in executeDict:
            rd = executeDict["_rd"]
            if rd in self.scoreboard.keys():
                entry = self.scoreboard[rd]
                entry[0] = entry[0] - 1
                entry.append(executeDict["result"])

    def cleanScoreboard(self, reg):
        # print("reg",reg)
        if reg in self.scoreboard.keys() and len(self.scoreboard[reg]) > 1:
            del self.scoreboard[reg]

    def simulate(self, log, instn_mem, data_mem):
        decode_input = [None, None]
        execute_input = [None, None]
        memory_input = [None, None]
        writeback_input = [None, None]
        # input_scoreboard = dict()
        dm_stage_temp = 1
        while True:
            fetchList = self.F.fetch(instn_mem, self.PC)                                          #FETCH STAGE     
            decodeDict = [self.D.decode(self.M.delay, decode_input[0], self.RegisterFile, self.scoreboard), decode_input[1]]     #DECODE STAGE      
            print("-------------------- Cycle", self.clk.getCycle(), "----------------------------------") 
            # print("###############",decodeDict[0])
            executeDict = [self.X.execute(execute_input[0]), execute_input[1]]   #EXECUTE STAGE
            print("&&&&&&&&&&&&&&&&&&&&&&&&")
            print(decodeDict)
            if executeDict[0] != None:
                self.updateScoreboard(executeDict[0])
            # print("good",self.scoreboard)
            if decodeDict[0] != None and decodeDict[0]["bypassing"] == True:
                # print("999999999")
                self.bypassing(decodeDict[0], executeDict[0])
            print("#################", decodeDict)
                        
            # print("------------------------------------------------------") 
            memoryDict = self.M.Memory(memory_input, data_mem)
            if decodeDict[0] != None and decodeDict[0]["bypassing"] == True:
                print("999999999")
                self.bypassing(decodeDict[0], memoryDict[0])                                    #MEMORY STAGE
            self.W.writeback(self.RegisterFile, writeback_input[0])       
            if writeback_input[0] != None:
                if "rd" in writeback_input[0]:
                    self.cleanScoreboard("R"+str(int(writeback_input[0]["rd"], 2)))                            #WRITEBACK STAGE
            print(self.scoreboard)  
            self.dump(log, fetchList, decode_input, decodeDict, execute_input, executeDict, memory_input, memoryDict, writeback_input)
                 
            if memoryDict[0] != None and dm_stage_temp < self.M.delay: #handling data memory delay
                dm_stage_temp = dm_stage_temp + 1
                memory_input = memoryDict
                
                if executeDict[0] is None:
                    execute_input = decodeDict
                    if decodeDict[0] != None and decodeDict[0]["instruction"] == "BEQ" and decodeDict[0]["BranchTaken?"] == "YES": #Handling a taken branch
                        self.PC.setValue(format(int(self.PC.getValue(), 2) + decodeDict[0]["BranchOffset"], "032b"))
                        self.F.currentDelay = 1
                        decode_input[0] = None
                    else: 
                        decode_input = fetchList
                else:
                    execute_input = executeDict
                    if decodeDict[0] == None:
                        decode_input = fetchList
                    else:
                        decode_input = decodeDict
                        self.isCPUstalled = True
                writeback_input = [None, None]
                
                if self.F.currentDelay == 1 and self.isCPUstalled == True:
                    self.PC.setValue(format(int(self.PC.getValue(), 2) - 1, "032b"))
            
            else:
                dm_stage_temp = 1
                self.isCPUstalled = False
            
                if decodeDict[0] != None and decodeDict[0]["instruction"] == "BEQ" and decodeDict[0]["BranchTaken?"] == "YES": #Handling a taken branch
                    self.PC.setValue(format(int(self.PC.getValue(), 2) + decodeDict[0]["BranchOffset"], "032b"))
                    self.F.currentDelay = 1
                    decode_input[0] = None
                else: 
                    decode_input = fetchList

                execute_input = decodeDict
                # input_scoreboard = self.scoreboard.copy()
                memory_input = executeDict 
                writeback_input = memoryDict
            
            
            if ((fetchList[0] == "0"*32 or (fetchList[0] == "1"*32 and fetchList[2] == "0"*32)) 
                and
                (decode_input[0] == "0"*32 or (decode_input[0] == "1"*32 and decode_input[2] == "0"*32))
                and
                execute_input[0] is None and
                memory_input[0] is None and
                writeback_input[0] is None): 
                break

            self.clk.setCycle()



if __name__ == '__main__':
    PROGRAM_BINARY = "test_binary.txt"
    # PROGRAM_BINARY = "temp.txt"
    cpu = CPU()
    
    delay = int(input('Enter Instruction Memory Delay (in clock cyles): '))
    cpu.F.setdelay(delay)
    instn_mem = InstructionMemory.InstructionMemory(delay)

    delay = int(input('Enter Data Memory Delay (in clock cyles): '))
    cpu.M.setDelay(delay)
    data_mem = DataMemory.DataMemory(delay)

    file = open(PROGRAM_BINARY, 'r')
    program = []

    for instn in file:
        if len(instn) == 33:
            program.append(instn[:-1])
        else:
            program.append(instn)

    instn_mem.put_data(program)   #storing program in instruction memory

    log = open('log.txt', "w")
    
    print("\nStarting Simulation...")
    
    log.write("""Instructions:
        \tRegisters are numbered from 0 to 31.
        \trd gives the destination register in an instruction that uses it.
        \tresult field gives the output after the EXECUTE unit executes the given instruction.
        \tFormat of register file printing is <reg_name>: <reg_val_base10>\n""")
                
    log.write("\nRegister File before cycle 0:\n")
    cpu.logRegisterFile(log)
    
    cpu.simulate(log, instn_mem, data_mem)

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
    
    GraphPlotter.plot_num_reg_and_mem_instns(PROGRAM_BINARY)
    GraphPlotter.plot_instruction_and_data_mem_access_pattern("log.txt")
    