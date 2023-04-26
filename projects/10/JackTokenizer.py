import re

class JackTokenizer:
    endofline_com_pat = '//.*\n'

    multiline_com_pat = '/\*.*?\*/'
    
    whitespaces_pat = '[\t\r\f\v]'

    keywords_pat = '(class|constructor|function|method|field|static|var|int|char|boolean' + \
                   '|void|true|false|null|this|let|do|if|else|while|return)' 
    
    symbol_pat = '([{}()[\].,;+\-*/&|<>=~])'

    str_cons_pat = '(\"[^\n]*\")'

    int_cons_pat = '(\d+)'

    id_pat = '([a-zA-Z]_*\w*)'

    types = ['keyword', 'symbol', 'identifier', 'integerConstant', 'stringConstant']

    def has_more_tokens(self):
        return self.cur_ind < len(self.tokens)

    def next_token(self):
        if not self.has_more_tokens():
            return None
        next_token = self.tokens[self.cur_ind][0]
        self.cur_ind += 1
        return next_token

    def get_token_type(self):
        return self.tokens[self.cur_ind - 1][1]

    def get_keyword(self):
        if self.get_token_type() == 'keyword':
            return self.tokens[self.cur_ind-1][0]
        return None

    def get_symbol(self):
        if self.get_token_type() == 'symbol':
            sym = self.tokens[self.cur_ind-1][0]
            if (sym == '<'):
                sym = '&lt;'
            if (sym == '>'):
                sym = '&gt;'
            if (sym == '&'):
                sym = '&amp;'
            return sym
        return None

    def get_identifier(self):
        if self.get_token_type() == 'identifier':
            return (self.tokens[self.cur_ind-1][0])
        return None

    def get_int_val(self):
        if self.get_token_type() == 'integerConstant':
            return int(self.tokens[self.cur_ind-1][0])
        return None

    def get_str_val(self):
        if self.get_token_type() == 'stringConstant':
            return self.tokens[self.cur_ind-1][0][1:-1]
        return None


    def __create_token_list(self):
        all_pattern = '{}|{}|{}|{}|{}'.format(self.keywords_pat, self.symbol_pat, self.id_pat, self.int_cons_pat, self.str_cons_pat)
        raw_tokens = re.findall(all_pattern, self.file_txt)
        for cur_tok in raw_tokens:
            for i in range(0, 5):
                if len(cur_tok[i]) > 0:
                    self.tokens.append((cur_tok[i], self.types[i]))

    # clears whole text from multiline and inline comments
    # and whitespaces
    def __clear_txt_from_extras(self):
        self.file_txt = re.sub(self.multiline_com_pat, '', self.file_txt, flags=re.DOTALL)
        self.file_txt = re.sub(self.endofline_com_pat, '\n', self.file_txt)
        self.file_txt = re.sub(self.whitespaces_pat, '', self.file_txt)


    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.cur_ind = 0
        with open(self.filename, "r") as f:
            self.file_txt = f.read()
        self.__clear_txt_from_extras()
        self.__create_token_list()