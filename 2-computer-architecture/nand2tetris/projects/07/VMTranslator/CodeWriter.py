COMMANDS = {
    'ARITHMETIC': 'arithmetic',
    'PUSH': 'push',
    'POP': 'pop'
}

C_ARITHMETIC = ['add', 'sub', 'eq', 'lt', 'gt', 'and', 'not', 'or', 'neg']

class CodeWriter:
    def __init__(self, vm, file_name):
        self.file_name = file_name
        self.vm = vm
        self.asm= []
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
        self.write_file()

    def write_file(self):
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
            self.asm += [f'@{self.static_name}.{value}', 'D=M']
            
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
            self.asm += ['D=A', f'@{self.static_name}.{value}', 'M=D']

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
