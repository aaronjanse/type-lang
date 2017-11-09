from enum import Enum


class TokenType():
    (LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE,
     COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR,

     BANG, BANG_EQUAL,
     EQUAL, EQUAL_EQUAL,
     GREATER, GREATER_EQUAL,
     LESS, LESS_EQUAL,

     IDENTIFIER, STRING, NUMBER,

     AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR,
     PRINT, RETURN, SUPER, THIS, TRUE, WHILE,

     VAR, VAR_INT, VAR_STR,

     EOF) = range(41)


TokenType.VAR = 'var'
TokenType.VAR_INT = 'int'
TokenType.VAR_STR = 'str'

