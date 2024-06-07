from enum import Enum

HISTORY = "_history"

class Code:
    def __init__(self, indent = 0):
        self.lines = []
        self.current_indent = indent

    def text(self) -> str:
        return "\n".join(self.lines)

    def line(self, s: str):
        self.lines.append("    " * self.current_indent + s)

    def indent(self):
        self.current_indent += 1

    def unindent(self):
        self.current_indent -= 1

    def extend(self, other):
        self.lines.extend(other.lines)

    def __repr__(self):
        return self.text()

class PythonClassType(Enum):
    DIRECTIVE = 0,
    SPECIFIER = 1,
    START = 2,
    END = 3,

class PythonClass:
    def __init__(self, name: str, type: PythonClassType = PythonClassType.DIRECTIVE):
        self.name = name
        self.extra_args = []
        self.methods: list[PythonMethod] = []
        self.flags = []
        self.type = type

    def args(self):
        return self.extra_args + [f"{HISTORY}=[]"]

    def code(self) -> str:
        c = Code()
        c.line(f"class {self.name}:")
        c.indent()

        args = ["self"] + self.args() + list(map(lambda x: f"{x}=false", self.flags))

        if self.type == PythonClassType.START:
            c.line(f"def __init__(self): self.{HISTORY} = []")
        else:
            c.line(f"def __init__({', '.join(args)}):")
            c.indent()
            c.line(f"self.{HISTORY} = {HISTORY} + [self]")

            for arg in self.extra_args:
                c.line(f"self.{arg} = {arg}")
            c.unindent()

        for method in self.methods:
            c.extend(method.code(indent=c.current_indent))

        c.unindent()

        c.line("")

        return c
    
    def __repr__(self) -> str:
        return f"Class {self.name}"

class PythonMethod:
    def __init__(self, name: str, args=[], returns=None, property=False):
        self.name = name
        self.args = args
        self.returns = returns
        self.property = property

    def code(self, indent = 0) -> str:
        c = Code(indent=indent)

        body = "pass"
        if self.returns: body = f"return {self.returns}"
        if self.property: c.line("@property")
        args = ["self"] + self.args
        c.line(f"def {self.name}({', '.join(args)}): {body}")
        return c

    def __repr__(self) -> str:
        return f"{self.name}{tuple(self.args)}"

class PythonModule:
    def __init__(self, classes: list[PythonClass], imports = []):
        self.classes = classes
        self.imports = imports

    def find_class(self, name: str):
        for python_class in self.classes:
            if python_class.name == name:
                return python_class
        print(f"ERROR: DID NOT FIND '{name}'")
        exit(1)

    def code(self) -> str:
        c = Code()

        for imp in self.imports:
            c.line(imp)

        for python_class in self.classes:
            c.line("")
            c.extend(python_class.code())
        return c
