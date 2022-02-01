from NotOrientedGraphModule import NotOrientedGraph

raw_graph = NotOrientedGraph(33, 'no', 0.3, 0.9, 'yes')
test_graph = raw_graph.build_graph()

#test_graph.set_N(-1)
#test_graph.set_lower_bound(0.9)
#test_graph.set_complete(876)
#print(test_graph.__dict__)

print(test_graph.edges)
print(test_graph.nodes.data())
print([test_graph[node] for node in test_graph])
print(test_graph[4])
NotOrientedGraph.draw_graph(raw_graph)

