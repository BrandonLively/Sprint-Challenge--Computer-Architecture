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
OR  = 0b10101010  # Or
XOR = 0b10101011  # Xor
SHL = 0b10101100  #
SHR = 0b10101101  #
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

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "JMP":
            self.pc = self.reg[reg_a]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.equal_flag = True
        elif op == "JNE":
            if self.equal_flag is not True:
                self.pc = self.reg[reg_a]
            else:
                self.pc += 2
        elif op == "JEQ":
            if self.equal_flag is True:
                self.pc = self.reg[reg_a]
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
