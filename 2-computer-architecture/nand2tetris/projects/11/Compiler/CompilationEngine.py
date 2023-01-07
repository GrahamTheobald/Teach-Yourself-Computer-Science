from SymbolTable import SymbolTable

class CompilationEngine:
    def __init__(self, input):
        self.inputXML1 = input
        self.inputXML = input
        self.outputXML = []
        self.symbolTable = SymbolTable()

    TYPES = {'KEYWORD': '<keyword>', 'SYMBOL': '<symbol>', 'IDENTIFIER': '<identifier>', 
    'INT_CONST': '<integerConstant>', 'STRING_CONST': '<stringConstant>'}

    ClassSVarDEC = ['static', 'field']
    SubroutineDEC = ['constructor', 'method', 'function']
    Types = ['int', 'char', 'boolean']
    Statements = ['let', 'if', 'while', 'do', 'return']
    OPS = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
    UnaryOPS = ['-', '~']
    TermTags = ['<integerConstant>', '<stringConstant>']
    KeyWordConstants = ['true', 'false', 'null', 'this']

    SymbolTableTags = {'var': '<var/>', 'arg': '<argument/>', 'static': '<static/>', 
            'field': '<field/>', 'class': '<class/>', 'subroutine': '<subroutine/>'}
    ClassTableCount = {}
    SubroutineTableCount = {}
    

    def compile(self):
        next_token = self.inputXML.pop(0)
        _, token , _ = self.split_tokens(next_token)
        if token  == 'class':
            self.compile_class(next_token)
    
    def write_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write('\n'.join(self.outputXML))
        
    def compile_class(self, next_token):
        '''
        creates relevent xml tags and when all of the required elements in the rules array are True the rest of the tokens are returned to be compiled recursively
        '''
        TAG = {'OPEN': '<class>', 'CLOSE': '</class>'}
        rules = [
            ['class', True],
            [self.TYPES['IDENTIFIER'], False],
            ['{', False],
            [self.ClassSVarDEC, False],
            [self.SubroutineDEC, False],
            ['}', False],
        ]

        self.ClassTableCount = {}

        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[1][0]:
            rules[1][1] = True
            next__token = self.compile_identifier(token, 'class', 'class')
            self.outputXML.append(next__token)
        else:
            self.error(token)
       
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[2][0]:
            rules[2][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)

        while not rules[3][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token in rules[3][0]:
                self.compile_class_vardec(next_token)
            elif token in rules[4][0]:
                rules[3][1] = True
                self.compile_subroutine(next_token)
            elif token == rules[5][0]:
                rules[3][1] = True
                rules[4][1] = True
                rules[5][1] = True
                self.outputXML.append(next_token)
            else:
                self.error(token)

        while not rules[4][1]:       
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token in rules[4][0]:
                self.compile_subroutine(next_token)
            elif token == rules[5][0]:
                rules[4][1] = True
                rules[5][1] = True
                self.outputXML.append(next_token)
            else:
                self.error(token)
        
        self.outputXML.append(TAG['CLOSE'])


    def compile_class_vardec(self, next_token):
        TAG = {'OPEN': '<classVarDec>', 'CLOSE': '</classVarDec>'}
        rules = [
            [self.ClassSVarDEC, True],
            [self.Types, False],
            [self.TYPES['IDENTIFIER'], False],
            [[',', self.TYPES['IDENTIFIER']], False],
            [';', False]
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)
        tag, token, _ = self.split_tokens(next_token)
        type = token

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == self.TYPES['IDENTIFIER'] or token in rules[1][0]:
            rules[1][1] = True
            kind = token
            self.outputXML.append(next_token)
        else:
            self.error(token)

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[2][0]:
            rules[2][1] = True
            next__token = self.compile_identifier(token, type, kind, False)
            self.outputXML.append(next__token)
        else:
            self.error(token)
        
        while not rules[3][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[3][0][0]:
                self.outputXML.append(next_token)
                next_token = self.inputXML.pop(0)
                tag, token, _ = self.split_tokens(next_token)
                if tag == rules[3][0][1]:
                    next__token = self.compile_identifier(token, type, kind, False)
                    self.outputXML.append(next__token)
                else:
                    self.error(token)
            elif token == rules[4][0]:
                rules[3][1] = True
                rules[4][1] = True
                self.outputXML.append(next_token)
            else:
                self.error(token)
        
        self.outputXML.append(TAG['CLOSE'])

    def compile_subroutine(self, next_token):
        TAG = {'OPEN': '<subroutineDec>', 'CLOSE': '</subroutineDec>'}
        rules = [
            [self.SubroutineDEC, True],
            [self.Types, False ],
            [self.TYPES['IDENTIFIER'], False],
            ['(', False],
            ['PARAMETER_LIST', False],
            [')', False],
            ['SUBROUTINE_BODY', False]
        ]

        self.SubroutineTableCount = {}

        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)

        if token == 'void' or token in rules[1][0] or tag == self.TYPES['IDENTIFIER']:
            rules[1][1] = True
            if tag == self.TYPES['IDENTIFIER']:
                next__token = self.use_identifier(token, True)
                self.outputXML.append(next__token)
            else:
                self.outputXML.append(next_token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[2][0]:
            rules[2][1] = True
            next__token = self.compile_identifier(token, 'subroutine', 'subroutine')
            self.outputXML.append(next__token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[3][0]:
            rules[3][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        rules[4][1] = self.compile_parameter_list()

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[5][0]:
            rules[5][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)

        rules[6][1] = self.compile_subroutine_body()

        self.outputXML.append(TAG['CLOSE'])

    def compile_parameter_list(self, terminator=')'):
        TAG = {'OPEN': '<parameterList>', 'CLOSE': '</parameterList>'}
        rules = [
            [self.Types, False],
            [self.TYPES['IDENTIFIER'], False],
            [[',', self.Types, self.TYPES['IDENTIFIER']], False],
        ]
        type = 'arg'
        self.outputXML.append(TAG['OPEN'])
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == terminator:
            rules[0][1] = rules[1][1] = rules[2][1] = True
            self.inputXML.insert(0, next_token)
            self.outputXML.append(TAG['CLOSE'])
            return True
        elif token in rules[0][0] or tag == self.TYPES['IDENTIFIER']:
            kind = token
            rules[0][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[1][0]:
            rules[1][1] = True
            next__token = self.compile_identifier(token, type, kind, False)
            self.outputXML.append(next__token)
        else:
            self.error(token)

        while not rules[2][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == terminator:
                self.inputXML.insert(0, next_token)
                rules[2][1] = True
            elif token == rules[2][0][0]:
                self.outputXML.append(next_token)
                next_token = self.inputXML.pop(0)
                tag, token, _ = self.split_tokens(next_token)
                if token in rules[2][0][1] or tag == self.TYPES['IDENTIFIER']:
                    self.outputXML.append(next_token)
                    kind = token
                    next_token = self.inputXML.pop(0)
                    tag, token, _ = self.split_tokens(next_token)
                    if tag == rules[2][0][2]:
                        next__token = self.compile_identifier(token, type, kind, False)
                        self.outputXML.append(next__token)
                    else:
                        self.error(token)
                else:
                    self.error(token)
            else:
                self.error(token)

        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)

    def compile_identifier(self, name, type, kind, used=False):
        if used:
            use = '<used/>'
        else:
            use = '<defined/>'
        
        if kind not in ['class', 'subroutine']:
            if not used:
                self.symbolTable.define(name, type, kind)
            count = self.symbolTable.index_of(name)
        else:
            count = 0

        return f'<identifier> {name} {self.SymbolTableTags[type]} {use} {count} </identifier>'

    def use_identifier(self, name, subroutine=False):
        if not subroutine:
            type = self.symbolTable.kind_of(name)
            kind = self.symbolTable.type_of(name)
        else:
            type = 'subroutine'
            kind = 'subroutine'

        return self.compile_identifier(name, type, kind, True)


    def compile_subroutine_body(self):
        TAG = {'OPEN': '<subroutineBody>', 'CLOSE': '</subroutineBody>'}
        rules = [
            ['{', False],
            ['VAR_DEC', False],
            ['STATEMENTS', False],
            ['}', False],
        ]
        self.outputXML.append(TAG['OPEN'])

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[0][0]:
            rules[0][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        while not rules[1][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == 'var':
                self.compile_var_dec(next_token)
            else:
                rules[1][1] = True
                self.inputXML.insert(0, next_token)

        rules[2][1] = self.compile_statements(rules[3][0])

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[3][0]:
            rules[3][1] = True
            self.outputXML.append(next_token)
        
        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)

    def compile_var_dec(self, next_token):
        TAG = {'OPEN': '<varDec>', 'CLOSE': '</varDec>'}
        rules = [
            ['var', False],
            [self.Types, False],
            [self.TYPES['IDENTIFIER'], False],
            [[',', self.TYPES['IDENTIFIER']], False],
            [';', False]
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token in rules[1][0] or tag == self.TYPES['IDENTIFIER']:
            rules [1][1] = True
            kind = token
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[2][0]:
            rules [2][1] = True
            next__token = self.compile_identifier(token, 'var', kind)
            self.outputXML.append(next__token)
        else:
            self.error(token)
        
        while not rules[3][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[4][0]:
                rules[3][1] = True
                rules[4][1] = True
            elif token == rules[3][0][0]:
                self.outputXML.append(next_token)
                next_token = self.inputXML.pop(0)
                tag, token, _ = self.split_tokens(next_token)
                if tag == rules[3][0][1]:
                    next__token = self.compile_identifier(token, 'var', kind)
                    self.outputXML.append(next__token)
                else:
                    self.error(token)
            else:
                self.error(token)
        
        self.outputXML.append(next_token)
        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] == True for x in rules)

    def compile_statements(self, terminator):
        TAG = {'OPEN': '<statements>', 'CLOSE': '</statements>'}
        rules = [ 
            [self.Statements, False],
            [terminator, False]
        ]
        self.outputXML.append(TAG['OPEN'])

        while not rules[0][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[1][0]:
                rules[0][1] = rules[1][1] = True
                self.inputXML.insert(0, next_token)
            elif token in rules[0][0]:
                if token == 'let':
                    self.compile_let(next_token)
                elif token == 'if':
                    self.compile_if(next_token)
                elif token == 'while':
                    self.compile_while(next_token)
                elif token == 'do':
                    self.compile_do(next_token)
                elif token == 'return':
                    self.compile_return(next_token)
            else:
                self.error(token)
        
        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] == True for x in rules) 
          
    def compile_let(self, next_token):
        TAG = {'OPEN': '<letStatement>', 'CLOSE': '</letStatement>'}
        rules = [ 
            ['let', True],
            [self.TYPES['IDENTIFIER'], False],
            [['[', 'EXPRESSION', ']'], False],
            ['=', False],
            ['EXPRESSION', False],
            [';', False]
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[1][0]:
            rules[1][1] = True;
            next__token = self.use_identifier(token)
            self.outputXML.append(next__token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[2][0][0]:
            self.outputXML.append(next_token)
            self.compile_expression()
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[2][0][2]:
                rules[2][1] = True
                self.outputXML.append(next_token)
            else:
                self.error(token)
        elif token == rules[3][0]:
            rules[2][1] = rules[3][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        if not rules[3][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[3][0]:
                rules[2][1] = rules[3][1] = True
                self.outputXML.append(next_token)
            else:
                self.error(token)
        
        rules[4][1] = self.compile_expression()

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[5][0]:
            rules[5][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        self.outputXML.append(TAG['CLOSE'])

    def compile_if(self, next_token):
        TAG = {'OPEN': '<ifStatement>', 'CLOSE': '</ifStatement>'}
        rules = [ 
            ['if', True],
            ['(', False],
            ['EXPRESSION', False],
            [')', False],
            ['{', False],
            ['STATEMENTS', False],
            ['}', False],
            ['else', False],
            ['{', False],
            ['STATEMENTS', False],
            ['}', False],
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[1][0]:
            rules[1][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(next_token)
        
        rules[2][1] = self.compile_expression()

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[3][0]:
            rules[3][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(next_token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[4][0]:
            rules[4][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(next_token)
        
        rules[5][1] = self.compile_statements(rules[6][0])

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[6][0]:
            rules[6][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(next_token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[7][0]:
            rules[7][1] = True
            self.outputXML.append(next_token)
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[8][0]:
                rules[8][1] = True
                self.outputXML.append(next_token)
                rules[9][1] = self.compile_statements(rules[10][0])
                next_token = self.inputXML.pop(0)
                tag, token, _ = self.split_tokens(next_token)
                if token == rules[10][0]:
                    rules[10][1] = True
                    self.outputXML.append(next_token)
                else:
                    self.error(token)
            else:
                self.error(token)
        else:
            rules[7][1] = rules[8][1] = rules[9][1] = rules[10][1] = True
            self.inputXML.insert(0, next_token)

        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)
    
    def compile_while(self, next_token):
        TAG = {'OPEN': '<whileStatement>', 'CLOSE': '</whileStatement>'}
        rules = [ 
            ['while', True],
            ['(', False],
            ['EXPRESSION', False],
            [')', False],
            ['{', False],
            ['STATEMENTS', False],
            ['}', False]
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[1][0]:
            rules[1][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        rules[2][1] = self.compile_expression()

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[3][0]:
            rules[3][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[4][0]:
            rules[4][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        rules[5][1] = self.compile_statements(rules[6][0])

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[6][0]:
            rules[6][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)

    def compile_do(self, next_token):
        TAG = {'OPEN': '<doStatement>', 'CLOSE': '</doStatement>'}
        rules = [ 
            ['do', True],
            ['SUBROUTINE_CALL', False],
            [';', False]
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)
        rules[1][1] = self.compile_subroutine_call()

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[2][0]:
            rules[2][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)

        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)

    def compile_return(self, next_token):
        TAG = {'OPEN': '<returnStatement>', 'CLOSE': '</returnStatement>'}
        rules = [ 
            ['return', True],
            ['EXPRESSION', False],
            [';', False]
        ]
        self.outputXML.append(TAG['OPEN'])
        self.outputXML.append(next_token)
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[2][0]:
            rules[1][1] = rules[2][1] = True
            self.outputXML.append(next_token)
        else:
            self.inputXML.insert(0, next_token)
            rules[1][1] = self.compile_expression()
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[2][0]:
                rules[2][1] = True
                self.outputXML.append(next_token)
            else:
                self.error(token)

        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)
        
    def compile_subroutine_call(self):
        rules = [ 
            [[self.TYPES['IDENTIFIER'], '.', self.TYPES['IDENTIFIER']], False],
            ['(', False],
            ['EXPRESSION_LIST', False],
            [')', False]
        ]
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if tag == rules[0][0][0]:
            next__token = self.use_identifier(token, True)
            self.outputXML.append(next__token)
        else:
            self.error(token)
        
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[0][0][1]:
            self.outputXML.append(next_token)
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if tag == rules[0][0][2]:
                rules[0][1] = True
                next__token = self.use_identifier(token, True)
                self.outputXML.append(next__token)
            else:
                self.error(token)
        elif token == rules[1][0]:
            rules[0][1] = rules[1][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        if not rules[1][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[1][0]:
                self.outputXML.append(next_token)
            else:
                self.error(token)
        
        self.compile_expression_list(rules[3][0])

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        if token == rules[3][0]:
            rules[3][1] = True
            self.outputXML.append(next_token)
        else:
            self.error(token)
        
        return all(x[1] for x in rules)

    def compile_expression_list(self, terminator):
        TAG = {'OPEN': '<expressionList>', 'CLOSE': '</expressionList>'}
        rules = [
            ['EXPRESSION', False],
            [[',', 'EXPRESSION'], False]
        ]
        self.outputXML.append(TAG['OPEN'])

        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)
        self.inputXML.insert(0, next_token)

        if token == terminator:
            rules[0][1] = rules[1][1] = True
        else:
            rules[0][1] = self.compile_expression()

        while not rules[1][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == rules[1][0][0]:
                self.outputXML.append(next_token)
                self.compile_expression()
            elif token == terminator:
                rules[1][1] = True
                self.inputXML.insert(0, next_token)
            else:
                self.error(token)
        
        self.outputXML.append(TAG['CLOSE'])


    def compile_expression(self):
        TAG = {'OPEN': '<expression>', 'CLOSE': '</expression>'}
        rules = [ 
            ['TERM', False],
            [[self.OPS, 'TERM'], False]
        ]
        self.outputXML.append(TAG['OPEN'])
        rules[0][1] = self.compile_term()
        while not rules[1][1]:
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token in rules[1][0][0]:
                self.outputXML.append(next_token)
                self.compile_term()
                next_token = self.inputXML.pop(0)
                tag, token, _ = self.split_tokens(next_token)
                self.inputXML.insert(0, next_token)
                if token not in rules[1][0][0]:
                    rules[1][1] = True
            else:
                rules[1][1] = True
                self.inputXML.insert(0, next_token)

        self.outputXML.append(TAG['CLOSE'])
        return all(x[1] for x in rules)

    def compile_term(self):
        TAG = {'OPEN': '<term>', 'CLOSE': '</term>'}
        self.outputXML.append(TAG['OPEN'])
        next_token = self.inputXML.pop(0)
        tag, token, _ = self.split_tokens(next_token)

        if tag in self.TermTags:
            self.outputXML.append(next_token)
            self.outputXML.append(TAG['CLOSE'])
            return True
        elif token in self.KeyWordConstants:
            self.outputXML.append(next_token)
            self.outputXML.append(TAG['CLOSE'])
            return True
        elif token in self.UnaryOPS:
            self.outputXML.append(next_token)
            self.compile_term()
            self.outputXML.append(TAG['CLOSE'])
            return True
        elif token == '(':
            self.outputXML.append(next_token)
            self.compile_expression()
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == ')':
                self.outputXML.append(next_token)
                self.outputXML.append(TAG['CLOSE'])
                return True
            else:
                self.error(token)
        elif tag == self.TYPES['IDENTIFIER']:
            first_token = next_token
            next_token = self.inputXML.pop(0)
            tag, token, _ = self.split_tokens(next_token)
            if token == '[':
                tag, token, _ = self.split_tokens(first_token)
                next__token = self.use_identifier(token)
                self.outputXML.append(next__token)
                self.compile_expression()
                next_token = self.inputXML.pop(0)
                tag, token, _ = self.split_tokens(next_token)
                if token == ']':
                    self.outputXML.append(next_token)
                    self.outputXML.append(TAG['CLOSE'])
                    return True
                else:
                    self.error(token)
            elif token == '.':
                self.inputXML.insert(0, next_token)
                self.inputXML.insert(0, first_token)
                self.compile_subroutine_call()
                self.outputXML.append(TAG['CLOSE'])
                return True
            else:
                self.inputXML.insert(0, next_token)
                tag, token, _ = self.split_tokens(first_token)
                next__token = self.use_identifier(token)
                self.outputXML.append(next__token)
                self.outputXML.append(TAG['CLOSE'])
                return True
        else:
            self.error(token)

    def split_tokens(self, token):
        if 'stringConstant' in token:
            arr = token.split()
            tag = arr[0]
            _ = arr[-1]
            token = ' '.join(arr[1:-2])
            arr = [tag]+[token]+[_]
            return arr
        else:
            return token.split()
        

    def error(self, token):
        print(f'Invalid token ({token}) encountered.')

        
    





        

