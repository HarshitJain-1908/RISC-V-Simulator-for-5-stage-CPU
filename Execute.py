# instructions can be
# decode gave type of instruction ie (R,S,I) and what insruction to run
# R type [and, or, add, sub, sll, sra]
# I type [addi, lw]
# S type [sw]
# B type [beq]
# ADD ADDI SUB 
# does not store results
# SW and LW are returning the address o store or load from 

class Execute:

    Itype = ["ADDI", "LW"]
    Rtype = ["AND", "OR", "ADD", "SUB", "SLL", "SRA"]
    Stype = ["SW", "LOADNOC", "STORENOC"]
    Btype = ["BEQ"]
        

    def execute(self, set):
        
        if set is None :
            return None

        if (set["instruction"] in self.Itype):

            rs1 = set["rs1"]
            print("rs1", rs1)
            imm = set["imm"]
            val1 = int(rs1 , 2)  
            val2 = int(imm, 2)
            if (rs1[0] == 1):
                val1 -= 2**32
                print("let's see", val1) 
            if (imm[0] == 1):
                val2 -= 2**32 

            if (set["instruction"] == "ADDI"):
                result = self.ADDI(val1, val2)
            if (set["instruction"] == "LW"):
                result = self.ADDI(val1,val2)
            
            set["result"] = result
            return set
    
        elif (set["instruction"] in self.Rtype):
            rs1 = set["rs1"]
            val1 = int(rs1 , 2)
            rs2 = set["rs2"]
            val2 = int(rs2 , 2)
            if (rs1[0] == 1):
                val1 -= 2**32 
            if (rs2[0] == 1):
                val2 -= 2**32 

            if (set["instruction"] == "AND"):
                result = self.AND(val1, val2)
            elif (set["instruction"] == "OR"):
                result = self.OR(val1, val2)
            elif (set["instruction"] == "ADD"):
                result = self.ADD(val1, val2)
            elif (set["instruction"] == "SUB"):
                result = self.SUB(val1,val2)
            elif (set["instruction"] == "SLL"):
                result = self.SLL(val1,val2)
            elif (set["instruction"] == "SRA"):
                result = self.SRA(val1,val2)

            if len(result) > 32:                    #overflow check
                result = result[-32:] 
            set["result"] = result
            return set                           #result in string 32 bit binary 
        
        elif (set["instruction"] in self.Stype):
            rs1 = set["rs1"]
            rs2 = set["rs2"]
            imm = int(set["imm"], 2)
            val1 = int(rs1 , 2)
            val2 = int(rs2 , 2)
            if (rs1[0] == 1):
                val1 -= 2**32 
            if (rs2[0] == 1):
                val2 -= 2**32 

            if (set["instruction"] == "SW"):
                result = self.ADDI(val1,imm)
            if (set["instruction"] == "STORENOC"):
                result = format((2**14) + 4, "032b")
            if(set["instruction"] == "LOADNOC"):
                result = self.ADDI(val1,imm)
                if (int(result, 2) < (2**14)) or (int(result,2) > (2**14)+3):
                    result = "invalid"
            
            set["result"] = result
            return set
        
        elif (set["instruction"] in self.Btype):
                return set
        
        else:
            print("invalid operation type passed in EXECUTE : ", set["instruction"])
            return set
            
    def ADD(self,val1, val2): 
        result = val1 + val2 #int result
        result = format(result, "032b")
        return result

    
    def SUB(self,val1, val2): 
        result = val1 - val2 #int result
        if (result >= 0):
            result = format(result, "032b")
        else:
            result = format(2**32 - abs(result), "032b")
        return result

    def AND(self,val1, val2): 
        result = val1 & val2 #int result
        result = format(result, "032b")
        return result
    
    def OR(self,val1, val2): 
        result = val1 | val2 #int result
        result = format(result, "032b")
        return result
    
    def SLL(self,val1, val2):
        result = val1 << val2 #int result
        result = format(result, "032b")
        return result
    
    def SRA(self,val1,val2):
        print(val1, val2)
        result = val1 >> val2 #int result
        result = format(result, "032b")
        return result


    def ADDI(self, val1, val2): 
        result = val1 + val2 #int result
        result = format(result, "032b")
        if len(result) > 32:                    #overflow check
            result = result[-32:] 
        return result                           #result in string 32 bit binary