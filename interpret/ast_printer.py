from token_type import TokenType
from token import Token
from expr import *


class AstPrinter(Expr.Visitor):
    def printExpr(self, expr):
        return expr.accept(self)

# # Testing
# expression = ExprBinary(
# 		ExprUnary(
# 			Token(TokenType.MINUS, "-", None, 1),
# 			ExprLiteral(123)),
# 		Token(TokenType.STAR, "*", None, 1),
# 		ExprGrouping(
# 			ExprLiteral(45.67)));
#
# print(AstPrinter().printExpr(expression))
