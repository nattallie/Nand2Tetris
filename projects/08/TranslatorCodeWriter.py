import os

class TranslatorCodeWriter:
    def close(self):
        end_txt = "(END)\n" + \
                  "@END\n" + \
                  "0;JMP\n"
        self.output_f.write(end_txt)
        self.output_f.close()
    
    # returns x and y (M, D)
    def __get_x_y(self):
        asm_txt = self.__get_last_ind() 
        asm_txt += "D=M\n" + \
                   "A=A-1\n"    
        return asm_txt

    def __decrease_sp(self):
        asm_txt = "@R0\n" + \
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

    # returns last_ind (A)
    def __get_last_ind(self):
        asm_txt = "@R0\n"   
        asm_txt += "A=M-1\n" 
        return asm_txt

    def neg_asm(self):
        asm_txt = self.__get_last_ind()
        asm_txt += "M=-M\n"  
        return asm_txt

    def __with_jmp(self, label_name, jmp_com):
        asm_txt = "A=M-1\n" + \
                  "D=M\n" + \
                  "M=0\n"  + \
                  "@" + label_name.upper() + "_" + str(self.cnt) + "\n" + \
                  "D;" + jmp_com + "\n" + \
                  "@1\n" + \
                  "D=-A\n" + \
                  self.__get_last_ind() + \
                  "M=D\n" + \
                  "(" + label_name.upper() + "_" + str(self.cnt) + ")\n"
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
        asm_txt = self.__get_last_ind()
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
        asm_txt = "@"+ind+"\n"  + \
                  "D=A\n"  + \
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
        asm_txt = self.__get_last_ind() + \
                  "D=M\n" + \
                  "@top_val\n" + \
                  "M=D\n"
        return asm_txt

    def __pop_top_to(self):
        asm_txt = "D=A\n" + \
                  "@top_to\n" + \
                  "M=D\n" + \
                  "@top_val\n" + \
                  "D=M\n" + \
                  "@top_to\n" + \
                  "A=M\n" + \
                  "M=D\n"
        return asm_txt

    def write_push_pop(self, command, seg, ind):
        asm_txt = ""
        if command == "pop":
            asm_txt += self.__get_top_value()
            asm_txt += self.__decrease_sp()
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
            filename = self.func_names[-1].split(".")[0]
            asm_txt += "@"+filename+"_"+ind+"\n"

        if seg != "constant":
            if command == "push":
                asm_txt += self.__push_top("M")
            else:
                asm_txt += self.__pop_top_to()
        self.output_f.write(asm_txt)

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

    def __push_locals(self, func_name, num_loc):
        asm_txt = "@"+num_loc+"\n" + \
                  "D=A\n" + \
                  "@" + func_name.lower() + "_num_loc\n" + \
                  "M=D\n" + \
                  "@" + func_name.upper() + "_LOCAL_LOOP_END\n" + \
                  "D;JLE\n" + \
                  "(" + func_name.upper() + "_LOCAL_LOOP)\n"
        self.output_f.write(asm_txt)
        self.write_push_pop("push", "constant", 0)
        asm_txt = "@" + func_name.lower() + "_num_loc\n" + \
                   "M=M-1\n" + \
                   "D=M\n" + \
                   "@" + func_name.upper() + "_LOCAL_LOOP\n" + \
                   "D;JGT\n" + \
                   "(" + func_name.upper() + "_LOCAL_LOOP_END)\n"
        self.output_f.write(asm_txt)


    def write_function(self, func_name, num_loc):
        self.func_names.append(func_name)
        self.write_label(func_name.upper())
        self.__push_locals(func_name, num_loc)

    def __save_variable(self, var_name):
        asm_txt = "D=A\n" + \
                  "@"+var_name+"\n" + \
                  "M=D\n"
        return asm_txt

    def __set_min_ind(self, ind, reg):
        asm_txt = "@" + ind + "\n" + \
                  "A=-A\n" + \
                  "D=A\n" + \
                  "@"+reg+"\n" + \
                  "A=M+D\n" + \
                  "A=M\n"
        return asm_txt

    def __rewrite_reg(self, var_name, ind, reg):
        asm_txt = ""
        if ind[0] != "-":
            asm_txt = self.__count_from_base(ind, reg)
        else:
            asm_txt = self.__set_min_ind(ind[1:], reg)
        asm_txt += self.__save_variable(var_name)
        return asm_txt

    def write_return(self):
        asm_txt = self.__rewrite_reg("frame", "0", "R1") + \
                   self.__rewrite_reg("ret_"+self.func_names[-1].lower()+ "_" + str(self.cnt), "-5", "frame")
        self.output_f.write(asm_txt)
        self.write_push_pop("pop", "argument", "0")
        asm_txt = self.__rewrite_reg("R0", "1", "R2") + \
                   self.__rewrite_reg("R4", "-1", "frame") + \
                   self.__rewrite_reg("R3", "-2", "frame") + \
                   self.__rewrite_reg("R2", "-3", "frame") + \
                   self.__rewrite_reg("R1", "-4", "frame") + \
                   "@ret_"+self.func_names[-1].lower() + "_"+ str(self.cnt)+ "\n" + \
                   "A=M\n" + \
                   "0;JMP\n"
        self.cnt += 1
        self.func_names.pop()
        self.output_f.write(asm_txt)

    def write_if(self, label_name):
        asm_txt = self.__get_top_value() + \
                  self.__decrease_sp() + \
                  "@top_val\n" + \
                  "D=M\n" + \
                  "@" + label_name.upper() + "\n" + \
                  "D;JNE\n"
        self.output_f.write(asm_txt)    
    
    def write_goto(self, label_name):
        asm_txt = "@" + label_name.upper() + "\n"
        asm_txt += "0;JMP\n"
        self.output_f.write(asm_txt)

    def __push_attributes(self, reg):
        asm_txt = "@"+reg + "\n"
        asm_txt += self.__push_top("M")
        return asm_txt

    def __change_attributes(self, reg1, ind, reg2):
        asm_txt = ""
        if ind[0] == "-":
            asm_txt += "@" + ind[1:]+"\n"
            asm_txt += "A=-A\n"
        else:
            asm_txt += "@" +ind + "\n"
        asm_txt += "D=A\n" + \
                   "@"+reg2+"\n" + \
                   "D=M+D\n" + \
                   "@" + reg1 + "\n" + \
                   "M=D\n"
        return asm_txt
        

    def write_call(self, func_name, num_args):
        asm_txt = "@" + func_name.lower() + "_ret_" + str(self.cnt) + "\n"
        asm_txt += self.__push_top("A")
        asm_txt += self.__push_attributes("R1")
        asm_txt += self.__push_attributes("R2")
        asm_txt += self.__push_attributes("R3")
        asm_txt += self.__push_attributes("R4")
        tmp_ind = -1 * (int(num_args) + 5)
        asm_txt += self.__change_attributes("R2", str(tmp_ind), "R0")
        asm_txt += self.__change_attributes("R1", "0", "R0")
        self.output_f.write(asm_txt)
        self.write_goto(func_name)
        self.write_label(func_name.lower() + "_ret_" + str(self.cnt))
        self.cnt += 1

    def write_label(self, label_name):
        self.output_f.write("("+label_name+")\n")

    def set_filename(self, name):
        self.func_names = [name.split("/")[-1][:-3]]
        self.cnt = 0

    def __init_VM(self, ls_path):
        sys_path = ""
        for cur in ls_path:
            sys_path += cur + "/"
        sys_path += "Sys.vm"
        if os.path.isfile(sys_path):
            init_com = "@256\n"
            init_com += "D=A\n"
            init_com += "@R0\n"
            init_com += "M=D\n"
            self.output_f.write(init_com)
            self.write_call("Sys.init", "0")


    def __init__(self, filename):
        self.output_f = open(filename, "w")
        self.cnt = 0
        self.__init_VM(filename.split("/")[:-1])