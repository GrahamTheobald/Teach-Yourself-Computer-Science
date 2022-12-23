class Parser: 
    def __init__(self, vm):
        self.vm = vm
        self.lines = []

    def parse(self):
        with open(self.vm, 'r') as file:
            for line in file:
                cleaned = self.clean(line)
                if len(cleaned) == 0:
                    continue
                self.lines.append(cleaned.split(' '))
    
    def clean(self, line):
        index = line.find('//')
        if index > -1:
            line = line[:index]
        return line.strip()
        
