def parse(file_path):

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


def code_writer(lines):

    hack_code = []

    for i in lines:
        words = i.split()
        if words[0] == "push":
            if words[1] == "constant":
                hack_code.append(f"@{words[2]}")
                hack_code.append("D=A")
                hack_code.append("@SP")
                hack_code.append("A=M")
                hack_code.append("M=D")
                hack_code.append("@SP")
                hack_code.append("M=M+1")
        elif words[0] == "add":
            hack_code.append("@SP")
            hack_code.append("AM=M-1")
            hack_code.append("D=M")
            hack_code.append("A=A-1")
            hack_code.append("M=M+D")
        
    return hack_code


def vm_2_hack():
    lines = parse("SimpleAdd.vm")
    final_line = code_writer(lines)

    for i in final_line:
        print(i)


vm_2_hack()