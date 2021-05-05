# -*- coding: utf-8 -*-

from lwwelementset import LWWElementSet
from exceptions import NonExistentVertex

class LWWElementGraph:
    """
    LWWElementGraph class
    
    An LWWElementGraph object consists of vertices and edges. Vertices and edges are LWW element sets. But there are the following conditions:
        
        - You can only add an edge if its endpoints exist
        - When you remove a vertex, you remove all hanging edges
        - An edge only exists if its endpoints exist (you can get an edge without its endpoints if two LWWElementGraph objects are merged)
    """
    
    
    def __init__(self, vertices, edges):
        
        if not isinstance(vertices, LWWElementSet) or not isinstance(edges, LWWElementSet):
            raise TypeError
        
        self.vertices = vertices
        self.edges = edges
        
    def __eq__(self, other):
        # this is required because we need to test that merging is commutative etc.
        # which requires that we can test LWWElementGraph objects for equality
        return self.vertices.__eq__(other.vertices) and self.edges.__eq__(other.edges)
        
    def __repr__(self):
        """
        print the contents of the object, for debugging
        """
        return 'vertices:\n' + self.vertices.__repr__() +'\nedges:\n' + self.edges.__repr__()
    
    def addVertex(self, x, timestamp):
        """
        add vertex x at timestamp
        """
        self.vertices.addElement(x, timestamp)        
        
    def removeVertex(self, x, timestamp):
        """
        remove vertex x at timestamp
        also remove all trailing edges
        """
        self.vertices.removeElement(x, timestamp)
        
        # remove all trailing edges
        # every potential trailing edge must be in the addset. If it's already 
        # been deleted, there is no harm in removing it again (or is there?)
        for e in self.edges.addSet:
            if (x in e[0]):# and (self.hasEdge(e[0], timestamp)):
                self.edges.removeElement(e[0], timestamp)
        
    def addEdge(self, e, timestamp):
        """
        add edge e at timestamp, but only if its endpoints exist
        """
        for v in e:
            if not self.hasVertex(v, timestamp):
                # raise exception
                raise NonExistentVertex('Cannot add edge if not all endpoints exist.')     
        # if no exception was raised
        self.edges.addElement(e, timestamp)
        
    def addEdgeBetween(self, v1, v2, timestamp):
        """
        add edge between v1 and v2 at timestamp. A more convenient version of addEdge. v1 and v2 should be vertices in the graph
        """
        self.addEdge(frozenset([v1, v2]), timestamp)
        
    def removeEdge(self, e, timestamp):
        """
        remove edge e at timestamp
        """
        self.edges.removeElement(e, timestamp)
        
    def removeEdgeBetween(self, v1, v2, timestamp):
        """
        remove edge e at timestamp where e is specified by its endpoints
        """
        self.removeEdge(frozenset([v1, v2]), timestamp)
        
    def hasVertex(self, x, timestamp):    
        """
        check if vertex x exists at timestamp
        """
        return self.vertices.snapshot(timestamp).contains(x)
        
    def hasEdge(self, e, timestamp):
        """
        check if edge e exists at timestamp
        
        need to check if the endpoints exist as well because it's possible
        for an edge to exist but its vertices not exist. For example:
            
        Alice adds vertex v at time 0
        Bob adds vertex v at time 0
        Alice adds edge {v, v} at time 1
        Bob deletes vertex v at time 2
        
        When the two graphs are merged, the edge {v, v} exists at time 2 but
        the vertex v doesn't. So the edge {v, v} should not exist either
        """
        if self.edges.snapshot(timestamp).contains(e):
            # check whether vertices exist
            for v in e:
                # if a vertex does not exist, false
                if not self.hasVertex(v, timestamp):
                    return False
            # if edge exists and all vertices exist, true
            return True
        # if edge does not exist, false
        return False
    
    def hasEdgeBetween(self, v1, v2, timestamp):
        """
        check if edge between v1 and v2 exists at timestamp
        """
        return self.hasEdge(frozenset([v1, v2]), timestamp)
    
    def merge(self, other):
        """
        merge two LWWElementGraph objects together
        """
        
        # create empty sets of vertices and edges
        v = LWWElementSet(set([]), set([]))
        e = LWWElementSet(set([]), set([]))
        
        # create an object to be the result of the merge
        merged = LWWElementGraph(v, e)
        
        # populate the merged object
        merged.vertices = self.vertices.merge(other.vertices)
        merged.edges = self.edges.merge(other.edges)
        
        return merged
    
    def findAllVerticesConnectedTo(self, v, timestamp):
        """
        find all vertices connected to vertex v at timestamp
        (because the graph can have loops, {v, v} = {v} can be an edge)
        """
        # list to store the results
        out = []
        
        for e in self.edges.addSet:
            if (v in e[0]) and self.hasEdge(e[0], timestamp):
                if len(e[0]) == 1:
                    out += [v]
                else:
                    # e has exactly two elements
                    # add the single element which is not v
                    out += list( e[0].difference(set([v])) )
                    
        # return results as a set
        return set(out)
    
    def findAnyPathBetweenTwoVertices(self, v1, v2, timestamp):
        """
        Return True if there is a path between v1 and v2 in the graph at timestamp
        
        Notes:
        ------
        I'm not sure whether this is asking for all paths, or whether a path exists? I think the easiest way to do this is to extract a graph from the LWW Element graph at the timestamp and then use the networkx library to find the paths.  However, I am not sure whether I am allowed to use the networkx library
        
        Also, I am not sure whether there is a path between v and v if there is no loop at v? It is easier to assume that there is a path, even if there is no loop
        """
        # check whether the vertices are in the graph
        if not (self.hasVertex(v1, timestamp) and self.hasVertex(v2, timestamp)):
            raise NonExistentVertex('Vertex does not exist')
        
        v1_neighbourhood = set([])
        v1_neighbourhood_next = set([v1])
        
        # grow the neighbourhood of v1 until it has maximum size
        while v1_neighbourhood != v1_neighbourhood_next:
            v1_neighbourhood = v1_neighbourhood_next.copy()
            
            for e in self.edges.addSet:
                if self.hasEdge(e[0], timestamp):
                    if v1 in e[0]:
                        # if the edge e[0] contains v1, add the other vertex in e[0] to the neighbourhood. Submission was rejected because of a bug in this part which previously had v1_neighbourhood_next.union(e[0])
                        v1_neighbourhood_next = v1_neighbourhood_next.union(e[0].difference(set([v1])))
            #print(v1_neighbourhood)
            #print(v1_neighbourhood_next)
        
        # check whether maximal neighbourhood of v1 contains v2            
        if v2 in v1_neighbourhood:
            return True
        return False