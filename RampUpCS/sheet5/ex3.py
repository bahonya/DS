from rdflib import Graph

g = Graph()
g.parse('exercise3.ttl', format='turtle')


q1 = """
    ASK {<http://ifisexamples.com/Alan_Turing> rel:childOf <http://ifisexamples.com/Julius_Turing>}
"""

q2 = """
    SELECT ?g
    WHERE {?g rel:childOf/rel:childOf <http://ifisexamples.com/Ethel_Turing>}
"""

q3 = """
    SELECT ?g
    WHERE {?g rel:birthYear ?b
    FILTER(?b < 1880)}
"""


for stmt in g.query(q1):
    print(stmt)

for stmt in g.query(q2):
    print(stmt)

for stmt in g.query(q3):
    print(stmt)