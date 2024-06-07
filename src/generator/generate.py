#!/usr/bin/env python3

import sys
import pydot
from pydot import Graph, Node, Edge

from python_classes import PythonModule, PythonClass, PythonClassType, PythonMethod, HISTORY

END_METHOD = "sql"
START_NODE = "START"
END_NODE = "END"

class ForwardMap():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.map = self.generate_forward_map()

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

def node_is_target(node: Node):
    parts = node.get_name().split("_")
    return len(parts) > 1 and parts[1] == "TARGET"

def node_is_specifier(node: Node):
    parts = node.get_name().split("_")
    return len(parts) > 1 and parts[1] == "SPECIFIER"


def create_class(node, node_map: ForwardMap):

    class_name = node.get_label()
    t = PythonClassType.DIRECTIVE
    if not class_name:
        class_name = node.get_name()
        if class_name == "START":
            t = PythonClassType.START
            class_name = "Query"
        elif class_name == END_NODE:
            t = PythonClassType.END

    python_class = PythonClass(class_name, type=t)

    next_nodes = node_map.get(node.get_name())
    for next_node in next_nodes:

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
        
        if python_class.type == PythonClassType.END:
            # We do not need a class for the ending method.
            # It should return a string instead.
            continue

        if node_is_specifier(this_node):
            python_class.extra_args = []
            python_class.type = PythonClassType.SPECIFIER

        classes.append(python_class)

    return classes

def populate_methods(module: PythonModule):

    for python_class in module.classes:
        for method in python_class.methods:
            if method.name == END_NODE:
                method.name = END_METHOD
                method.returns = f"make_sql(self.{HISTORY})"
                continue
            method_class = module.find_class(method.name)
            method.args = method_class.extra_args
            method.returns = f"{method_class.name}({', '.join(method_class.extra_args + [f'{HISTORY}=self.{HISTORY}'])})"
            if method_class.type == PythonClassType.SPECIFIER:
                method.property = True

        # Add __repr__ method
        fields = list(map(lambda x: f"{{self.{x}}}", python_class.extra_args))
        repr = ""
        if len(fields) > 0: repr = f'f"{python_class.name} {", ".join(fields)}"'
        else:               repr = f'f"{python_class.name}"'
        method = PythonMethod("__repr__", returns=repr)
        python_class.methods.append(method)

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
    module = PythonModule(classes, [f"from query_builder.query_to_sql import make_sql"])
    module.imports
    populate_methods(module)

    with open(output_path, "w") as f:
        f.write(str(module.code()))
