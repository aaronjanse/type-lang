class Stmt(object):
    class Visitor(object):
        # Stmt.Block stmt
        def visitBlockStmt(self, stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitBlockStmt()'.format(self.__class__.__name__))

        # Stmt.Expression stmt
        def visitExpressionStmt(self, stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitExpressionStmt()'.format(self.__class__.__name__))

        # Stmt.If stmt
        def visitIfStmt(stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitIfStmt()'.format(self.__class__.__name__))

        # Stmt.Print stmt
        def visitPrintStmt(self, stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitPrintStmt()'.format(self.__class__.__name__))

        # Stmt.Var stmt
        def visitVarStmt(self, stmt):
            raise NotImplementedError(
                'Class {} doesn\'t implement visitVarStmt()'.format(self.__class__.__name__))


class StmtBlock(Stmt):
    def __init__(self, statements):
        # List<Stmt>
        self.statements = statements

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


class StmtExpression(Stmt):
    def __init__(self, expression):
        # Expr
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


class StmtIf(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        # Expr
        self.condition = condition

        # Stmt
        self.thenBranch = thenBranch

        # Stmt
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visitIfStmt(self)


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
