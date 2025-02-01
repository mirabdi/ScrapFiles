import pygraphviz as pgv

# Load the DOT file
dot_file = "schema.dot"
graph = pgv.AGraph(dot_file)

# Save as GraphML for yEd
graph.write("schema.graphml")
