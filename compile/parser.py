from token_type import TokenType
from expr import *
from error import *
from stmt import *


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            statements = []

            while not self.isAtEnd():
                statements.append(self.declaration())

            return statements
        except ParserError as e:
            ErrorHandler.report(e)

    def declaration(self):
        try:
            for type_token in TokenType.VAR, TokenType.VAR_INT, TokenType.VAR_STR:
                if self.match(type_token):
                    return self.varDeclaration(type_token)

            return self.statement()
        except ParserError as e:
            print('Caught: ' + str(e))
            self.synchronize()
            return None

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        elif self.match(TokenType.LEFT_BRACE):
            return StmtBlock(self.block())

        return self.expressionStatement()

    def varDeclaration(self, type_token):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        # self.consume(TokenType.SEMICOLON,
        #              "Expect ';' after variable declaration.")
        return StmtVar(type_token, name, initializer)

    def printStatement(self):
        value = self.expression()
        # self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return StmtPrint(value)

    def expressionStatement(self):
        expr = self.expression()
        # self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")

        return StmtExpression(expr)

    def block(self):
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, ExprVariable):
                name = expr.name
                return ExprAssign(name, value)

            ErrorHandler.report(
                "Invalid assignment target at char {}".format(equals), equals.line)

        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = ExprBinary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = ExprBinary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = ExprBinary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = ExprBinary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return ExprUnary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return ExprLiteral(False)
        if self.match(TokenType.TRUE):
            return ExprLiteral(True)
        if self.match(TokenType.NIL):
            return ExprLiteral(None)

        if self.match(TokenType.IDENTIFIER):
            return ExprVariable(self.previous())

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return ExprLiteral(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return ExprGrouping(expr)

        ErrorHandler.report(ParserError("Expected expression. Instead got {}".format(
            str(self.peek().literal))), self.peek().line)

    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()

        ErrorHandler.report(ParserError(
            message + ' at token ' + str(self.peek().literal)), self.peek().line)

    def match(self, *types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def check(self, token_type):
        if self.isAtEnd():
            return False

        return self.peek().token_type == token_type

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            if self.peek().token_type in (TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
                return

            self.advance()

    def advance(self):
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    def isAtEnd(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
