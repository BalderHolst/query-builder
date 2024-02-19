import pydot
from pydot import Graph, Node, Edge

def generate_name_to_node_map(graph: Graph):
    nodes: list[Node] = graph.get_nodes()
    name_to_node = {}
    for n in nodes:
        name = n.get_name()
        name_to_node[name] = n
    return name_to_node

def generate_forward_map(graph: Graph):
    edges: list[Edge] = graph.get_edges()
    name_to_node = generate_name_to_node_map(graph)
    forward_map = {}
    for e in edges:
        from_node = name_to_node[e.get_source()]
        to_node = name_to_node[e.get_destination()]

        if not from_node in forward_map:
            forward_map[from_node] = [to_node]
        else:
            forward_map[from_node].append(to_node)
    return forward_map

class Code:
    def __init__(self):
        self.lines = []
        self.current_indent = 0

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

def main():
    graph: Graph = pydot.graph_from_dot_file("./grammar.dot")[0]

    node_map = generate_forward_map(graph)

    classes = []

    for (k, v) in node_map.items():

        if node_is_target(k): continue

        class_name = k.get_label()
        if not class_name: class_name = k.get_name()

        class_args = []
        class_methods = []

        for after in v:

            if node_is_target(after):
                class_args.append(after.get_label())
                for n in node_map[after]:
                    if not n.get_label(): class_methods.append(n.get_name())
                    else: class_methods.append(n.get_label())

            else:
                after_method = after.get_label()
                if not after_method: after_method = after.get_name()
                class_methods.append(after_method)


        classes.append({
            "name": class_name,
            "args": class_args,
            "methods": class_methods
        })

    module = Code()

    for class_ in classes:

        c = Code()
        c.line(f"class {class_['name']}:")
        c.indent()

        if len(class_['args']) > 0:
            c.line(f"def __init__(self, history, {', '.join(class_['args'])}):")
            c.indent()
            c.line("self.history = history")
            c.line(f"self.history.append('{class_['name']}')")
            for arg in class_['args']:
                c.line(f"self.history.append({arg})")
            c.unindent()
        else:
            c.line("def __init__(self, history):")
            c.indent()
            c.line("self.history = history")
            c.line(f"self.history.append('{class_['name']}')")
            c.unindent()
        c.line("")

        for method in class_['methods']:

            extra_args = []
            for cl in classes:
                if method == cl['name']:
                    extra_args = cl['args']
                    break

            method_code = ""
            if len(extra_args) > 0:
                method_code += f"def {method}(self, {', '.join(extra_args)}): "
            else:
                method_code += f"def {method}(self): "
            method_code += f"return {method}(self.history, {', '.join(extra_args)})"

            c.line(method_code)

        # Add repr
        c.line("def __repr__(self): return ' '.join(self.history)")

        c.line("")

        module.extend(c)

    text = module.text()
    with open("out.py", "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()
