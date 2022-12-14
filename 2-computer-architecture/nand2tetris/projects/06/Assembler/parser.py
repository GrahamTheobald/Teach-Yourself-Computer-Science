from code import Code
from symbol_table import Symbol_table

COMMAND_TYPES = {
    'L': 'L_COMMAND',
    'A': 'A_COMMAND',
    'C': 'C_COMMAND'
}

class Parser:
    def __init__(self, assembly):
        self.assembly = assembly
        self.lines = []
        self.binary = []
        self.current_command = None
    
    def parse(self):
        code = Code()
        symbol_table = Symbol_table()
        with open(self.assembly) as file:
            for line in file:
                cleaned = self.clean_line(line)
                if len(cleaned) == 0:
                    continue
                type = self.command_type(cleaned)
                if type == COMMAND_TYPES['L']:
                    symbol = self.label_name(cleaned)
                    symbol_table.add_entry(symbol, len(self.lines))
                    continue
                self.lines.append([type, cleaned])
        
        for type, cleaned in self.lines:
            if type == COMMAND_TYPES['A']:
                address = cleaned[1:]
                if address.isdigit():
                    number = int(address)
                else:
                    if not symbol_table.contains(address):
                        symbol_table.add_entry(address)
                    number = int(symbol_table.get_address(address))
                binary = code.a_command(number)
                self.binary.append(binary)
            elif type == COMMAND_TYPES['C']:
                dest = self.dest(cleaned)
                jump = self.jump(cleaned)
                comp = self.comp(cleaned)
                binary = code.c_command(dest, comp, jump)
                self.binary.append(binary)
        
    def label_name(self, line):
        return line[1:-1]

    def write(self):
        hack_file = self.file_name()
        with open(hack_file, 'w') as file:
            file.write('\n'.join(self.binary))               
    
    def file_name(self): 
        index = self.assembly.find('.asm')
        print(index, self.assembly)
        hack = self.assembly[:index]
        hack += '.hack'
        return hack
        
    def comp(self, line):
        start = 0
        end = len(line)
        if '=' in line:
            start = line.find('=') + 1
        if ';' in line:
            end = line.find(';')
        return line[start:end]

    def dest(self, line):
        if '=' not in line:
            return 'null'
        index = line.find('=')
        return line[:index]             

    def jump(self, line):
        if 'JMP' in line:
            return 'JMP'       
        if ';' not in line:
            return 'null'
        index = line.find(';')
        return line[index + 1:]
    
    def clean_line(self, line):
        line = ''.join(line.split())
        if '//' in line:
            index = line.find('//')
            line = line[:index]
        return line
    
    def command_type(self, line): 
        if line[0] == '(':
            return COMMAND_TYPES['L']
        if line[0] == '@':
            return COMMAND_TYPES['A']
        return COMMAND_TYPES['C']
