class Stmt(object):
    class Visitor(object):
        # Stmt.Expression stmt
        def visitExpressionStmt(stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitExpressionStmt()'.format(self.__class__.__name__))

        # Stmt.Print stmt
        def visitPrintStmt(stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitPrintStmt()'.format(self.__class__.__name__))

        # Stmt.Var stmt
        def visitVarStmt(stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitVarStmt()'.format(self.__class__.__name__))


class StmtExpression(Stmt):
    def __init__(self, expression):
        # Expr
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


class StmtPrint(Stmt):
    def __init__(self, expression):
        # Expr
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)


class StmtVar(Stmt):
    def __init__(self, type_name, name, initializer):
        # Str
        self.type_name = type_name

        # Token
        self.name = name

        # Expr
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVarStmt(self)
