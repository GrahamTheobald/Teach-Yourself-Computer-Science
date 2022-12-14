class Symbol_table: 
    table = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,  
        'SCREEN': 16384,
        'KBD': 24576,
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
    }  
    addresses = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16384,24576] 

    def add_entry(self, symbol, address=False):
        if not address:
            address = self.unused_address()
            self.addresses.append(address)
            
        self.table[symbol] = address

    def unused_address(self):
        for i in range(16, 100000):
            if i not in self.addresses:
                return i

    def contains(self, symbol):
        return symbol in self.table.keys()
    
    def get_address(self, symbol):
        return self.table[symbol]
