Run 'cpu.py' to run the simulator and a file named 'log.txt' is created 
containing the required contents of log file. Test file is in 'test_binary.txt'.

AND rd, rs1, rs2
OR rd, rs1, rs2
ADD rd, rs1, rs2
SUB rd, rs1, rs2
ADDI rd, rs1, imm
BEQ rs1, rs2, imm       (12 bit immediate field is used to encode branch offsets in multiples of 2. Add 0 to LSB of the immediate to get the correct offset)
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
imm[12|10:5] | rs2 | rs1 | 000 |imm[4:1|11]|1100011      (BEQ)
imm[11:0]          | rs1 | 010 | rd        |0000011      (LW)
imm[11:5]    | rs2 | rs1 | 010 | imm[4:0]  |0100011      (SW)
0000000      | rs2 | rs1 | 001 | rd        |0110011      (SLL)
0100000      | rs2 | rs1 | 101 | rd        |0110011      (SRA)
imm[11:5]    | rs2 | rs1 |    imm[7:0]     |0000001      (LOADNOC)
imm[11:5]    | rs2 | rs1 | 100 | imm[4:0]  |0100011      (STORENOC)



There are 2^5 = 32 registers(32 bit each), numbered from 00000 to 11111.