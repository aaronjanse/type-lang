def defineAst(basename, types):
    print("class {}(object):".format(basename))

    defineVisitor(basename, types)

    for type_ in types:
        className = type_.split(":")[0].strip();
        fields = type_.split(":")[1].strip();
        defineType(basename, className, fields)


def defineVisitor(basename, types):
    print("\tclass Visitor(object):")

    for type_ in types:
        typeName = type_.split(":")[0].strip()
        print("\t\t# {}.{} {}".format(basename, typeName, basename.lower()))
        print("\t\tdef visit{}({}):".format(
            typeName + basename, basename.lower()))
        print("\t\t\traise NotImplementedError('Class {} doesn\\'t implement visit{}()'.format(self.__class__.__name__))".format(
            '{}', typeName + basename))
        print()


def defineType(basename, className, fieldList):
    print("")
    print("class {1}{0}({1}):".format(className, basename))

    fields = fieldList.split(", ")

    parameters = []

    for field in fields:
        tokens = field.split(' ')
        parameters.append(tokens[1].strip())

    parameters = ', '.join(parameters)

    # Constructor.
    print("\tdef __init__(self, {}):".format(parameters))

    # Store parameters in fields.
    fields = fieldList.split(", ")
    for field in fields:
        tokens = field.split(' ')
        print("\t\t# {}".format(tokens[0]))
        print("\t\tself.{0} = {0}".format(tokens[1]))
        print()

    print()
    print("\tdef accept(self, visitor):");
    print("\t\treturn visitor.visit{}(self);".format(className + basename))


defineAst("Expr", [
    "Assign   : Token name, Expr value",
    "Binary   : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal  : Object value",
    "Logical  : Expr left, Token operator, Expr right",
    "Unary    : Token operator, Expr right",
    "Variable : Token name"
])

# defineAst("Stmt", [
#       "Block      : List<Stmt> statements",
#       "Expression : Expr expression",
#       "If         : Expr condition, Stmt thenBranch, Stmt elseBranch",
#       "Print      : Expr expression",
#       "Var        : Token name, Expr initializer"
#       ])
