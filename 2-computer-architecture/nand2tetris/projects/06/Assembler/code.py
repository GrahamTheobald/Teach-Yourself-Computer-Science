from mnemonics import COMP, JUMP, DEST

class Code:
    def a_command(self, number):
        binary = bin(number)
        return self.format_binary(binary)

    def c_command(self, dest, comp, jump):
        binary = '111'
        if 'M' in comp:
            binary += '1'
        else:
            binary += '0'
        binary += COMP[comp]
        binary += DEST[dest]
        binary += JUMP[jump]
        return binary

    def format_binary(self, binary):
        string = binary[2:]
        while len(string) != 16:
            string = '0' + string
        return string
    