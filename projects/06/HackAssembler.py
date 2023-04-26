import sys

dest = {
  "null" : "000",
  "M" : "001",
  "D" : "010",
  "MD" : "011",
  "A" : "100",
  "AM" : "101",
  "AD" : "110",
  "AMD" : "111"
}

jump = {
  "null" : "000",
  "JGT" : "001",
  "JEQ" : "010",
  "JGE" : "011",
  "JLT" : "100",
  "JNE" : "101",
  "JLE" : "110",
  "JMP" : "111"
}

comp = {
    "0" : "101010",
    "1" : "111111",
    "-1" : "111010",
    "D" : "001100",
    "X" : "110000",
    "!D" : "001101",
    "!X" : "110001",
    "-D" : "001111",
    "-X" : "110011",
    "D+1" : "011111",
    "X+1" : "110111",
    "D-1" : "001110",
    "X-1" : "110010",
    "D+X" : "000010",
    "D-X" : "010011",
    "X-D" : "000111",
    "D&X" : "000000",
    "D|X" : "010101"
}

symbols = {
    "SP" : "0",
    "LCL" : "1",
    "ARG" : "2",
    "THIS" : "3",
    "THAT" : "4",
    "R0" : "0",
    "R1" : "1",
    "R2" : "2",
    "R3" : "3",
    "R4" : "4",
    "R5" : "5",
    "R6" : "6",
    "R7" : "7",
    "R8" : "8",
    "R9" : "9",
    "R10" : "10",
    "R11" : "11",
    "R12" : "12",
    "R13" : "13",
    "R14" : "14",
    "R15" : "15",
    "SCREEN" : "16384",
    "KBD" : "24576"
}

labels = {}
var = {}
ram_cnt = 16

def get_A_instr(line):
    global ram_cnt
    const = line[1:-1]
    if not const.isdigit():
        if const in labels:
            const = labels[const]
        elif const in symbols:
            const = symbols[const]
        elif const in var:
            const = var[const]
        else:
            var[const] = ram_cnt
            ram_cnt += 1
            const = var[const]
    bin_dig = bin(int(const))[2:]
    res = (16 - len(bin_dig)) * '0'
    res = res + bin_dig
    return res

def get_three_var(line):
    dest_var = ""
    comp_var = ""
    jmp_var = ""
    equal_ind = line.find('=')
    sem_ind = line.find(';')
    if equal_ind == -1 and sem_ind == -1:
        comp_var = line[-1]
        dest_var = "null"
        jmp_var = "null"
    elif equal_ind == -1:
        comp_var = line[0:sem_ind]
        jmp_var = line[sem_ind+1:]
        dest_var = "null"
    elif sem_ind == -1:
        dest_var = line[0:equal_ind]
        comp_var = line[equal_ind+1:]
        jmp_var = "null"
    else:
        dest_var = line[0:equal_ind]
        comp_var = line[equal_ind+1:sem_ind]
        jmp_var = line[sem_ind+1:]
    return dest_var, comp_var, jmp_var

def get_C_instr(line):
    line = line[:-1]
    dest_var, comp_var, jmp_var = get_three_var(line)
    a = "1" if comp_var.find('M') != -1 else "0"
    tmp = comp_var.find('M')
    if tmp != -1:
        comp_var = comp_var[0:tmp] + 'X' + comp_var[tmp+1:]
    tmp = comp_var.find('A')
    if tmp != -1:
        comp_var = comp_var[0:tmp] + 'X' + comp_var[tmp+1:]
    res = "111" + a + comp[comp_var] + dest[dest_var] + jump[jmp_var]
    return res

def write_txt(txt):
    new_name = sys.argv[1][:-4] + ".hack" 
    f = open(new_name, "w")
    f.write(txt)
    f.close()

def translate_line(line):
    machine_line = ""
    com_ind = line.find('//')
    if com_ind != -1:
        line = line[0:com_ind+1]
    if line[0] == '@':
        machine_line = get_A_instr(line)
    else:
        machine_line = get_C_instr(line)
    return machine_line

def first_pass(f):
    cnt = 0
    for line in f:
        format_line = ""
        parsed_line = line.split(" ")
        for cur in parsed_line:
            format_line += cur
        if format_line[0] == '(':
            labels[format_line[1:-2]] = cnt
        elif len(format_line) > 0 and format_line[0] != "/" and format_line[0] != '\n':
            cnt += 1

def sec_pass(f):
    txt = ""
    for line in f:
        format_line = ""
        parsed_line = line.split(" ")
        for cur in parsed_line:
            format_line += cur
        if len(format_line) > 0 and format_line[0] != '(' and format_line[0] != "/" and format_line[0] != '\n':
            txt += translate_line(format_line) + '\n'
    return txt


def translate_to_machine(filename):
    f = open(filename, "r")
    first_pass(f)
    f.seek(0)
    txt = sec_pass(f)
    write_txt(txt)
    f.close()


def main():
    if len(sys.argv) > 1:
        translate_to_machine(sys.argv[1])

if __name__ == "__main__":
    main()
