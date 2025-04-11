# call with "python vm_2_hack.py <filename>.vm or <folder>"

import sys
import os  # Add import for handling directories

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
        "local": "@LCL\nD=D+A",
        "temp": "@5\nD=D+A",
        "pointer": "@3\nD=D+A",
    }

    j_counter = -1
    call_counter = 0  # Counter to generate unique return labels

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
            asm_file.write(f"// return\n@LCL\nD=M\n@R13\nM=D\n@5\nA=D-A\nD=M\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n@R13\nAM=M-1\nD=M\n@THAT\nM=D\n@R13\nAM=M-1\nD=M\n@THIS\nM=D\n@R13\nAM=M-1\nD=M\n@ARG\nM=D\n@R13\nAM=M-1\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP\n\n")
        elif words[0] == "call":
            call_counter += 1
            return_label = f"{words[1]}_return{call_counter}"
            asm_file.write(f"// call {words[1]} {words[2]}\n")
            asm_file.write(f"@{return_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")  # Push return address
            asm_file.write(f"@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")  # Push LCL
            asm_file.write(f"@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")  # Push ARG
            asm_file.write(f"@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")  # Push THIS
            asm_file.write(f"@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")  # Push THAT
            asm_file.write(f"@SP\nD=M\n@5\nD=D-A\n@{words[2]}\nD=D-A\n@ARG\nM=D\n")  # Reposition ARG
            asm_file.write(f"@SP\nD=M\n@LCL\nM=D\n")  # Reposition LCL
            asm_file.write(f"@{words[1]}\n0;JMP\n")  # Transfer control
            asm_file.write(f"({return_label})\n")  # Declare return label
    
    asm_file.close()


def vm_2_hack():
    if len(sys.argv) != 2:
        print("Usage: python vm_2_hack.py <filename>.vm or <folder>")
        return
    
    input_path = sys.argv[1]
    
    if os.path.isfile(input_path) and input_path.endswith(".vm"):
        # Single .vm file
        filename = os.path.basename(input_path).replace(".vm", "")
        parsed_lines = parser(input_path)
        code_writer(parsed_lines, filename)
    elif os.path.isdir(input_path):
        # Directory containing .vm files
        folder_name = os.path.basename(os.path.normpath(input_path))
        output_file = os.path.join(os.path.dirname(__file__), f"{folder_name}.asm")
        asm_file = open(output_file, "w")  # Create/overwrite the output .asm file
        asm_file.close()
        
        for vm_file in os.listdir(input_path):
            if vm_file.endswith(".vm"):
                vm_file_path = os.path.join(input_path, vm_file)
                parsed_lines = parser(vm_file_path)
                code_writer(parsed_lines, output_file.replace(".asm", ""))
    else:
        print("Invalid input. Provide a .vm file or a folder containing .vm files.")


vm_2_hack()