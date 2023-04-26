class TranslatorParser:
    def has_more_commands(self):
        return self.cur_ind < len(self.lines)

    def print_lines(self):
        return self.lines

    def next_command(self):
        next_com = self.lines[self.cur_ind]
        self.cur_ind += 1
        return next_com

    def get_arg1(self):
        ind = self.cur_ind - 1
        parsed_line = self.lines[ind]
        arg1 = parsed_line[1] if len(parsed_line) > 1 else parsed_line[0]
        return arg1

    def get_arg2(self):
        ind = self.cur_ind - 1
        parsed_line = self.lines[ind]
        arg2 = int(parsed_line[2]) if len(parsed_line) > 2 else -1
        return arg2

    def get_command_type(self):
        cur_com = self.lines[self.cur_ind-1][0]
        com_type = ""
        if len(self.lines[self.cur_ind-1]) == 1:
            if cur_com == "return":
                com_type = "C_RETURN"
            else:
                com_type = "C_ARITHMETIC"
        if cur_com == "push":
            com_type = "C_PUSH"
        if cur_com == "pop":
            com_type = "C_POP"
        return com_type

    def __create_line_list(self):
        f = open(self.filename, "r")
        for line in f:
            format_line = ""
            parsed_line = line.split(" ")
            for cur in parsed_line:
                if (cur == "//"):
                    break
                tmp = cur.find("\n")
                if tmp != -1:
                    cur = cur[:tmp]
                if len(cur) != 0:
                    format_line += cur + " "
            if len(format_line) > 0 and format_line[0] != '\n':
                self.lines.append(format_line[:-1].split(" "))
        f.close()

    def __init__(self, filename):
        self.filename = filename
        self.cur_ind = 0
        self.lines = []
        self.__create_line_list()