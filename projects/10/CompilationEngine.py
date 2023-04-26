import os
from JackTokenizer import *

class CompilationEngine:
    variable_keys = 'static|field'
    subroutine_keys = 'constructor|function|method'
    op_keys = ['+', '-', '*', '/', '&', '<', '>', '=', '&lt;', '&gt;', '&amp;', '|']
    unary_op_keys = '-~'

    def begin_tag(self, tag):
        self.output_f.write('<' + tag + '>\n')
        self.tab_space += '\t'

    def end_tag(self, tag):
        self.tab_space = self.tab_space[:-1]
        self.output_f.write(self.tab_space + '</' + tag +'>\n')

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

    def write_several_token(self, n):
        for i in range(0,n):
            tok_type, tok_str = self.get_next_token()
            if tok_type and tok_str:
                self.write_token_xml(tok_type, tok_str)            

    def compile_class(self):
        self.begin_tag('class')
        self.write_several_token(3)

        tok_type, tok_str = self.get_next_token()

        while (tok_str != '}'):
            if tok_str in self.variable_keys:
                self.compile_var_dec('classVarDec')
            if tok_str in self.subroutine_keys:
                self.compile_subroutine()
            tok_type, tok_str = self.get_next_token()

        tok_type, tok_str = self.get_last_tok()
        if tok_type and tok_str:
            self.write_token_xml(tok_type, tok_str)
        
        self.end_tag('class')

    def compile_var_dec(self, tag):
        self.begin_tag(tag)

        if (self.tokenizer.get_token_type() == 'keyword'):
            self.write_token_xml('keyword', self.tokenizer.get_keyword())

        tok_type, tok_str = self.get_next_token()
        while (tok_str != ';'):
            self.write_token_xml(tok_type, tok_str)
            tok_type, tok_str = self.get_next_token()

        if tok_type and tok_str:
            self.write_token_xml(tok_type, tok_str)

        self.end_tag(tag)

    def compile_subroutine_dec(self):
        if self.tokenizer.get_token_type() == 'keyword':
            self.write_token_xml('keyword', self.tokenizer.get_keyword())
            self.write_several_token(3)

    def compile_subroutine_body(self):
        self.begin_tag('subroutineBody')
        tok_type, tok_str = self.get_next_token()
        if tok_str == '{':
            self.write_token_xml('symbol', '{')
        
        tok_type, tok_str = self.get_next_token()
        while (tok_str == 'var'):
            self.compile_var_dec('varDec')
            tok_type, tok_str = self.get_next_token()
        
        if tok_str != '}':
            self.compile_statements()

        tok_type, tok_str = self.get_last_tok()
        if tok_str == '}':
            self.write_token_xml('symbol', '}')    

        self.end_tag('subroutineBody')

    def compile_subroutine(self):
        self.begin_tag('subroutineDec')
        self.compile_subroutine_dec()
        self.compile_parameter_list()
        self.compile_subroutine_body()
        self.end_tag('subroutineDec')
        
    def compile_parameter_list(self):
        self.begin_tag('parameterList')

        tok_type, tok_str = self.get_next_token()

        while (tok_str != ')'):
            self.write_token_xml(tok_type, tok_str)
            tok_type, tok_str = self.get_next_token()

        self.end_tag('parameterList')
        
        if tok_type and tok_str:
            if (self.tokenizer.get_token_type() == 'symbol'):
                self.write_token_xml('symbol', self.tokenizer.get_symbol())

    def compile_statements(self):
        self.begin_tag('statements')
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

        self.end_tag('statements')

    def compile_do(self):
        self.begin_tag('doStatement')
        self.write_token_xml('keyword', 'do')
        self.write_several_token(2)
        self.compile_subroutine_call()
        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)
        self.end_tag('doStatement')

    def compile_let(self):
        self.begin_tag('letStatement')
        self.write_token_xml('keyword', 'let')

        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str == '[':
            self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
            self.compile_expression()
            tok_type, tok_str = self.get_last_tok()
            self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
        
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)
        self.get_next_token()
        self.compile_expression()
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)

        self.end_tag('letStatement')

    def compile_while(self):
        self.begin_tag('whileStatement')
        self.write_token_xml('keyword', 'while')
        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str != ')':
            self.compile_expression()
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)
        
        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str != '}':
            self.compile_statements()
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)

        self.end_tag('whileStatement')

    def compile_return(self):
        self.begin_tag('returnStatement')
        self.write_token_xml('keyword', 'return')
        tok_type, tok_str = self.get_next_token()
        if tok_str != ';':
            self.compile_expression()
        
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)
        self.end_tag('returnStatement')

    def compile_else(self):
        self.write_token_xml('keyword', 'else')
        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)
        self.get_next_token()
        self.compile_statements()
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)
        self.get_next_token()

    def compile_if(self):
        self.begin_tag('ifStatement')
        self.write_token_xml('keyword', 'if')
        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)
        self.get_next_token()
        self.compile_expression()
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str != '}':
            self.compile_statements()

        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)

        tok_type, tok_str = self.get_next_token()
        if tok_str == 'else':
            self.compile_else()

        self.end_tag('ifStatement')

    def compile_expression(self):
        self.begin_tag('expression')
        term_again = self.compile_term()
        while (term_again):
            tok_type, tok_str = 'symbol', self.tokenizer.get_symbol()
            self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
            term_again = self.compile_term()

        self.end_tag('expression')

    def get_last_tok(self):
        tok_type = self.tokenizer.get_token_type()
        tok_str = self.get_str_by_keyword(tok_type)
        return tok_type, tok_str

    def compile_subroutine_call(self):
        tok_type, tok_str = self.get_last_tok()
        if (tok_str == '.'):
            self.write_several_token(2)        
        self.compile_expression_list()
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)

    def identifier_in_term(self):
        tok_type, tok_str = self.get_next_token()
        if tok_str == '(' or tok_str == '.':
            self.write_token_xml('symbol', tok_str)
            self.compile_subroutine_call()
            self.get_next_token()
        elif tok_str == '[':
            self.write_token_xml('symbol', '[')
            self.get_next_token()
            self.compile_expression()
            tok_type, tok_str = self.get_last_tok()
            self.write_token_xml(tok_type, tok_str)
            self.get_next_token()
        elif tok_str in self.op_keys:
            self.end_tag('term')
            return True
        return False
        
    def compile_term(self):
        self.begin_tag('term')
        tok_type, tok_str = self.get_last_tok()
        self.write_token_xml(tok_type, tok_str)

        if tok_str in self.unary_op_keys:
            self.get_next_token()
            self.compile_term()
        elif tok_str == '(':
            self.get_next_token()
            self.compile_expression()
            tok_type, tok_str = self.get_last_tok()
            self.write_token_xml(tok_type, tok_str)
            tok_type, tok_str = self.get_next_token()
            if tok_str in self.op_keys:
                self.end_tag('term')
                return True
        elif tok_type == 'identifier':
            to_return = self.identifier_in_term()
            if (to_return):
                return True
        else:
            tok_type, tok_str = self.get_next_token()
            if tok_type and tok_str and tok_str in self.op_keys:
                self.end_tag('term')
                return True
        
        self.end_tag('term')
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
        self.begin_tag('expressionList')
        tok_type, tok_str = self.get_next_token()
        if tok_str != ')':
            self.compile_expression()
            tok_type, tok_str = self.get_last_tok()
            while (tok_str == ','):
                self.write_token_xml('symbol', ',')
                self.get_next_token()
                self.compile_expression()
                tok_type, tok_str = self.get_last_tok()

        self.end_tag('expressionList')   

    def write_token_xml(self, type_str, tok):
        self.output_f.write(self.tab_space + "<"+type_str+"> " + tok + " </" + type_str + ">\n")

    def __init__(self, input_name, output_name):
        self.tokenizer = JackTokenizer(input_name)
        self.output_f = open(output_name, "w")
        self.tab_space = ''