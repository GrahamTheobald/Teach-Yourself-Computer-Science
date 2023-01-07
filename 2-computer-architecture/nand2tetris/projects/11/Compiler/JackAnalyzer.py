from Tokeniser import Tokeniser
from CompilationEngine import CompilationEngine
import sys
import os

def main():
    arg = sys.argv[1]
    if not is_jackfile(arg):
        for file in os.listdir(arg):
            if is_jackfile(file):
                file_name = f'{arg}/{file}'
                tokeniser = Tokeniser(file_name)
                tokeniser.tokenise()
                txml = tokeniser.xml[1:-1]
                compilation_engine = CompilationEngine(txml)
                compilation_engine.compile()
                file_name = file_name[:-5]
                compilation_engine.write_file(file_name)

def is_jackfile(str):
    return str[-5:] == '.jack'

main()
