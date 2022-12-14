import sys
from parser import Parser , COMMAND_TYPES

assembly = sys.argv[1]
parser = Parser(assembly)
parser.parse()
parser.write()


