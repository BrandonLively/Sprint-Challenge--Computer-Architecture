"""CPU functionality."""

import sys

LDI = 0b10000010  # Load and Increment
PRN = 0b01000111  # Print
HLT = 0b00000001  # Halt
PUS = 0b01000101  # PUSH
POP = 0b01000110  # POP
MUL = 0b10100010  # Multiply
MOD = 0b10100100  # Modulo
DIV = 0b10100011  # Divide
SUB = 0b10100001  # Subtract
ADD = 0b10100000  # Add
AND = 0b10101000  # And
NOT = 0b01101001  # Not
OR = 0b10101010  # Or
XOR = 0b10101011  # Xor
SHL = 0b10101100  # Bitwise Shift left
SHR = 0b10101101  # Bitwise Shift right
INC = 0b01100101  # Increment
DEC = 0b01100110  # Decrement
CMP = 0b10100111  # Compare - set flag is equal
JMP = 0b01010100  # JUMP to value
JEQ = 0b01010101  # JUMP to value if equal flag is set
JNE = 0b01010110  # JUMP to value if equal flag is not set


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.equal_flag = False
        self.pc = 0
        self.ram = [None] * 256
        self.reg = [0] * 8

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print("File not Found")
            sys.exit(2)

    def alu(self, op, op_1, op_2):
        """ALU operations."""

        value_1 = self.reg[op_1]
        if op_2 is not None:
            value_2 = self.reg[op_2]

        if op == "ADD":
            value_1 += value_2

        elif op == "SUB":
            value_1 -= value_2

        elif op == "MUL":
            value_1 *= value_2

        elif op == "DIV":
            value_1 /= value_2

        elif op == "MOD":
            self.reg[op_1] = value_1%value_2

        elif op == "AND":
            value_1_binary = format(value_1, '08b')
            value_2_binary = format(value_2, '08b')
            results = ''
            for i in range(8):
                if value_1_binary[i] == '1' and value_2_binary[i] == '1':
                    results += '1'
                else:
                    results += '0'

            self.reg[op_1] = int(results, 2)

        elif op == "OR":
            value_1_binary = format(value_1, '08b')
            value_2_binary = format(value_2, '08b')
            results = ''
            for i in range(8):
                if value_1_binary[i] == '1' or value_2_binary[i] == '1':
                    results += '1'
                else:
                    results += '0'

            self.reg[op_1] = int(results, 2)

        elif op == "XOR":
            value_1_binary = format(value_1, '08b')
            value_2_binary = format(value_2, '08b')
            results = ''
            for i in range(8):
                if value_1_binary[i] == '1' or value_2_binary[i] == '1':
                    if value_1_binary[i] == '1' and value_2_binary[i] == '1':
                        results += '0'
                    else:
                        results += '1'
                else:
                    results += '0'
            self.reg[op_1] = int(results, 2)

        elif op == "NOT":
            value_1_binary = format(value_1, '08b')
            results = ''
            for i in range(8):
                if value_1_binary[i] == '1':
                    results += '0'
                else:
                    results += '1'

            self.reg[op_1] = int(results, 2)

        elif op == "SHR":
            value_1_binary = format(value_1, '08b')
            results_left = ''
            results_right = ''
            for i in range(8):
                if i < value_2:
                    results_left += '0'
                else:
                    results_right += value_1_binary[i-value_2]

            self.reg[op_1] = int((results_left + results_right), 2)

        elif op == "SHL":
            value_1_binary = format(value_1, '08b')
            results_left = ''
            results_right = ''
            for i in range(8):
                if i < value_2:
                    results_left += '0'
                else:
                    results_right += value_1_binary[i]

            self.reg[op_1] = int((results_right + results_left), 2)

        elif op == "JMP":
            self.pc = value_1

        elif op == "CMP":
            if value_1 == value_2:
                self.equal_flag = True

        elif op == "JNE":
            if self.equal_flag is not True:
                self.pc = value_1
            else:
                self.pc += 2

        elif op == "JEQ":
            if self.equal_flag is True:
                self.pc = value_1
            else:
                self.pc += 2

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def run(self):
        running = True
        while running:
            command = self.ram[self.pc]
            if command == HLT:
                running = False

            elif command == PRN:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2

            elif command == LDI:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                self.pc += 3

            elif command == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == SUB:
                self.alu("SUB", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == ADD:
                self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == DIV:
                self.alu("DIV", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == CMP:
                self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == JNE:
                self.alu("JNE", self.ram[self.pc + 1], None)

            elif command == JMP:
                self.alu("JMP", self.ram[self.pc + 1], None)

            elif command == JEQ:
                self.alu("JEQ", self.ram[self.pc + 1], None)

            elif command == AND:
                self.alu("AND", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == OR:
                self.alu("OR", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == XOR:
                self.alu("XOR", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == SHR:
                self.alu("SHR", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == SHL:
                self.alu("SHL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == MOD:
                self.alu("MOD", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif command == NOT:
                self.alu("NOT", self.ram[self.pc + 1], None)
                self.pc += 2

            elif command == MOD:
                self.alu("MOD", self.ram[self.pc + 1], None)
                self.pc += 3