COMMANDS = {
    'ARITHMETIC': 'arithmetic',
    'PUSH': 'push',
    'POP': 'pop',
    'GOTO': 'goto',
    'IF-GOTO': 'if-goto',
    'LABEL': 'label',
    'FUNCTION': 'function',
    'RETURN': 'return',
    'CALL': 'call'
}

C_ARITHMETIC = ['add', 'sub', 'eq', 'lt', 'gt', 'and', 'not', 'or', 'neg']

class CodeWriter:
    def __init__(self, vm, file_name, asm=[]):
        self.file_name = file_name
        self.vm = vm
        self.asm = asm
        self.i = 0
        self.comparators = {
            'eq': 'D;JEQ',
            'lt': 'D;JLT',
            'gt': 'D;JGT'
        }
        self.segments = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
        }
        self.push_default = ['push', 'default', 0]
        self.pop_default = ['pop', 'default', 0]
        self.generate_static()
        self.function_calls = {'null': 1}
        self.active_function = 'null'
    
    def generate_static(self):
        s_name = self.file_name
        index = s_name.find('/')
        while index != -1:
            s_name = s_name[index+1:]
            index = s_name.find('/')
        index = s_name.find('.vm')
        self.static_name = s_name[:index]
    
    def translate(self):
        for line in self.vm:
            command = self.command_type(line)
            if command == COMMANDS['ARITHMETIC']:
                self.write_arithmetic(line)
            elif command == COMMANDS['PUSH']:
                self.write_push(line)
            elif command == COMMANDS['POP']:
                self.write_pop(line)
            elif command == COMMANDS['LABEL']:
                self.write_label(line[1])
            elif command == COMMANDS['GOTO']:
                self.write_goto(line)
            elif command == COMMANDS['IF-GOTO']:
                self.write_if_goto(line)
            elif command == COMMANDS['FUNCTION']:
                self.write_function(line)
            elif command == COMMANDS['RETURN']:
                self.write_return()
            elif command == COMMANDS['CALL']:

                self.write_call(line)

    def write_file(self, directory=False):
        if directory:
            new_file_name = f'{self.final_directory(self.file_name)}.asm'
        else:
            new_file_name = self.file_name.replace('.vm', '.asm')
        with open(new_file_name, 'w') as file:
            file.write('\n'.join(self.asm))

    
    def command_type(self, line):
        command = line[0]
        if command in C_ARITHMETIC:
            return COMMANDS['ARITHMETIC']
        elif command == 'push':
            return COMMANDS['PUSH']
        elif command == 'pop':
            return COMMANDS['POP']
        elif command == 'goto':
            return COMMANDS['GOTO']
        elif command == 'if-goto':
            return COMMANDS['IF-GOTO']
        elif command == 'label':
            return COMMANDS['LABEL']
        elif command == 'function':
            return COMMANDS['FUNCTION']
        elif command == 'return':
            return COMMANDS['RETURN']
        elif command == 'call':
            return COMMANDS['CALL']

    def write_call(self, line):
        _, fname, args = line
        if fname in self.function_calls:
            self.function_calls[fname] += 1
        else:
            self.function_calls[fname] = 1
        return_label = f'ret.{self.generate_flabel(fname)}'

        self.asm += [f'@{return_label}', 'D=A']
        self.write_push(['push', '_', '_'])
        self.asm += ['@LCL', 'D=M']
        self.write_push(['push', '_', '_'])
        self.asm += ['@ARG', 'D=M']
        self.write_push(['push', '_', '_'])
        self.asm += ['@THIS', 'D=M']
        self.write_push(['push', '_', '_'])
        self.asm += ['@THAT', 'D=M']
        self.write_push(['push', '_', '_'])

        self.asm += ['@SP', 'D=M', '@5', 'D=D-A', f'@{args}', 'D=D-A', '@ARG', 'M=D']
        
        self.asm += ['@SP', 'D=M', '@LCL', 'M=D']
        self.asm += [f'@{fname}', '0;JMP']

        self.asm.append(f'({return_label})')

    def write_return(self):
        self.asm += ['@LCL', 'D=M', '@endFrame', 'M=D']
        self.asm += ['@endFrame', 'D=M', '@5', 'A=D-A', 'D=M', '@retAddr', 'M=D']
        self.write_pop(['pop', 'argument', '0'])
        self.asm += ['@ARG', 'D=M', '@1', 'D=D+A', '@SP', 'M=D']
        self.asm += ['@endFrame', 'D=M', '@1', 'A=D-A', 'D=M', '@THAT', 'M=D']
        self.asm += ['@endFrame', 'D=M', '@2', 'A=D-A', 'D=M', '@THIS', 'M=D']
        self.asm += ['@endFrame', 'D=M', '@3', 'A=D-A', 'D=M', '@ARG', 'M=D']
        self.asm += ['@endFrame', 'D=M', '@4', 'A=D-A', 'D=M', '@LCL', 'M=D']
        self.asm += ['@retAddr', 'A=M', '0;JMP']

    def write_function(self, line):
        _, fname, lcls = line
        self.active_function = fname
        if fname in self.function_calls:
            self.function_calls[fname] += 1
        else:
            self.function_calls[fname] = 1
        self.write_label(fname, True)
        for _ in range(int(lcls)):
            self.write_push(['push', 'constant', '0'])

    def write_if_goto(self, line):
        self.write_pop(self.pop_default)
        self.asm += ['D=A', f'@{self.generate_label(line[1])}', 'D;JNE']
        
    def write_goto(self, line):
        self.asm += [f'@{self.generate_label(line[1])}', '0;JMP']

    def generate_label(self, name):
        count = self.function_calls[self.active_function]
        return f'{self.active_function}${name}.{count}' 
        
    def write_label(self, label, function=False):
        count = self.function_calls[self.active_function]
        if not function:
            label = f'{self.active_function}${label}.{count}'
        self.asm.append(f'({label})')
    
    def generate_flabel(self, function):
        count = self.function_calls[function]
        return f'{function}.{count}'

    def write_arithmetic(self, line):
        command = line[0]
        if command == 'add':
            self.write_pop(self.pop_default)
            self.asm.append('D=A')
            self.write_pop(self.pop_default)
            self.asm.append('D=D+A')
            self.write_push(self.push_default)
        elif command == 'sub':
            self.write_sub()
        elif command == 'neg':
            self.write_pop(self.pop_default)
            self.asm.append('D=-A')
            self.write_push(self.push_default)
        elif command in ['eq', 'lt', 'gt']:
            self.write_sub(False)
            self.write_jump(command)
        elif command == 'or':
            self.write_pop(self.pop_default)
            self.asm.append('D=A')
            self.write_pop(self.pop_default)
            self.asm.append('D=D|A')
            self.write_push(self.push_default)
        elif command == 'and':
            self.write_pop(self.pop_default)
            self.asm.append('D=A')
            self.write_pop(self.pop_default)
            self.asm.append('D=D&A')
            self.write_push(self.push_default)
        elif command == 'not':
            self.write_pop(self.pop_default)
            self.asm.append('D=!A')
            self.write_push(self.push_default)

    def write_push(self, line): 
        _, location, value = line
        if location == 'constant': 
            self.asm += [f'@{value}', 'D=A']
        elif location in self.segments.keys():
            self.asm += [f'@{self.segments[location]}', 'D=M', f'@{value}', 'A=D+A', 'D=M']
        elif location == 'temp': 
            self.asm += ['@5', 'D=A', f'@{value}', 'A=D+A', 'D=M']
        elif location == 'pointer':
            segment = 'THIS'
            if value == '1':
                segment = 'THAT'
            self.asm += [f'@{segment}', 'D=M']
        elif location == 'static':
            index = self.active_function.find('.')
            if index != -1: 
                clss = self.active_function[:index]
            else:
                clss = self.active_function
            self.asm += [f'@{clss}${self.static_name}.{value}', 'D=M']
            
        self.asm += ['@SP', 'A=M', 'M=D', '@SP', 'M=M+1']

    def write_pop(self, line):
        _, location, value = line
        self.asm += ['@SP', 'M=M-1', 'A=M', 'A=M']
        if location in self.segments.keys():
            self.asm += ['D=A', '@val', 'M=D', f'@{self.segments[location]}', 'D=M', f'@{value}', 'D=D+A', '@addr', 'M=D', '@val', 'D=M', '@addr', 'A=M', 'M=D']
        elif location == 'temp':
            self.asm += ['D=A', '@val', 'M=D', f'@5', 'D=A', f'@{value}', 'D=D+A', '@addr', 'M=D', '@val', 'D=M', '@addr', 'A=M', 'M=D']
        elif location == 'pointer':
            segment = 'THIS'
            if value == '1':
                segment = 'THAT'
            self.asm += ['D=A', f'@{segment}', 'M=D']
        elif location == 'static':
            index = self.active_function.find('.')
            if index != -1: 
                clss = self.active_function[:index]
            else:
                clss = self.active_function
            self.asm += ['D=A', f'@{clss}${self.static_name}.{value}', 'M=D']

    def write_sub(self, push=True):
        self.write_pop(self.pop_default)
        self.asm.append('D=A')
        self.write_pop(self.pop_default)
        self.asm.append('D=A-D')
        if push:
            self.write_push(self.push_default)

    def write_jump(self, comparator):
        self.asm += [f'@TRUE{self.i}',
            self.comparators[comparator],
            '@0',
            'D=A',
            f'@PUSH{self.i}',
            '0;JMP',
             f'(TRUE{self.i})',
            '@0',
            'D=A',
            'D=D-1',
            f'@PUSH{self.i}',
            '0;JMP',
            f'(PUSH{self.i})',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            ]
        self.i += 1
    
    def final_directory(self, vm):
        reverse = vm[::-1]
        index = reverse.find('/')
        if index != -1:
            directory = reverse[:index][::-1]
        else:
            directory = reverse[::-1]
        return f'{vm}/{directory}'
