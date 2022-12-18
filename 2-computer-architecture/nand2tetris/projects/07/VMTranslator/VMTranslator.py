import sys
from Parser import Parser
from CodeWriter import CodeWriter

vm = sys.argv[1]

parser = Parser(vm)
parser.parse()

code_writer = CodeWriter(parser.lines, vm)
code_writer.translate()
