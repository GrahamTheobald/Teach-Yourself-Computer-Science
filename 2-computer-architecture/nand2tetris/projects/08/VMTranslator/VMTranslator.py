import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    vm = sys.argv[1]
    if is_vm(vm):
        file_procedure  
    else:
        directory_procedure(vm)

def is_vm(vm):
    return vm[-3:] == '.vm'

def file_procedure(vm):
    parser = Parser(vm)
    parser.parse()
    code_writer = CodeWriter(parser.lines, vm)
    code_writer.translate()
    code_writer.write_file()

def directory_procedure(vm):
    files = os.listdir(vm)
    last_asm = initiate()
    for file in files:
        if is_vm(file):
            parser = Parser(f'{vm}/{file}')
            parser.parse()
            code_writer = CodeWriter(parser.lines, vm, last_asm)
            code_writer.translate()
            last_asm = code_writer.asm
    code_writer.write_file(True)

def initiate():
    bootstrap = ['@256', 'D=A', '@SP', 'M=D']
    code_writer = CodeWriter([['call', 'Sys.init', '0']], '_', bootstrap)
    code_writer.translate()
    return code_writer.asm

# def final_directory(vm):
#     reverse = vm[::-1]
#     index = reverse.find('/')
#     directory = reverse[:index][::-1]
#     return f'{vm}/{directory}'

main()