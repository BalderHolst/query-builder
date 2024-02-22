#!/usr/bin/env python3

import sys
from enum import Enum
import pydot
from pydot import Graph, Node, Edge

HISTORY_VAR = "history"

class ForwardMap():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.map = self.generate_forward_map()
        print(self.map)

    def generate_forward_map(self):
        edges: list[Edge] = self.graph.get_edges()
        name_to_node = self.generate_name_to_node_map()
        forward_map = {}
        for e in edges:
            from_node_name = e.get_source()
            to_node = name_to_node[e.get_destination()]

            if not from_node_name in forward_map:
                forward_map[from_node_name] = [to_node]
            else:
                forward_map[from_node_name].append(to_node)
        return forward_map

    def generate_name_to_node_map(self):
        nodes: list[Node] = self.graph.get_nodes()
        name_to_node = {}
        for n in nodes:
            name = n.get_name()
            name_to_node[name] = n
        return name_to_node

    def get(self, node: str):
        if node in self.map:
            return self.map[node]
        else:
            return []


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

def node_is_target(node: Node):
    parts = node.get_name().split("_")
    return len(parts) > 1 and parts[1] == "TARGET"

def node_is_specifier(node: Node):
    parts = node.get_name().split("_")
    return len(parts) > 1 and parts[1] == "SPECIFIER"


class PythonMethod:
    def __init__(self, name: str):
        self.name = name
        self.args = []
        self.returns = None
        self.property = False

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
        return self.extra_args + [f"{HISTORY_VAR}=[]"]

    def code(self) -> str:
        c = Code()
        c.line(f"class {self.name}:")
        c.indent()

        args = ["self"] + self.args() + list(map(lambda x: f"{x}=false", self.flags))

        c.line(f"def __init__({', '.join(args)}):")
        if len(args) <= 1:
            c.indent(); c.line("pass"); c.unindent()

        c.indent()
        c.line(f"self.history = history + ['{self.name.replace('_', ' ')}']")
        for arg in self.extra_args:
            c.line(f"self.{arg} = {arg}")
        c.unindent()

        for method in self.methods:
            c.extend(method.code(indent=c.current_indent))
        c.line(f"def __repr__(self): return ' '.join(self.history)")

        c.unindent()

        c.line("")

        return c
    
    def __repr__(self) -> str:
        return f"Class {self.name}"

class PythonModule:
    def __init__(self, classes: list[PythonClass]):
        self.classes = classes

    def find_class(self, name: str):
        for python_class in self.classes:
            if python_class.name == name:
                return python_class
        print(f"ERROR: DID NOT FIND '{name}'")
        exit(1)

    def code(self) -> str:
        c = Code()
        for python_class in self.classes:
            c.line("")
            c.extend(python_class.code())
        return c

def create_class(node, node_map: ForwardMap):

    class_name = node.get_label()
    t = PythonClassType.DIRECTIVE
    if not class_name:
        class_name = node.get_name()
        if class_name == "START": t = PythonClassType.START
        elif class_name == "END": t = PythonClassType.END

    python_class = PythonClass(class_name, type=t)

    next_nodes = node_map.get(node.get_name())
    for next_node in next_nodes:
        print("\t", next_node.get_name())

        # Is it an argument?
        if node_is_target(next_node):
            arg = next_node.get_label()
            python_class.extra_args.append(arg)
            new_class = create_class(next_node, node_map)
            python_class.methods = new_class.methods
            continue
        
        method_name = next_node.get_label()
        if not method_name: method_name = next_node.get_name()
        python_class.methods.append(PythonMethod(method_name))

    return python_class



def create_classes(grammar_path: str):
    graph: Graph = pydot.graph_from_dot_file(grammar_path)[0]
    node_map = ForwardMap(graph)

    classes: list[PythonClass] = []

    for this_node in graph.get_nodes():
        if node_is_target(this_node): continue
        python_class = create_class(this_node, node_map)

        if node_is_specifier(this_node):
            python_class.extra_args = []
            python_class.type = PythonClassType.SPECIFIER

        print(python_class.name, python_class.methods)
        classes.append(python_class)

    return classes

def populate_methods(module: PythonModule):

    for python_class in module.classes:
        for method in python_class.methods:
            method_class = module.find_class(method.name)
            method.args.extend(method_class.extra_args)
            method.returns = f"{method_class.name}({', '.join(method_class.extra_args + ['history=self.history'])})"
            if method_class.type == PythonClassType.SPECIFIER:
                method.property = True

def usage():
    print(f"{sys.argv[0]} <grammar> <output-path>")

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Error incorrect number of arguments.")
        usage()
        exit(1)

    grammar_path = sys.argv[1]
    output_path = sys.argv[2]

    classes = create_classes(grammar_path)
    module = PythonModule(classes)
    populate_methods(module)

    with open(output_path, "w") as f:
        f.write(str(module.code()))
