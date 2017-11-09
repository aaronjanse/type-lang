from error import *
from lang_types import is_type

class Environment(object):
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.dictionary = {}
        self.type_dict = {}

    def define(self, type_name, token_key, value):
        if not is_type(value, type_name):
            ErrorHandler.report(ProgramRuntimeError(
                f"Variable {token_key.lexeme} of type {type_name} cannot be assigned as {value}"), token_key.line)

        self.dictionary[token_key.lexeme] = value
        self.type_dict[token_key.lexeme] = type_name

    def assign(self, token_key, value):
        key = token_key.lexeme

        type_name = self.type_dict[key]
        if not is_type(value, type_name):
            ErrorHandler.report(ProgramRuntimeError(
                f"Variable {key} of type {type_name} cannot be assigned as {value}"), key.line)

        if key in self.dictionary:
            self.dictionary[key] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(token_key, value)
            return

        ErrorHandler.report(ProgramRuntimeError(
            "Undefined variable '{}'".format(key)), token_key.line)

    def get(self, token_key):
        key = token_key.lexeme

        if key in self.dictionary:
            return self.dictionary[key]

        if self.enclosing is not None:
            return self.enclosing.get(token_key)

        ErrorHandler.report(ProgramRuntimeError(
            "Undefined variable '{}'".format(key)), token_key.line)
