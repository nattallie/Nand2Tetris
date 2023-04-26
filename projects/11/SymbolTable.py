class SymbolTable:
    def define(self, name, typ, kind):
        if kind == 'static' or kind == 'field':
            self.class_table[name] = (typ, kind, self.indexes[kind])
        else:
            self.subroutine_table[name] = (typ, kind, self.indexes[kind])
        self.indexes[kind] += 1

    def var_count(self, kind):
        return self.indexes[kind]

    def kind_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name][1]
        if name in self.class_table:
            return self.class_table[name][1]
        return None

    def type_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name][0]
        if name in self.class_table:
            return self.class_table[name][0]
        return None

    def index_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name][2]
        if name in self.class_table:
            return self.class_table[name][2]
        return None

    def start_subroutine(self):
        self.subroutine_table = {}
        self.indexes['arg'] = 0
        self.indexes['var'] = 0

    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.indexes = {'static' : 0, 'field' : 0, 'arg' : 0, 'var' : 0}