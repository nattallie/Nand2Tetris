import os
from JackTokenizer import *
from SymbolTable import *
from VMWriter import *

class CompilationEngine:
    variable_keys = 'static|field'
    subroutine_keys = 'constructor|function|method'
    op_keys = ['+', '-', '*', '/', '&', '<', '>', '=', '&lt;', '&gt;', '&amp;', '|']
    unary_op_keys = '-~'

    def get_next_token(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.next_token()
            tok_type, tok_str = self.tokenizer.get_token_type(), ''
            if (tok_type == 'keyword'):
                tok_str = self.tokenizer.get_keyword()
            elif (tok_type == 'symbol'):
                tok_str = self.tokenizer.get_symbol()
            elif (tok_type == 'identifier'):
                tok_str = self.tokenizer.get_identifier()
            elif (tok_type == 'integerConstant'):
                tok_str = str(self.tokenizer.get_int_val())
            elif (tok_type == 'stringConstant'):
                tok_str = self.tokenizer.get_str_val()
            return tok_type, tok_str
        else:
            return None, None

    def skip_several_token(self, n):
        for i in range(0,n):
            tok_type, tok_str = self.get_next_token()

    def create_class_self(self):
        pass        

    def compile_class(self):
        self.skip_several_token(2)
        self.class_name = self.tokenizer.get_identifier()
        # self.write_token_xml('class_name', self.class_name)
        # self.write_several_token(1)
        self.skip_several_token(1)

        tok_type, tok_str = self.get_next_token()

        while (tok_str != '}'):
            if tok_str in self.variable_keys:
                print("classVarDectan")
                self.compile_var_dec('classVarDec')
            if tok_str in self.subroutine_keys:
                self.compile_subroutine()
            tok_type, tok_str = self.get_next_token()

        # tok_type, tok_str = self.get_last_tok()
        # if tok_type and tok_str:
        #     self.write_token_xml(tok_type, tok_str)
        
        # self.end_tag('class')

    def compile_var_dec(self, tag):
        kind, typ = '', ''
        if (self.tokenizer.get_token_type() == 'keyword'):
            # self.write_token_xml('keyword', self.tokenizer.get_keyword())
            kind = self.tokenizer.get_keyword()

        tok_type, tok_str = self.get_next_token()
        if (tok_str != ';'):
            typ = tok_str
            while (tok_str != ';'):
                # self.write_token_xml(tok_type, tok_str)
                tok_type, tok_str = self.get_next_token()
                if tok_type != 'symbol':
                    self.table.define(tok_str, typ, kind)
                    # self.write_token_xml(self.table.type_of(tok_str) + ' ' + self.table.kind_of(tok_str) + ' ' + str(self.table.index_of(tok_str)) + ' define', tok_str)

        # if tok_type and tok_str:
        #     self.write_token_xml(tok_type, tok_str)

        # self.end_tag(tag)

    def compile_subroutine_dec(self):
        if self.tokenizer.get_token_type() == 'keyword':
            # self.write_token_xml('keyword', self.tokenizer.get_keyword())
            self.cur_subroutine['keyword'] = self.get_last_tok()[1]
            self.cur_subroutine['return_type'] = self.get_next_token()[1]
            # self.skip_several_token(2)
            # self.write_token_xml('subroutine name', self.class_name + '.' + self.tokenizer.get_identifier())
            self.cur_subroutine['name'] = self.class_name + '.' + self.get_next_token()[1]
            self.table.start_subroutine()
            self.skip_several_token(1)

    def compile_subroutine_body(self):
        tok_type, tok_str = self.get_next_token()
        # if tok_str == '{':
        #     self.write_token_xml('symbol', '{')
        
        tok_type, tok_str = self.get_next_token()
        while (tok_str == 'var'):
            self.compile_var_dec('varDec')
            tok_type, tok_str = self.get_next_token()
        
        # self.write_token_xml('local cnt ' + self.class_name + '.' + self.cur_subroutine, str(self.table.var_count('var')))

        self.writer.write_function(self.cur_subroutine['name'], self.table.var_count('var'))
        if tok_str != '}':
            self.compile_statements()

        tok_type, tok_str = self.get_last_tok()
        # if tok_str == '}':
        #     self.write_token_xml('symbol', '}')    

    def compile_subroutine(self):
        self.compile_subroutine_dec()
        self.compile_parameter_list()
        self.compile_subroutine_body()
        
    def compile_parameter_list(self):
        tok_type, tok_str = self.get_next_token()

        typ = tok_str
        i = 0
        while (tok_str != ')'):
            # self.write_token_xml(tok_type, tok_str)
            if (i % 3 == 0):
                typ = tok_str
            elif (i % 3 == 1):
                self.table.define(tok_str, typ, 'arg')
                # self.write_token_xml(self.table.type_of(tok_str) + ' ' + self.table.kind_of(tok_str) + ' ' + str(self.table.index_of(tok_str)) + ' arg', tok_str)
            tok_type, tok_str = self.get_next_token()
            i += 1
        
        
        # if tok_type and tok_str:
        #     if (self.tokenizer.get_token_type() == 'symbol'):
                # self.write_token_xml('symbol', self.tokenizer.get_symbol())

    def compile_statements(self):
        tok_type, tok_str = '', '}'
        if (self.tokenizer.get_token_type() == 'keyword'):
            tok_type, tok_str = 'keyword', self.tokenizer.get_keyword()

        while (tok_str != '}'):
            if tok_str == 'let':
                self.compile_let()
            if tok_str == 'if':
                self.compile_if()
            if tok_str == 'while':
                self.compile_while()
            if tok_str == 'do':
                self.compile_do()
            if tok_str == 'return':
                self.compile_return()
            if tok_str != 'if':
                tok_type, tok_str = self.get_next_token()    
            else:
                tok_type, tok_str = self.get_last_tok()


    def compile_do(self):
        # self.write_token_xml('keyword', 'do')
        self.skip_several_token(1)
        id = self.get_last_tok()[1]
        self.skip_several_token(1)

        tok_type, tok_str = self.get_last_tok()
        if tok_str == '(':
            self.call_subroutine = self.class_name + '.' + id
            # self.write_token_xml('subroutine call', self.class_name + '.' + id)
            pass
        elif tok_str == '.':
            id_type = self.table.type_of(id)
            if id_type:
                self.call_subroutine = id_type
                # self.write_token_xml(' subroutine class in Call', id_type)
            else:
                self.call_subroutine = id
                # self.write_token_xml('subroutine call class', id)

        self.compile_subroutine_call()
        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)

    def compile_let(self):
        # self.write_token_xml('keyword', 'let')

        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)

        # self.write_token_xml(self.table.type_of(tok_str) + ' ' + self.table.kind_of(tok_str) + ' ' + str(self.table.index_of(tok_str)) + ' used', tok_type)

        tok_type, tok_str = self.get_next_token()
        if tok_str == '[':
            # self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
            self.compile_expression(False)
            tok_type, tok_str = self.get_last_tok()
            # self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
        
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)
        self.get_next_token()
        self.compile_expression(False)
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)


    def compile_while(self):
        # self.write_token_xml('keyword', 'while')
        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str != ')':
            self.compile_expression(False)
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)
        
        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str != '}':
            self.compile_statements()
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)


    def compile_return(self):
        # self.write_token_xml('keyword', 'return')
        tok_type, tok_str = self.get_next_token()
        if tok_str != ';':
            self.compile_expression(False)
        else:
            self.writer.write_push('constant', '0')
            
        self.writer.write_return()
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)

    def compile_else(self):
        # self.write_token_xml('keyword', 'else')
        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)
        self.get_next_token()
        self.compile_statements()
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)
        self.get_next_token()

    def compile_if(self):
        # self.write_token_xml('keyword', 'if')
        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)
        self.get_next_token()
        self.compile_expression(False)
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        # self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str != '}':
            self.compile_statements()

        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str == 'else':
            self.compile_else()


    def compile_expression(self, is_in_list):
        term_again = self.compile_term(is_in_list)
        last_op = None
        while (term_again):
            tok_type, tok_str = 'symbol', self.tokenizer.get_symbol()
            # self.write_token_xml(tok_type, tok_str)
            if tok_str in self.op_keys:
                last_op = tok_str
            self.get_next_token()
            term_again = self.compile_term(is_in_list)
            self.writer.write_arithmetic(tok_str)


    def get_last_tok(self):
        tok_type = self.tokenizer.get_token_type()
        tok_str = self.get_str_by_keyword(tok_type)
        return tok_type, tok_str

    def compile_subroutine_call(self):
        tok_type, tok_str = self.get_last_tok()
        if (tok_str == '.'):
            self.skip_several_token(1)
            id = self.get_last_tok()[1]
            self.call_subroutine += '.' + id
            # self.write_token_xml('subroutine name in call', id)
            self.skip_several_token(1)
        self.compile_expression_list()
        tok_type, tok_str = self.get_last_tok()
        # self.write_token_xml(tok_type, tok_str)

    def identifier_in_term(self):
        id = self.get_last_tok()[1]
        tok_type, tok_str = self.get_next_token()
        if tok_str == '(' or tok_str == '.':
            if tok_str == '(':
                pass
                # self.write_token_xml('subroutine call', self.class_name + '.' + id)
            else:
                id_type = self.table.type_of(id)
                if id_type:
                    pass
                    # self.write_token_xml(' subroutine class in Call', id_type)
                else:
                    pass
                    # self.write_token_xml('subroutine call class', id)
            # self.write_token_xml('symbol', tok_str)
            self.compile_subroutine_call()
            self.get_next_token()
        elif tok_str == '[':
            # self.write_token_xml(self.table.type_of(id) + ' ' + self.table.kind_of(id) + ' ' + str(self.table.index_of(id)) + ' used', id)
            # self.write_token_xml('symbol', '[')
            self.get_next_token()
            self.compile_expression(False)
            tok_type, tok_str = self.get_last_tok()
            # self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
        else:
            # self.write_token_xml(self.table.type_of(id) + ' ' + self.table.kind_of(id) + ' ' + str(self.table.index_of(id)) + ' used', id)
            if tok_str in self.op_keys:
                # self.end_tag('term')
                return True
        return False
        
    def compile_term(self, is_in_list):
        tok_type, tok_str = self.get_last_tok()
        if is_in_list:
            if tok_type == 'identifier':
                pass
                # self.write_token_xml(self.table.type_of(tok_str) + ' ' + self.table.kind_of(tok_str) + ' ' + str(self.table.index_of(tok_str)) + ' used', 'identifier')
            elif tok_type == 'integerConstant':
                self.writer.write_push('constant', tok_str)
                # self.write_token_xml(tok_str +  ' arg', 'const')
            elif tok_str in self.op_keys:
                op = self.get_next_token()[1]
                self.compile_term(is_in_list)
                # self.writer.write_push()

        if tok_str in self.unary_op_keys:
            self.get_next_token()
            self.compile_term(is_in_list)
        elif tok_str == '(':
            self.get_next_token()
            self.compile_expression(is_in_list)
            tok_type, tok_str = self.get_last_tok()
            # self.write_token_xml(tok_type, tok_str)
            tok_type, tok_str = self.get_next_token()
            if tok_str in self.op_keys:
                # self.end_tag('term')
                return True
        elif tok_type == 'identifier':
            to_return = self.identifier_in_term()
            if (to_return):
                return True
        else:
            tok_type, tok_str = self.get_next_token()
            if tok_str in self.op_keys:
                # self.end_tag('term')
                return True
        
        return False

    def get_str_by_keyword(self, tok_type):
        tok_str = ''
        if tok_type == 'keyword':
            tok_str = self.tokenizer.get_keyword()
        elif tok_type == 'identifier':
            tok_str = self.tokenizer.get_identifier()
        elif tok_type == 'integerConstant':
            tok_str = str(self.tokenizer.get_int_val())
        elif tok_type == 'stringConstant':
            tok_str = self.tokenizer.get_str_val()
        else:
            tok_str = self.tokenizer.get_symbol()
        return tok_str

    def compile_expression_list(self):
        tok_type, tok_str = self.get_next_token()
        cnt = 0
        if tok_str != ')':
            self.compile_expression(True)
            cnt += 1
            tok_type, tok_str = self.get_last_tok()
            while (tok_str == ','):
                # self.write_token_xml('symbol', ',')
                self.get_next_token()
                self.compile_expression(True)
                tok_type, tok_str = self.get_last_tok()
                cnt += 1
        self.writer.write_call(self.call_subroutine, cnt)
        self.writer.write_pop('temp', '0')


    # def write_token_xml(self, type_str, tok):
    #     self.output_f.write(self.tab_space + "<"+type_str+"> " + tok + " </" + type_str + ">\n")

    def __init__(self, input_name, output_name):
        self.tokenizer = JackTokenizer(input_name)
        self.class_name = input_name.split("/")[-1]
        self.writer = VMWriter(output_name)
        self.call_subroutine = ''
        self.cur_subroutine = {}
        self.table = SymbolTable()