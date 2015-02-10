"""
"""
import igraph

def computeCd(g):
    n = len(g.vs)
    maxDegree = max(g.degree())
    sum = 0
    for vertex in g.vs():
        sum = sum + (maxDegree - vertex.degree())
    return (float(sum)/(n**2-3*n+2))

def computeCb(g):
    n = len(g.vs)
    maxCb = max(g.betweenness())
    sum = 0
    for vertex in g.vs():
        sum = sum + (maxCb - vertex.betweenness() )
    return (2*float(sum)/(n**3-4*n**2+5*n-2))

def computeCc(g):
    n = len(g.vs)
    maxCc = max(g.closeness())
    sum = 0
    for vertex in g.vs():
        sum = sum + (maxCc - vertex.closeness())
    return (float(sum*(2*n-3))/(n**2-3*n+2))
