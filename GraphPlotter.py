import matplotlib.pyplot as plt

len_program = 0

def plot_num_reg_and_mem_instns(program_binary):
    y = [0, 0]
    file = open(program_binary, "r")
    n = 0
    for instruction in file:
        if (len(instruction) == 33):
            opcode = instruction[-8:-1]
        else:
            opcode = instruction[-7:]

        if opcode in ['0100011', '0000011', '0000001']: # memory instructions
            y[0] = y[0] + 1
        else: #reg instructions
            y[1] = y[1] + 1
        n = n + 1
    
    plt.bar(["Num Memory Instructions", "Num Register Instructions"], y)
    plt.title("Number of memory and register instructions in the program")
    plt.yticks(range(0, n + 1))
    len_program = n
    file.close()
    plt.show()


def plot_instruction_and_data_mem_access_pattern(log):
    file = open(log, "r")
    cycles = []
    imem_accesses = []
    dmem_accesses = []
    for line in file:
        if line[0:5] == "FETCH":
            cycles.append(len(cycles))
            line = line.split()
            if (len(line) > 2):
                line = int(line[2][:-1])
                if (len(imem_accesses) == 0 or imem_accesses[-1] != line): #check for stalls
                    imem_accesses.append(line)
                else:
                    imem_accesses.append(-1)
            else:
                imem_accesses.append(-1)
        
        """elif line[0:6] == "MEMORY":
            line = line.split()
            if (len(line) > 2):
                if line[3] in ["SW", "LW", "LOADNOC"]: #INCOMPLETE
                    dmem_accesses.append(int(line[11]))
                elif line[3] =="STORENOC":
                    dmem_accesses.append(16388) #16388 is the decimal of 0x4004
                else:
                    dmem_accesses.append(-9999)
            else:
                dmem_accesses.append(-9999)"""

    f2 = plt.figure()
    plt.scatter(cycles, imem_accesses, color="orange")
    plt.xlabel("Cycle")
    plt.ylabel("Instruction memory address(base 10)")
    # plt.xlim(0, 50)
    # plt.ylim(0, 30)
    plt.title("Instruction Memory Accesses")
    
    plt.xticks(range(0, len(cycles) + 1))
    plt.yticks(range(0, len(cycles) + 1))
    plt.ylim(0, len(cycles) + 1)
    plt.show()
    """f3 = plt.figure()
    plt.scatter(cycles, dmem_accesses, color="red")
    plt.xlabel("Cycle")
    plt.ylabel("Data memory address(base 10)")
    plt.title("Data Memory Accesses")
    plt.xticks(range(0, len(cycles) + 1))
    plt.ylim(0, 2**14+5)
    file.close()
    plt.show()"""

            

