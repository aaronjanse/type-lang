import sys


class ErrorHandler(object):
    errored = False

    @classmethod
    def report(cls, exception, line=None):
        if line is not None:
            print('[line {}]', end=' ')

        print('{}: {}'.format(line, type(exception).__name__, str(exception)))
        cls.errored = True

        if isinstance(exception, ProgramRuntimeError):
            raise exception


class ScannerError(Exception):
    pass


class ParserError(Exception):
    pass


class InterpreterError(Exception):
    pass


class ProgramRuntimeError(Exception):
    pass
