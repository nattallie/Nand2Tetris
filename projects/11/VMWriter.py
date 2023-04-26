class VMWriter:
    op_names = {'+' : 'add', '-' : 'sub', '&' : 'and', '<' : 'lt', '>' : 'gt', '&lt;' : 'lt', '&gt;' : 'gt', '&amp;' : 'and', '|' : 'or', 'neg' : 'neg', 'not' : 'not', '=' : 'eq'}

    def write_push(self, segment, index):
        self.output_f.write('push ' + segment + ' ' + index + '\n')

    def write_pop(self, segment, index):
        self.output_f.write('pop ' + segment + ' ' + index + '\n')

    def write_arithmetic(self, command):
        if command in self.op_names:
            self.output_f.write(self.op_names[command] + '\n')
        elif command == '*':
            self.write_call('Math.multiply', '2')
        elif command == '/':
            self.write_call('Math.divide', '2')

    def write_label(self, label):
        self.output_f.write('label ' + label + '\n')

    def write_goto(self, label):
        self.output_f.write('goto ' + label + '\n')

    def write_if(self, label):
        self.output_f.write('if-goto ' + label + '\n')

    def write_call(self, name, n_args):
        self.output_f.write('call ' + name + ' ' + str(n_args) + '\n')

    def write_function(self, name, n_locals):
        self.output_f.write('function ' + name + ' ' + str(n_locals) + '\n')

    def write_return(self):
        self.output_f.write('return' + '\n')

    def close(self):
        self.output_f.close()

    def __init__(self, output_name):
        self.output_f = open(output_name, "w")