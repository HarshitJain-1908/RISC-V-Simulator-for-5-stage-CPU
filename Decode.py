# Runs in the second half of the clock cycle. Must be triggered only after the first half of the clock cycle
# Decode the instruction and read the registers corresponding to register
# source specifiers from the register file. Do the equality test on the 
# registers as they are read, for a possible branch.
# The decoded instruction will be returned in the form of a dictionary,
# with format {"instruction" : "...", "rd" : '...', "rs1" : '...', "rs2" : '...', 'imm' : '...'}

class Decode: 

    def decode(self, inst, RegisterFile):
        if inst == "0"*32 :
            return None
        
        opcode = inst[-7 : ]
        
        if opcode == '0110011':
            return self.R_type(inst[ : -7], RegisterFile)
        
        elif opcode == '0010011':
            return self.ADDI(inst[ : -7], RegisterFile)
        
        elif opcode == '0000011':
            return self.LW(inst[ : -7], RegisterFile)
        
        elif opcode == '0100011':
            return self.SW(inst[ : -7], RegisterFile)
        
        elif opcode == '1100011':
            return self.BEQ(inst[ : -7], RegisterFile)

        elif opcode == '0000001':
            return self.LOADNOC(inst[ : -7], RegisterFile)

    def R_type(self, inst, RegisterFile):
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
        Dict['rs1'] = RegisterFile[int(inst[-13: -8], 2)].getValue()
        Dict['rs2'] = RegisterFile[int(inst[-18:-13], 2)].getValue()
        Dict['_rs1'] = "R" + str(int(RegisterFile[int(inst[-13: -8], 2)].name, 2))
        Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
        Dict ["_rd"] = "R" + str(int(RegisterFile[int(inst[-5 : ], 2)].name, 2))
        
        return Dict

    def ADDI(self, inst, RegisterFile):
        Dict = {}
        Dict["instruction"] = "ADDI"
        Dict["rd"] = inst[-5:]
        Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()
        Dict["imm"] = inst[0 : 12]
        Dict["_rd"] = "R" + str(int(RegisterFile[int(inst[-5:], 2)].name, 2))
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))

        return Dict

    def LW(self, inst, RegisterFile):
        Dict = {}
        Dict["instruction"] = "LW"
        Dict["rd"] = inst[-5:]
        Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()
        Dict["imm"] = RegisterFile[int(inst[0:12], 2)].getValue()
        Dict["_rd"] = "R" + str(int(RegisterFile[int(inst[-5:], 2)].name, 2))
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
        return Dict

    def SW(self, inst, RegisterFile):
        Dict = {}
        funct3 = inst[-8 : -5]
        if funct3 == "010":
            Dict["instruction"] = "SW"
            Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()
            Dict["rs2"] = RegisterFile[int(inst[-18:-13], 2)].getValue()
            Dict["imm"] = inst[0:7] + inst[-5:]
            Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
            Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
        if funct3 == "100":
            Dict["instruction"] = "STORENOC"
            Dict["rs1"] = format(0, "032b")
            Dict["rs2"] = format(1, "032b")  
            Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
            Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
            Dict["imm"] = "0"*12
        return Dict
    
    def LOADNOC(self, inst, RegisterFile):
        Dict = {}
        Dict["instruction"] = "LOADNOC"
        Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()
        Dict["rs2"] = RegisterFile[int(inst[-18:-13], 2)].getValue()
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
        Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
        Dict["imm"] = inst[0:7] + inst[-8:]
        return Dict

    def BEQ(self, inst, RegisterFile):
        Dict = {}
        Dict["instruction"] = "BEQ"
        Dict["rs1"] = RegisterFile[int(inst[-13:-8], 2)].getValue()
        Dict["rs2"] = RegisterFile[int(inst[-18:-13], 2)].getValue()
        Dict["_rs1"] = "R" + str(int(RegisterFile[int(inst[-13:-8], 2)].name, 2))
        Dict['_rs2'] = "R" + str(int(RegisterFile[int(inst[-18:-13], 2)].name, 2))
        Dict["BranchOffset"] = inst[0] + inst[-1] + inst[1:7]  + inst[-5:-1] +'0'
        if Dict["rs1"] == Dict["rs2"]:
            #branch_target should change the PC value to [(current PC) +  Dict["BranchOffset"]]
            Dict["BranchTaken?"] = "YES";
        else:
            Dict["BranchTaken?"] = "NO";
        
        return Dict