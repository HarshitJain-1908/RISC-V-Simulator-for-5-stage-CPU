This was a group project in the Computer Architecture course offered in IIIT Delhi. The group project consist of 4 members. The detailed description can be found in the document titled 'Computer Architecture Projects Description'. We have implemented 'Project4 - Cycle accurate simulator for 5-stage CPU' in Python.

Steps to run the Simulator:-
1. Download all the files. (Input file to the simulator is in 'test_binary.txt' and the corresponding assembly code is in 'AssemblyCode.txt')
2. Run 'cpu.py' to run the simulator.
3. Enter custom defined instruction memory and data memory delay.

Consequently, a file named 'log.txt' is created. And, relevant graphs would pop up. All the information about data stalls, number of 
memory instructions and data instructions are stored in the log file (refer to Project descrition to know the exact type of content, graphs etc.). 

General information about the RISC-V ISA:-
Instructions with their encoding-
AND rd, rs1, rs2
OR rd, rs1, rs2
ADD rd, rs1, rs2
SUB rd, rs1, rs2
ADDI rd, rs1, imm
BEQ rs1, rs2, imm       (12 bit immediate field is used to encode branch offsets.)
LW rd, rs1, imm         (store 32 bit value to mem)(mem addr = [rs1] + imm(12 bit))
SW rs1, rs2, imm        (stores 32 bit value to mem)(mem addr = [rs1] + imm(12 bit))
SLL rd, rs1, rs2        (Shift logical left: performs logical shift left on the value in rs1 by the shift amount held in the lower 5 bits of rs2.)
SRA rd, rs1, rs2        (Shift Right Arithmetic: performs arithmetic shift right on the value in rs1 by the shift amount held in the lower 5 bits of rs2.)
LOADNOC rs2, rs1, imm
STORENOC                (will always be = 00000000000000000100000000100011)

All these instructions are 32 bit each.

_7bits_      |_5bts|5bts_|_3bts|5bts       |_7bits_
0000000      | rs2 | rs1 | 111 | rd        |0110011      (AND)
0000000      | rs2 | rs1 | 110 | rd        |0110011      (OR)
0000000      | rs2 | rs1 | 000 | rd        |0110011      (ADD)
0100000      | rs2 | rs1 | 000 | rd        |0110011      (SUB)
imm[11:0]          | rs1 | 000 | rd        |0010011      (ADDI)
imm[0:7]     | rs2 | rs1 | 000 |imm[8:11]  |1100011      (BEQ)
imm[11:0]          | rs1 | 010 | rd        |0000011      (LW)
imm[11:5]    | rs2 | rs1 | 010 | imm[4:0]  |0100011      (SW)
0000000      | rs2 | rs1 | 001 | rd        |0110011      (SLL)
0100000      | rs2 | rs1 | 101 | rd        |0110011      (SRA)
imm[11:5]    | rs2 | rs1 |    imm[7:0]     |0000001      (LOADNOC)
0000000      |00000|00000| 100 | 00000     |0100011      (STORENOC)

There are 2^5 = 32 registers(32 bit each), numbered from 00000 to 11111.
