from expr import *
from error import *
from token_type import TokenType
from stmt import Stmt
from environment import Environment


class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except:
            print('error')
            raise

    def execute(self, stmt):
        stmt.accept(self)

    # ExprAssign
    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)

        self.environment.assign(expr.name, value)
        return value

    # StmtVar
    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.type_name, stmt.name, value)
        return None

    # ExprVariable
    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    # StmtExpression
    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    # StmtPrint
    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)

        print(str(value))

        return None

    # ExprLiteral
    def visitLiteralExpr(self, expr):
        return expr.value

    # ExprGrouping
    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    # ExprBinary
    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.PLUS:
            return left + right
        elif expr.operator.token_type == TokenType.MINUS:
            return left - right
        elif expr.operator.token_type == TokenType.SLASH:
            return left / right
        elif expr.operator.token_type == TokenType.STAR:
            return left * right
        elif expr.operator.token_type == TokenType.GREATER:
            return left > right
        elif expr.operator.token_type == TokenType.GREATER_EQUAL:
            return left >= right
        elif expr.operator.token_type == TokenType.LESS:
            return left < right
        elif expr.operator.token_type == TokenType.LESS_EQUAL:
            return left <= right
        elif expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

        # Unreachable.
        return None

    # ExprUnary
    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            return -right
        elif expr.operator.token_type == TokenType.BANG:
            return not self.isTruthy(right)

        # Unreachable
        return None

    def isEqual(self, a, b):
        return a == b

    def isTruthy(self, expr):
        return bool(expr)

    def evaluate(self, expr):
        return expr.accept(self)
