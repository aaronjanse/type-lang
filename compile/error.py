import sys


class ErrorHandler(object):
    errored = False

    @classmethod
    def report(cls, exception, line=None):
        error_text = ''
        if line is not None:
            error_text += '[line {}]'.format(line)

        error_text = '{}: {}'.format(type(exception).__name__, str(exception))
        print(error_text)

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
