from token_type import TokenType
from token import Token
from error import *
import string
import re


class Scanner(object):
    non_conditional_char_tokentypes = {
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '-': TokenType.MINUS,
        '+': TokenType.PLUS,
        ';': TokenType.SEMICOLON,
        '*': TokenType.STAR,
        '/': TokenType.SLASH
    }

    conditional_char_tokentypes = {
        '!': lambda self: TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG,
        '=': lambda self: TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL,
        '>': lambda self: TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER,
        '<': lambda self: TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS
    }

    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "int": TokenType.VAR_INT,
        "str": TokenType.VAR_STR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source

        self.tokens = []

        self.line = 1
        self.start = 0
        self.current = 0

        self.stripComments()

    def stripComments(self):
        self.source = re.sub(r'\/\/[^"\']*\n', '', self.source)
        self.source = re.sub(r';\s*\n', '', self.source)  # XXX: remove trailing semicolons

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current

            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))

        return self.tokens

    def scanToken(self):
        char = self.advance()

        if char in (' ', '\r', '\t'):
            pass
        elif char == '\n':
            self.line += 1
        elif char in self.non_conditional_char_tokentypes:
            self.addToken(self.non_conditional_char_tokentypes[char])
        elif char in self.conditional_char_tokentypes:
            self.addToken(self.conditional_char_tokentypes[char](self))
        elif char == '"':
            self.processString()
        elif char in string.digits:
            self.processDigit()
        elif char.isalpha() or char == '_':
            self.processIdentifier()
        else:
            ErrorHandler.report(ScannerError(
                "Unexpected character."), self.line)

    def processIdentifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start: self.current]

        token_type = TokenType.IDENTIFIER

        if text in self.keywords:
            token_type = self.keywords[text]

        self.addToken(token_type)

    def processString(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1

            self.advance()

        # Unterminated string.
        if self.isAtEnd():
            ErrorHandler.report(ScannerError(
                "Unterminated string."), self.line)
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1: self.current - 1]
        self.addToken(TokenType.STRING, value)

    def processDigit(self):
        while self.peek().isnumeric():
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.peekNext().isnumeric():
            # Consume the "."
            self.advance()

            while self.peek().isnumeric():
                self.advance()

        self.addToken(TokenType.NUMBER, int(
            self.source[self.start: self.current]))

    def addToken(self, token_type, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, char):
        if self.isAtEnd():
            return False
        elif self.source[self.current] != char:
            return False
        else:
            self.current += 1
            return True

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.current + 1]

    def peek(self):
        if self.isAtEnd():
            return '\0'
        else:
            return self.source[self.current]

    def isAtEnd(self):
        return self.current >= len(self.source)
