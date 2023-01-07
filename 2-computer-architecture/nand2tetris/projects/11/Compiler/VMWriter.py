class VMWriter:
    def __init__(self):
        self.vm = []

    SEGMENT = {
        'constant': 'constant',
        'local': 'local',
        'argument': 'argument'
    }
    COMMAND = {
        '+': 'add',
        '-': 'sub',
        'neg': 'neg',
        '=': 'eq',
        '&gt;': 'gt',
        '&lt;': 'lt',
        '&amp;': 'and',
        '|': 'or',
        '~': 'not',
        '*': 'call Math.multiply 2',
        '/': 'call Math.divide 2'
    }

    def write_file(self, file_name):
        with open(f'{file_name}.vm', 'w') as file:
            file.write('\n'.join(self.vm))

    def write_function(self, name, locals):
        self.vm.append(f'function {name} {locals}')

    def write_push(self, segment, index=False):
        vm = f'push {self.SEGMENT[segment]} {index}'
        self.vm.append(vm)
    
    def write_pop(self, segment, index):
        vm = f'pop {self.SEGMENT[segment]} {index}'
        self.vm.append(vm)
    
    def write_arithmetic(self, command):
        self.vm.append(self.COMMAND[command])

    def write_label(self, label):
        self.vm.append(f'label {label}')

    def write_goto(self, label):
        self.vm.append(f'goto {label}')
    
    def write_if_goto(self, label):
        self.vm.append(f'if-goto {label}')
    
    def write_call(self, name, nArgs):
        self.vm.append(f'call {name} {nArgs}')

    def write_return(self, void):
        self.vm.append('return')
        if void:
            self.vm.append('pop temp 0')