# LWWElementGraph

This was a programming assignment for a software engineering company. Although I included unit tests, there was still a bug in the code. I decided to save it here because I found it educational.

The task is to implement a Last Writer Wins Element Graph, which is a kind of graph which can be edited collaboratively. Everyone has a local copy of the graph and can add and remove vertices and edges. A record is kept of when vertices and edges have been added or removed. The local copies can be merged into a global copy by taking the union of the sets of added and removed vertices.

## Notes

I am not a software engineering person, so this assignment was very unfamiliar to me.

The definition of LWW Element Set seemed fairly clear to me, although I was not sure what should happen when you remove an element which is not currently in the set. I decided it would be easier if arbitrary removal of elements was allowed.

I decided to allow arbitrary timestamps because when prototyping, I wanted to allow the timestamps to be integers. I also wanted it to be possible to edit the graph in the past. In practice, I envisage that the timestamps would be a datetime data type (as in the demo).

There was no firm definition for LWW Element Graph, but it seemed that you would need a lot of the functionality of LWW Element Set.

Therefore, I first wrote an LWW Element Set class. I then defined an LWW Element Graph to be a pair of LWW Element Sets (vertices and edges) with special methods for what happens when you remove a vertex or edge.

It turned out that for some reason related to Python, the edges have to be frozenset types instead of sets.

I had particular trouble with the notion of what should happen when you remove a vertex. It seems that you should remove all hanging edges as well. However, after you do a merge, there can still be hanging edges which were not removed when you deleted the vertex.

For example, suppose there are two copies of the graph A—B and the vertex B is deleted from one copy. Then the edge A—B should be deleted as well. But after the merge, the edge A—B still exists in the merged graph, but the vertex B does not.

I decided to get round this by requiring that one of the conditions for an edge to exist is that the vertices also exist. 

In general, I thought that it would be easier if I allowed as much leeway in the contents of the add sets/remove sets as possible, and put most of the logic in the membership methods such as hasEdge, rather than writing complicated methods to check if a particular add/remove operation was permitted.

I did not do any optimization. For example, the path finding algorithm is not fast. Also, I only did the most rudimentary type checking in the code. *(Note: this was where the bug was, or at least the only bug they told me about)*

I also wrote a Jupyter notebook showing how the LWW Element Graph works when two people are editing a graph concurrently, and to demonstrate the expected usage.

Files:

`lwwelementset.py`
`lwwelementset_tests.py`
`lwwelementgraph.py`
`lwwelementgraph_tests.py`
`exceptions.py`
`lwwelementgraph_demo.ipynb`
