class TranslatorCodeWriter:
    def close(self):
        end_txt = "(END)\n" + \
                  "@END\n" + \
                  "0;JMP\n"
        self.output_f.write(end_txt)
        self.output_f.close()
    
    # returns x and y (M, D)
    def __get_x_y(self):
        asm_txt = "@R0\n" +  \
                  "A=M-1\n" + \
                  "D=M\n"  + \
                  "A=A-1\n"    
        return asm_txt

    def __decrease_sp(self):
        asm_txt = "@R0\n" +\
                  "M=M-1\n"
        return asm_txt

    def add_asm(self):
        asm_txt = self.__get_x_y()
        asm_txt += "M=M+D\n"    
        asm_txt += self.__decrease_sp()
        return asm_txt

    def sub_asm(self):
        asm_txt = self.__get_x_y()
        asm_txt += "M=M-D\n"    
        asm_txt += self.__decrease_sp()
        return asm_txt      

    # returns X (M)
    def __get_x(self):
        asm_txt = "@R0\n"  + \
                  "A=M-1\n" 
        return asm_txt

    def neg_asm(self):
        asm_txt = self.__get_x()
        asm_txt += "M=-M\n"  
        return asm_txt

    def __with_jmp(self, label_name, jmp_com):
        asm_txt = "A=M-1\n" + \
                  "D=M\n"  + \
                  "M=0\n"  + \
                  "@" + label_name + str(self.cnt) + "\n" + \
                  "D;" + jmp_com + "\n" + \
                  "@1\n" + \
                  "D=-A\n" + \
                  "@R0\n" + \
                  "A=M-1\n" + \
                  "M=D\n"  + \
                  "(" + label_name + str(self.cnt) + ")\n"
        self.cnt += 1
        return asm_txt

    def eq_asm(self):
        asm_txt = self.sub_asm()
        asm_txt += self.__with_jmp("NOT_EQUAL", "JNE")
        return asm_txt

    def gt_asm(self):
        asm_txt = self.sub_asm()
        asm_txt += self.__with_jmp("NOT_GREATER", "JLE")
        return asm_txt

    def lt_asm(self):
        asm_txt = self.sub_asm()
        asm_txt += self.__with_jmp("NOT_LESS", "JGE")
        return asm_txt

    def and_asm(self):
        asm_txt = self.__get_x_y()
        asm_txt += "M=M&D\n"
        asm_txt += self.__decrease_sp()
        return asm_txt

    def or_asm(self):
        asm_txt = self.__get_x_y()
        asm_txt += "M=M|D\n"
        asm_txt += self.__decrease_sp()
        return asm_txt

    def not_asm(self):
        asm_txt = self.__get_x()
        asm_txt += "M=!M\n"
        return asm_txt

    def __push_top(self, reg):
        asm_txt = "D=" + reg + "\n" + \
                  "@R0\n" + \
                  "A=M\n" + \
                  "M=D\n" + \
                  "@R0\n" + \
                  "M=M+1\n"
        return asm_txt

    def __count_from_base(self, ind, reg):
        asm_txt = "@"+ind+"\n" + \
                  "D=A\n" + \
                  "@"+reg+"\n" + \
                  "A=M+D\n"
        return asm_txt

    def __count_from_ram(self, ram, ind):
        asm_txt = "@"+ind+"\n" + \
                  "D=A\n" + \
                  "@"+ram+"\n" + \
                  "A=A+D\n"
        return asm_txt

    def __get_top_value(self):
        asm_txt = "@R0\n" + \
                  "A=M-1\n" + \
                  "D=M\n" + \
                  "@val\n" + \
                  "M=D\n" + \
                  "@R0\n" + \
                  "M=M-1\n" 
        return asm_txt

    def __pop_top_to(self):
        asm_txt = "D=A\n" + \
                  "@top_to\n" + \
                  "M=D\n" + \
                  "@val\n" + \
                  "D=M\n" + \
                  "@top_to\n" + \
                  "A=M\n" + \
                  "M=D\n"
        return asm_txt

    def write_push_pop(self, command, seg, ind):
        asm_txt = ""
        if command == "pop":
            asm_txt += self.__get_top_value()
        if seg == "constant":
            asm_txt += "@" + str(ind) + "\n"
            asm_txt += self.__push_top("A")
        if seg == "local":
            asm_txt += self.__count_from_base(ind, "R1")
        if seg == "argument":
            asm_txt += self.__count_from_base(ind, "R2")
        if seg == "this":
            asm_txt += self.__count_from_base(ind, "R3")
        if seg == "that":
            asm_txt += self.__count_from_base(ind, "R4")
        if seg == "pointer":
            asm_txt += self.__count_from_ram("3", ind)
        if seg == "temp":
            asm_txt += self.__count_from_ram("5", ind)
        if seg == "static":
            asm_txt += "@"+self.file_name+ind+"\n"

        if seg != "constant":
            if command == "push":
                asm_txt += self.__push_top("M")
            else:
                asm_txt += self.__pop_top_to()
        self.output_f.write(asm_txt)

    def set_filename(self, name):
        self.func_names = [name.split("/")[-1][:-3]]
        self.cnt = 0

    def write_arithmetic(self, command):
        asm_txt = ""
        if (command == "add"):
            asm_txt = self.add_asm()
        if (command == "sub"):
            asm_txt = self.sub_asm()
        if (command == "neg"):
            asm_txt = self.neg_asm()
        if (command == "eq"):
            asm_txt = self.eq_asm()
        if (command == "gt"):
            asm_txt = self.gt_asm()
        if (command == "lt"):
            asm_txt = self.lt_asm()
        if (command == "and"):
            asm_txt = self.and_asm()
        if (command == "or"):
            asm_txt = self.or_asm()
        if (command == "not"):
            asm_txt = self.not_asm()
        self.output_f.write(asm_txt)

    def __init__(self, filename):
        self.output_f = open(filename, "w")
        self.file_name = filename.split("/")[-1][:-3]
        self.cnt = 0