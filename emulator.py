#!/usr/bin/env python3
asm = open("instructions", "r").read().split("\n")
asm = [[int(part, 16) if part[:2] == "0x" else part for part in instruction.split("#")[0].strip().split()] for instruction in asm if len(instruction) > 0]
rs = dict([[item, 0] for item in ["ax", "bx", "cx", "dx", "ip", "sp", "sb", "fl"]])
ram = [0 for i in range(1024)]

def debug(): 
    # prints the registers and the first 10 values in ram
    print("Registers: " + str(rs));
    i = len(ram) - 1
    while ram[i] == 0: i -= 1
    print("Ram: " + str(ram[:i+1])[:-1] + ", ...]")
def handle_three(i):
    instruction = i[0]
    first = i[1]
    second = i[2]
    if instruction == "add": rs[second] += rs[first]
    if instruction == "addi": rs[second] += first
    if instruction == "sub": rs[second] -= rs[first]
    if instruction == "subi": rs[second] -= first
    if instruction == "ls": rs[second] <<= rs[first]
    if instruction == "lsi": rs[second] <<= first
    if instruction == "rs": rs[second] >>= rs[first]
    if instruction == "rsi": rs[second] >>= first
    if instruction == "xor": rs[second] ^= rs[first]
    if instruction == "xori": rs[second] ^= first
    if instruction == "and": rs[second] &= rs[first]
    if instruction == "andi": rs[second] &= first
    if instruction == "mov": rs[second] = rs[first]
    if instruction == "movi": rs[second] = first
    if instruction == "test":
        if rs[second] == rs[first]: rs["fl"] = 0b001
        elif rs[second] < rs[first]: rs["fl"] = 0b010
        else: rs["fl"] = 0b100
    if instruction == "testi":
        if rs[second] == first: rs["fl"] = 0b001
        elif rs[second] < first: rs["fl"] = 0b010
        else: rs["fl"] = 0b100
    if instruction == "lea": rs[second] = ram[rs[first]]
    if instruction == "leai": rs[second] = ram[first]
    if instruction == "sea": ram[rs[first]] = rs[second]
    if instruction == "seai": ram[first] = rs[second]
def handle_two(i):
    instruction = i[0]
    arg = i[1]
    if instruction == "call":
        handle_two(["pushi", rs["ip"]])
        instruction = "jmp"
    if instruction == "je":
        if rs["fl"] & 0b001 > 0: instruction = "jmp"
    if instruction == "jne":
        if rs["fl"] & 0b001 == 0: instruction = "jmp"
    if instruction == "jl":
        if rs["fl"] & 0b100 > 0: instruction = "jmp"
    if instruction == "jle":
        if rs["fl"] & 0b101 > 0: instruction = "jmp"
    if instruction == "jg":
        if rs["fl"] & 0b010 > 0: instruction = "jmp"
    if instruction == "jge":
        if rs["fl"] & 0b011 > 0: instruction = "jmp"
    if instruction == "jmp":
        rs["ip"] = asm.index([arg + ":"]) - 1
    if instruction == "push":
        ram[rs["sp"]] = rs[arg]
        rs["sp"] += 1
    if instruction == "pushi":
        ram[rs["sp"]] = arg
        rs["sp"] += 1
    if instruction == "pop":
        rs["sp"] -= 1
        rs[arg] = ram[rs["sp"]]

while True:
    if rs["ip"] >= len(asm):
        print("Out of instructions")
        break;
    instruction = asm[rs["ip"]]
    if len(instruction) == 3: handle_three(instruction)
    elif len(instruction) == 2: handle_two(instruction)
    elif len(instruction) == 1:
        instruction = instruction[0]
        if instruction == "debug":
            debug()
        if instruction == "abort":
            print("Aborted at " + str(rs["ip"]))
            break
        if instruction == "ret":
            rs["sp"] -= 1
            rs["ip"] = ram[rs["sp"]]
    elif len(instruction) != 0:
        print("Found suspiciously long instruction \"" + " ".join(instruction) + "\"")
    rs["ip"] += 1
if rs["sp"] != 0:
    print("WARNING - Stack was not empty at program exit")
debug()
