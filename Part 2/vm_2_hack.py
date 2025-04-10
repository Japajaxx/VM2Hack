# call with "python vm_2_hack.py <filename>.vm"

import sys

def parser(file_path):

    def remove_whitespace_and_labels():
        for i in lines:
            if i[0] != "\n":
                i = i.strip()
                if i[0] != "/":
                    i = i.strip()
                    lines_new.append(i)

    lines_new = []
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    remove_whitespace_and_labels()

    return lines_new


def code_writer(lines, filename):

    asm_file = open(filename + (".asm"), "a")

    sum = {
        "add": "M=D+M",
        "sub": "M=M-D",
    }

    com = {
        "and": "M=D&M",
        "or": "M=D|M",
    }

    neg = {
        "neg": "M=-M",
        "not": "M=!M",
    }

    j = {
        "eq": "D;JEQ",
        "gt": "D;JGT",
        "lt": "D;JLT",
    }

    push_statements = {
        "this": "@THIS\nA=D+M",
        "that": "@THAT\nA=D+M",
        "argument": "@ARG\nA=D+M",
        "local": "@LCL\nA=D+M",
        "temp": "@5\nA=D+A",
        "pointer": "@3\nA=D+A",
    }

    pop_statements = {
        "this": "@THIS\nD=D+M",
        "that": "@THAT\nD=D+M",
        "argument": "@ARG\nD=D+M",
        "local": "@LCL\nD=D+M",
        "temp": "@5\nD=D+A",
        "pointer": "@3\nD=D+A",
    }

    j_counter = -1

    for i in lines:
        words = i.split()
        if words[0] == "push":
            asm_file.write(f"// {words[0]} {words[1]} {words[2]}\n")
            if words[1] == "static" or words[1] == "constant":
                if words[1] == "static":
                        asm_file.write(f"@Static_{words[2]}\nD=M\n\n")
                elif words[1] == "constant":
                    asm_file.write(f"@{words[2]}\nD=A\n")
                asm_file.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n\n")
            elif words[1] in push_statements:
                asm_file.write(f"@{words[2]}\nD=A\n{push_statements[words[1]]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n\n")

        elif words[0] == "pop":
            asm_file.write(f"// {words[0]} {words[1]} {words[2]}\n")
            if words[1] == "static":
                asm_file.write(f"@SP\nAM=M-1\nD=M\n@Static_{words[2]}\nM=D\n\n")
            elif words[1] in pop_statements:
                asm_file.write(f"@{words[2]}\nD=A\n{pop_statements[words[1]]}\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n\n")
            

        elif words[0] in sum:
            asm_file.write(f"// {words[0]}\n@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\n{sum[words[0]]}\n@SP\nM=M+1\n\n")

        elif words[0] in com:
            asm_file.write(f"// {words[0]}\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\n{com[words[0]]}\n\n")

        elif words[0] in neg:
            asm_file.write(f"// {words[0]}\n@SP\nA=M-1\n{neg[words[0]]}\n\n")

        elif words[0] in j:
            j_counter += 1
            asm_file.write(f"// {words[0]}\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@{words[0]}_True{j_counter}\n{j[words[0]]}\n@SP\nA=M-1\nM=0\n({words[0]}_True{j_counter})\n\n")

        elif words[0] == "label":
            asm_file.write(f"// label {words[1]}\n({words[1]})\n\n")

        elif words[0] == "goto":
            asm_file.write(f"// goto {words[1]}\n@{words[1]}\nD;JMP\n\n")

        elif words[0] == "if-goto":
            asm_file.write(f"// if-goto {words[1]}\n@SP\nAM=M-1\nD=M\n@{words[1]}\nD;JNE\n\n")
        
        elif words[0] == "function":
            asm_file.write(f"// function {words[1]} {words[2]}\n({words[1]})\n\n")
            for i in range(int(words[2])):
                asm_file.write(f"@SP\nA=M\nM=0\n@SP\nM=M+1\n\n")
        elif words[0] == "return":
            asm_file.write(f"// return\n@LCL\nD=M\n@R13\nM=D\n@5\nA=D-A\nD=M\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n@R13\nAM=M-1\nD=M\n@THAT\nM=D\n@R13\nAM=M-1\nD=M\n@ARG\nM=D\n@R13\nAM=M-1\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP")
    
    asm_file.close()


def vm_2_hack():
    if len(sys.argv) != 2:
        print("Usage: python vm_2_hack.py <filename>")
        return
    
    filename = sys.argv[1]
    parsed_lines = parser(filename)
    code_writer(parsed_lines, filename.replace(".vm", ""))


vm_2_hack()