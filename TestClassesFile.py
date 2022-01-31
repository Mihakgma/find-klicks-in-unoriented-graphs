from InorientedGraphModule import InorientedGraph

test_graph = InorientedGraph(25,'no',0.5,0.9,'yes').build_graph()


#test_graph.set_N(-1)
#test_graph.set_lower_bound(0.9)
#test_graph.set_complete(876)
#print(test_graph.__dict__)
print(test_graph.edges)
print(test_graph.nodes.data())
print([test_graph[node] for node in test_graph])