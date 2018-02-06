Python 3.7.0a2 (v3.7.0a2:f7ac4fe, Oct 17 2017, 16:23:57) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import networkx as nx
>>> import networkx as nx
G=nx.DiGraph();
G.add_node("Start")
G.add_node("End")
G.add_node("Pickup")
G.add_node("PutDown")
G.add_node("E1")
G.add_node("E2")
G.add_node("N1")
G.add_node("N2")
G.add_node("N3")
G.add_node("S1")
G.add_node("S2")
G.add_node("S3")
G.add_node("S4")
G.add_node("W1")
weights=[
0: "taxi.loc",
1: "pass.loc",
2: "pass.dest"]
SyntaxError: multiple statements found while compiling a single statement
>>> G=nx.DiGraph();
>>> G.add_node("Start")
>>> G.add_node("End")
>>> G.add_node("Pickup")
>>> G.add_node("PutDown")
>>> G.add_node("E1")
>>> G.add_node("E2")
>>> G.add_node("N1")
>>> G.add_node("N2")
>>> G.add_node("N3")
>>> G.add_node("S1")
>>> G.add_node("S2")
>>> G.add_node("S3")
>>> G.add_node("S4")
>>> G.add_node("W1")
>>> weights=[0: "taxi.loc", 1:"pass.loc", 2:"pass.dest"]
SyntaxError: invalid syntax
>>> w0="taxi.loc"
>>> w1="pass.loc"
>>> w2="pass.dest"
>>> G.add_weighted_edges_from([("Start", "E1", w0),("E1","E2",w0),("E2","N1",w0),("N1","N2",w0),("N2","N3",w0),("N3","Pickup",w0)])
>>> G.add_weighted_edges_from([("Pickup","S1",w0),("S1","S2",w0),("S2","S3",w0),("S3","S4",w0),("S4","W1",w0),("W1","Putdown",w0),("Putdown","End",w0), ("Start","Pickup",w1),("Pickup","Putdown",w1), ("Start","PutDown",w2),("Putdown","End",w1),("Putdown","End",w2)])
>>> import matplotlib.pyplot as plt
Traceback (most recent call last):
  File "<pyshell#23>", line 1, in <module>
    import matplotlib.pyplot as plt
ModuleNotFoundError: No module named 'matplotlib'
>>> G.edges()
OutEdgeView([('Start', 'E1'), ('Start', 'Pickup'), ('Start', 'PutDown'), ('Pickup', 'S1'), ('Pickup', 'Putdown'), ('E1', 'E2'), ('E2', 'N1'), ('N1', 'N2'), ('N2', 'N3'), ('N3', 'Pickup'), ('S1', 'S2'), ('S2', 'S3'), ('S3', 'S4'), ('S4', 'W1'), ('W1', 'Putdown'), ('Putdown', 'End')])
>>> 
