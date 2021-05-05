# -*- coding: utf-8 -*-

import unittest
from lwwelementset import LWWElementSet
from lwwelementgraph import LWWElementGraph
from exceptions import NonExistentVertex

class testLWWElementGraph(unittest.TestCase):
    
    def test_addVertex(self):
            
        # create instance of LWWElementGraph
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        g = LWWElementGraph(vertices, edges)
        
        # add vertex 1 at timestamp 0
        g.addVertex(1, 0)
        
        self.assertEqual(g.hasVertex(1, 0), True)
        
    def test_removeVertex(self):
        
        # create instance of LWWElementGraph
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        g = LWWElementGraph(vertices, edges)
        
        # add vertex 1 at time 0, then remove it at time 1
        g.addVertex(1, 0)
        g.removeVertex(1, 1)
        
        self.assertEqual(g.hasVertex(1, 1), False)
        
    def test_addEdge(self):
        
        # create instance of LWWElementGraph
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        g = LWWElementGraph(vertices, edges)
        
        g.addVertex(1, 0)
        g.addVertex(2, 0)
        g.addEdgeBetween(1, 2, 0)
        
        self.assertEqual(g.hasEdgeBetween(1, 2, 0), True)
        
        # check that removing a vertex also removes the trailing edges
        g.removeVertex(2, 1)
        
        self.assertEqual(g.hasEdgeBetween(1, 2, 1), False)
        
        # check that deleted edge does not magically reappear when you re-add the vertex which was just removed. I am not sure whether this is the expected behaviour?
        g.addVertex(2, 2)
        
        self.assertEqual(g.hasEdgeBetween(1, 2, 2), False)
        
        # check that you can't add an edge if an endpoint does not exist
        # try to add an edge between 2 and 3 at time 2
        self.assertRaises(NonExistentVertex, g.addEdgeBetween, 2, 3, 2)
        
        # try to add an edge between 'a' and 'b' at time -1
        self.assertRaises(NonExistentVertex, g.addEdgeBetween, 'a', 'b', -1)
        
    def test_removeEdge(self):
        
        # create instance of LWWElementGraph
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        g = LWWElementGraph(vertices, edges)
        
        g.addVertex(1, 0)
        g.addVertex(2, 0)
        g.addEdgeBetween(1, 2, 0)

        self.assertEqual(g.hasEdgeBetween(1, 2, 0), True)
        
        # remove the edge and check that it is gone
        g.removeEdgeBetween(1, 2, 1)
        
        self.assertEqual(g.hasEdgeBetween(1, 2, 1), False)
        
        
    def test_findAllVerticesConnectedTo(self):
        
        # create instance of LWWElementGraph
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        g = LWWElementGraph(vertices, edges)
        
        g.addVertex(1, 0)
        g.addVertex(2, 0)
        g.addVertex(3, 0)
        
        g.addEdgeBetween(1, 1, 0)
        g.addEdgeBetween(1, 2, 0)   
        g.addEdgeBetween(1, 3, 0)
        
        # check that 1 is connected to 1, 2, and 3
        self.assertEqual(g.findAllVerticesConnectedTo(1, 1), set([1,2,3]))
        
        g.removeEdgeBetween(1, 1, 1)
        # check that 1 is now only connected to 2 and 3
        # graph is now 3---1---2
        self.assertEqual(g.findAllVerticesConnectedTo(1, 1), set([2,3]))
        
        # remove Vertex 2 at time 2
        # graph is now 1---3
        g.removeVertex(2, 2)
        
        self.assertEqual(g.findAllVerticesConnectedTo(1, 2), set([3]))
        
        # add back vertex 2 and check that 1 and 2 are not reconnected
        g.removeVertex(2, 3)
        
        self.assertEqual(g.findAllVerticesConnectedTo(1, 3), set([3]))

        # add another vertex connected to 3 but not 1
        # graph is now 1---3---4 at timestamp 4
        g.addVertex(4, 4)
        g.addEdgeBetween(3, 4, 4)

        self.assertEqual(g.findAllVerticesConnectedTo(1, 4), set([3]))
        
    def test_findAnyPathBetweenTwoVertices(self):

        # create instance of LWWElementGraph
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        g = LWWElementGraph(vertices, edges)
        
        g.addVertex(1, 0)
        g.addVertex(2, 0)
        g.addVertex(3, 0)
        
        g.addEdgeBetween(1, 1, 0)
        g.addEdgeBetween(1, 2, 0)   
        g.addEdgeBetween(2, 3, 0)

        self.assertEqual(g.findAnyPathBetweenTwoVertices(1, 3, 0), True)
        
        # check that there is no longer a path if you remove the middle vertex
        g.removeVertex(2, 1)
        
        self.assertEqual(g.findAnyPathBetweenTwoVertices(1, 3, 1), False)
        
        # check that there is a path from 1 to 1
        self.assertEqual(g.findAnyPathBetweenTwoVertices(1, 1, 1), True)

        
    def test_merge(self):
        """
        Alice adds vertex v at time 0
        Bob adds vertex v at time 0
        Alice adds edge {v, v} at time 1
        Bob deletes vertex v at time 2
        
        When the two graphs are merged, the edge {v, v} exists at time 2 but
        the vertex v doesn't. So the edge {v, v} should not exist either
        """
        vertices = LWWElementSet(set([]), set([]))
        edges = LWWElementSet(set([]), set([]))
        
        Alice = LWWElementGraph(vertices, edges)
        
        verticesB = LWWElementSet(set([]), set([]))
        edgesB = LWWElementSet(set([]), set([]))
        
        Bob = LWWElementGraph(verticesB, edgesB)
        
        Alice.addVertex('v', 0)
        Bob.addVertex('v', 0)
        Alice.addEdgeBetween('v', 'v', 1)
        Bob.removeVertex('v', 2)
        
        # the merged graph should be empty because Bob deleted the only vertex
        self.assertEqual(Alice.merge(Bob).hasVertex('v', 2), False)
        self.assertEqual(Alice.merge(Bob).hasEdgeBetween('v', 'v', 2), False)
        
    
class testLWWElementGraphCRDT(unittest.TestCase):
    """
    LWWElementGraph is supposed to be a CRDT, which means that merging should be commutative, associative and idempotent, so need to test this
    
    x.merge(x) == x
    x.merge(y) == y.merge(x)
    (x.merge(y)).merge(z) == x.merge(y.merge(z))
    """    
    def test_crdt(self):
        x = LWWElementGraph(LWWElementSet(set([]), set([])), LWWElementSet(set([]), set([])))
        y = LWWElementGraph(LWWElementSet(set([]), set([])), LWWElementSet(set([]), set([])))
        z = LWWElementGraph(LWWElementSet(set([]), set([])), LWWElementSet(set([]), set([])))
        
        x.addVertex('a', 0)
        x.addVertex('b', 0)
        x.addEdgeBetween('a', 'b', 0)
        
        y.addVertex('b', 0)
        y.addVertex('c', 0)
        y.addEdgeBetween('c', 'b', 0)  
            
        z.addVertex('c', 0)
        z.addVertex('d', 0)
        z.addEdgeBetween('c', 'd', 0)   
        
        self.assertEqual(x.merge(x), x)
        self.assertEqual(x.merge(y), y.merge(x))
        self.assertEqual( (x.merge(y)).merge(z), x.merge(y.merge(z)) )
        
        
        


