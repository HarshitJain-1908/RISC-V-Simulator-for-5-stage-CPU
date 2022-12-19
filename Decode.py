# Runs in the second half of the clock cycle. Must be triggered only after the first half of the clock cycle
# Decode the instruction and read the registers corresponding to register
# source specifiers from the register file. Do the equality test on the 
# registers as they are read, for a possible branch.
# The decoded instruction will be returned in the form of a dictionary,
# with format {"instruction" : "...", "rd" : '...', "rs1" : '...', "rs2" : '...', 'imm' : '...'}

class Decode: 

    def decode(self, mem_delay, inst, RegisterFile, scoreboard):
        if inst == "0"*32 or inst == None or len(inst) == 3:
            return None
        
        if isinstance(inst, dict): #Happens in stalling
            return inst
        
        opcode = inst[-7 : ]
        
        if opcode == '0110011':
            return self.R_type(inst[ : -7], RegisterFile, scoreboard)
        
        elif opcode == '0010011':
            return self.ADDI(inst[ : -7], RegisterFile, scoreboard)
        
        elif opcode == '0000011':
            return self.LW(inst[ : -7], mem_delay, RegisterFile, scoreboard)
        
        elif opcode == '0100011':
            return self.SW(inst[ : -7], RegisterFile, scoreboard)
        
        elif opcode == '1100011':
            return self.BEQ(inst[ : -7], RegisterFile, scoreboard)

        elif opcode == '0000001':
            return self.LOADNOC(inst[ : -7], RegisterFile, scoreboard)
        
        return None

    def R_type(self, inst, RegisterFile, scoreboard):
        Dict = {}

        funct3 = inst[-8 : -5]
        if funct3 == '111':
            Dict["instruction"] = "AND"
        
        elif funct3 == '110':
            Dict["instruction"] = "OR"

        elif funct3 == '000':
            if inst[0:7] == '0000000':
                Dict["instruction"] = "ADD"
            
            else:
                Dict["instruction"] = "SUB"
        
        elif funct3 == '001':
            Dict["instruction"] = "SLL"
        
        elif funct3 == '101':
            Dict["instruction"] = "SRA"
        
        Dict["rd"] = inst[-5 : ]
        Dict['_rs1'] = "R" + str(int(RegisterFile[int(inst[-13: -8], 2)].name, 2))
        Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))

        if (Dict['_rs1'] in scoreboard.keys()):
            Dict['bypassing'] = True
        else:
            Dict['bypassing'] = False
        Dict['rs1'] = RegisterFile[int(inst[-13: -8], 2)].getValue()

        if (Dict['_rs2'] in scoreboard.keys()):
            Dict["bypassing"] = Dict['bypassing'] or True
        else:
            Dict['bypassing'] = Dict['bypassing'] or False
        Dict['rs2'] = RegisterFile[int(inst[-18:-13], 2)].getValue()

        Dict ["_rd"] = "R" + str(int(RegisterFile[int(inst[-5 : ], 2)].name, 2))
        
        if Dict["_rd"] not in scoreboard.keys():
            scoreboard[Dict["_rd"]] = [1]
        return Dict


    def ADDI(self, inst, RegisterFile, scoreboard):
        Dict = {}
        Dict["instruction"] = "ADDI"
        Dict["rd"] = inst[-5:]
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))

        if (Dict['_rs1'] in scoreboard.keys()):
            Dict["bypassing"] = True
        else:
            Dict["bypassing"] = False
        Dict['rs1'] = RegisterFile[int(inst[-13: -8], 2)].getValue()

        Dict["imm"] = inst[0 : 12]
        Dict["_rd"] = "R" + str(int(RegisterFile[int(inst[-5:], 2)].name, 2))
    
        if Dict["_rd"] not in scoreboard.keys():
            scoreboard[Dict["_rd"]] = [1]
        return Dict


    def LW(self, inst, mem_delay, RegisterFile, scoreboard):
        Dict = {}
        Dict["instruction"] = "LW"
        Dict["rd"] = inst[-5:]
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
        if Dict['_rs1'] in scoreboard.keys():
            Dict["bypassing"] = True
        else:
            Dict["bypassing"] = False
        Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()

        Dict["imm"] = RegisterFile[int(inst[0:12], 2)].getValue()
        Dict["_rd"] = "R" + str(int(RegisterFile[int(inst[-5:], 2)].name, 2))
        
        if Dict["_rd"] not in scoreboard.keys():
            scoreboard[Dict["_rd"]] = [mem_delay]
        return Dict


    def SW(self, inst, RegisterFile, scoreboard):
        Dict = {}
        funct3 = inst[-8 : -5]
        if funct3 == "010":
            Dict["instruction"] = "SW"
            Dict["imm"] = inst[0:7] + inst[-5:]
            Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
            Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))

            if (Dict['_rs1'] in scoreboard.keys()):
                Dict["bypassing"] = True
            else:
                Dict["bypassing"] = False
            Dict['rs1'] = RegisterFile[int(inst[-13: -8], 2)].getValue()

            if (Dict['_rs2'] in scoreboard.keys()):
                Dict["bypassing"] = Dict["bypassing"] or True
            else:
                Dict["bypassing"] = Dict["bypassing"] or False
            Dict['rs2'] = RegisterFile[int(inst[-18:-13], 2)].getValue()

        if funct3 == "100":
            Dict["instruction"] = "STORENOC" 
            Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
            Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
            if (Dict['_rs1'] in scoreboard.keys()):
                Dict["bypassing"] = True
            else:
                Dict["bypassing"] = False
            
            Dict["rs1"] = format(0, "032b")
    
            if (Dict['_rs2'] in scoreboard.keys()):
                Dict["bypassing"] = Dict["bypassing"] or True
            else:
                Dict["bypassing"] = Dict["bypassing"] or False
            Dict["rs2"] = format(1, "032b") 
            Dict["imm"] = "0"*12
        return Dict
    
    def LOADNOC(self, inst, RegisterFile, scoreboard):
        Dict = {}
        Dict["instruction"] = "LOADNOC"
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
        Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
        Dict["imm"] = inst[0:7] + inst[-8:]

        if Dict['_rs1'] in scoreboard.keys():
            Dict["bypassing"] = True
        else:
            Dict["bypassing"] = False
        Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()
        Dict["rs2"] = RegisterFile[int(inst[-18:-13], 2)].getValue()

        return Dict

    def BEQ(self, inst, RegisterFile, scoreboard):
        Dict = {}
        Dict["instruction"] = "BEQ"
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
        Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))

        # if (Dict['_rs1'] in scoreboard.keys()):
        #     Dict['bypassing'] = True
        # else:
        #     Dict['bypassing'] = False
        Dict['rs1'] = RegisterFile[int(inst[-13: -8], 2)].getValue()

        # if (Dict['_rs2'] in scoreboard.keys()):
        #     Dict['bypassing'] = Dict['bypassing'] or True
        # else:
        Dict['bypassing'] = False

        Dict['rs2'] = RegisterFile[int(inst[-18:-13], 2)].getValue()
        # Dict["BranchOffset"] = inst[0] + inst[-1] + inst[1:7]  + inst[-5:-1]
        Dict["BranchOffset"] = inst[0:7] + inst[-5:]
    

        if Dict["BranchOffset"][0] == "0":
            Dict["BranchOffset"] = int(Dict["BranchOffset"], 2)
        else:
            ones_comp = ""
            for c in Dict["BranchOffset"]:
                if c == "1":
                    ones_comp = ones_comp + "0"
                else:
                    ones_comp = ones_comp + "1"
        
            int_val = -1*(int(ones_comp, 2) + 1)
            Dict["BranchOffset"] = int_val
        if (len(Dict["rs1"]) > 0 and len(Dict["rs2"]) > 0) and Dict["rs1"] == Dict["rs2"]:

            Dict["BranchTaken?"] = "YES"
        else:
            Dict["BranchTaken?"] = "NO"
        return Dict