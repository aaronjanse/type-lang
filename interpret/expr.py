class Expr(object):
    class Visitor(object):
        # Expr.Assign expr
        def visitAssignExpr(expr):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitAssignExpr()'.format(self.__class__.__name__))

        # Expr.Binary expr
        def visitBinaryExpr(self, expr):
            return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

        # Expr.Grouping expr
        def visitGroupingExpr(self, expr):
            return self._parenthesize("group", expr.expression)

        # Expr.Literal expr
        def visitLiteralExpr(self, expr):
            if expr.value is None:
                return "nil"

            return str(expr.value)

        # Expr.Logical expr
        def visitLogicalExpr(expr):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitLogicalExpr()'.format(self.__class__.__name__))

        # Expr.Unary expr
        def visitUnaryExpr(self, expr):
            return self._parenthesize(expr.operator.lexeme, expr.right)

        # Expr.Variable expr
        def visitVariableExpr(expr):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitVariableExpr()'.format(self.__class__.__name__))

        def _parenthesize(self, name, *exprs):
            text = '(' + name

            for expr in exprs:
                text += ' '
                text += expr.accept(self)

            text += ')'

            return text


class ExprAssign(Expr):
    def __init__(self, name, value):
        # Token
        self.name = name

        # Expr
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssignExpr(self)


class ExprBinary(Expr):
    def __init__(self, left, operator, right):
        # Expr
        self.left = left

        # Token
        self.operator = operator

        # Expr
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class ExprGrouping(Expr):
    def __init__(self, expression):
        # Expr
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class ExprLiteral(Expr):
    def __init__(self, value):
        # Object
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class ExprLogical(Expr):
    def __init__(self, left, operator, right):
        # Expr
        self.left = left

        # Token
        self.operator = operator

        # Expr
        self.right = right

    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)


class ExprUnary(Expr):
    def __init__(self, operator, right):
        # Token
        self.operator = operator

        # Expr
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


class ExprVariable(Expr):
    def __init__(self, name):
        # Token
        self.name = name

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
