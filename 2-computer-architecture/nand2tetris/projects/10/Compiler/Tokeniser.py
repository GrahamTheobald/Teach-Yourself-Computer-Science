import re

class Tokeniser:
    def __init__(self, jack):
        self.jack = jack
        self.xml = []

    SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '-', '~']

    SYMBOL_CONVERT = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

    KEYWORDS = ['class', 'method', 'function', 'constructor', 'int', 'boolean', 'char', 'void', 'var', 'static',
    'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']

    TYPES = {'KEYWORD': 'keyword', 'SYMBOL': 'symbol', 'IDENTIFIER': 'identifier', 
    'INT_CONST': 'integerConstant', 'STRING_CONST': 'stringConstant'}
    
    def tokenise(self):
        self.xml.append('<tokens>')
        with open(self.jack, 'r') as file:
            for line in file:
                words = re.findall(r'(?:[^\s"]|"(?:\\.|[^"])*")+', self.clean(line))
                if len(words) == 0:
                    continue
                for j in words:
                    tokens = self.extract_tokens(j)
                    for t in tokens:
                        type = self.token_type(t) 
                        self.xml.append(self.markup(type, t))
        self.xml.append('</tokens>')
        self.write_file()
    
    def write_file(self):
        file_name = self.jack[:-5] + 'T.xml' 
        with open(file_name, 'w') as file:
            file.write('\n'.join(self.xml))

    def clean(self, line):
        line = line.strip()
        index1 = line.find('//')
        index2 = line.find('/*')
        if index1 > -1:
            line = line[:index1]
        if index2 > -1:
            line = line[:index2]
        if len(line) > 0 and line[0] == '*':
            line = ''
        
        return line.strip()
    
    def markup(self, type, token):
        if type == self.TYPES['STRING_CONST']:
            token = token[1:-1]
        elif token in self.SYMBOL_CONVERT:
            token = self.SYMBOL_CONVERT[token]

        return f'<{type}> {token} </{type}>'

    def token_type(self, token):
        if token in self.KEYWORDS:
            return self.TYPES['KEYWORD']
        if token in self.SYMBOLS:
            return self.TYPES['SYMBOL']
        if token.isdigit():
            return self.TYPES['INT_CONST']
        if token[0] == '"' and token[-1] == '"':
            return self.TYPES['STRING_CONST']
        else:
            return self.TYPES['IDENTIFIER']

    def extract_tokens(self, jack):
        tokens = []
        li = 0
        for i, j in enumerate(jack):
            if j in self.SYMBOLS:
                tokens.append(jack[li:i])
                tokens.append(jack[i])
                li = i + 1
        tokens.append(jack[li:])
        return [i for i in tokens if i != '']
    

