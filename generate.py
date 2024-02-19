import pydot

graphs = pydot.graph_from_dot_file("./grammar.dot")
graph: pydot.Graph = graphs[0]

graph.write_png("grammar.png")

edges: list[pydot.Edge] = graph.get_edges()

for e in edges:
    print(e)
