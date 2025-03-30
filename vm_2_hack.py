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

    parts5 = {
        "this": "@THIS\n",
        "that": "@THAT\n",
        "argument": "@ARG\n",
        "local": "@LCL\n",
        "temp": "@5\n",
        "pointer": "@3\n",
    }

    part3_label = -1

    for i in lines:
        words = i.split()
        if words[0] == "push":
            if words[1] == "constant":
                asm_file.write(f"// {words[0]} {words[1]} {words[2]}\n@{words[2]}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n\n")

        elif words[0] in sum:
            asm_file.write(f"// {words[0]}\n@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\n{sum[words[0]]}\n@SP\nM=M+1\n\n")

        elif words[0] in com:
            asm_file.write(f"// {words[0]}\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\n{com[words[0]]}\n\n")

        elif words[0] in neg:
            asm_file.write(f"// {words[0]}\n@SP\nA=M-1\n{neg[words[0]]}\n")

        elif words[0] in j:
            part3_label += 1
            asm_file.write(f"// {words[0]}\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@{words[0]}_True{part3_label}\n{j[words[0]]}\n@SP\nA=M-1\nM=0\n({words[0]}_True{part3_label})\n\n")
    
    asm_file.close()


def vm_2_hack():
    if len(sys.argv) != 2:
        print("Usage: python vm_2_hack.py <filename>")
        return
    
    filename = sys.argv[1]
    parsed_lines = parser(filename)
    code_writer(parsed_lines, filename.replace(".vm", ""))


vm_2_hack()