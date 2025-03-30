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
    counter = 0

    for i in lines:
        counter += 1
        words = i.split()
        if words[0] == "push":
            if words[1] == "constant":
                asm_file.write(f"@{words[2]}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1")
        elif words[0] == "add":
            asm_file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M")
        if counter != len(lines):
            asm_file.write("\n")
    
    asm_file.close()


def vm_2_hack():
    if len(sys.argv) != 2:
        print("Usage: python vm_2_hack.py <filename>")
        return
    
    filename = sys.argv[1]
    parsed_lines = parser(filename)
    code_writer(parsed_lines, filename.replace(".vm", ""))


vm_2_hack()