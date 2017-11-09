import sys
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter
from error import *


class Main(object):
    def __init__(self):
        self.interpreter = Interpreter()

    def run(self, source_code, ignore_errors=False):
        tokens = Scanner(source_code).scanTokens()

        parser = Parser(tokens)
        statements = parser.parse()

        if ErrorHandler.errored:
            if ignore_errors:
                ErrorHandler.errored = False
            return

        self.interpreter.interpret(statements)

        # print(AstPrinter().printExpr(expression));


main = Main()

if len(sys.argv) > 1:
    lox_filename = sys.argv[1]

    with open(lox_filename, 'r') as f:
        lox_source_code = f.read() + '\n'

    main.run(lox_source_code)
else:
    while True:
        line = input('> ')
        main.run(line, ignore_errors=True)
