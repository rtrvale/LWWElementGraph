# -*- coding: utf-8 -*-

import numpy as np

class LWWElementSet:
    """
    Last Writer Wins Element Set Class
    
    The task is to create a Last Writer Wins graph class, but I think that a graph has an LWW set of vertices and LWW set of edges, so it should be based on an LWW set class with some special read and write methods.
    
    Examples:
    ---------
    # create an object
    x = LWWElementSet(set([]), set([]))
    
    # add element at timestamp 0
    x.addElement(1, 0)
    
    # there is no control over what timestamps are, since they could be objects
    import pandas as pd
    x.addElement(2, pd.to_datetime('2020-01-01'))
    # note that x is now broken since it has timestamps which are not comparable
    
    # create new object y
    y = LWWElementSet(set([(1,0), (2,2), (1,3)]), set([(1,1)]))
    
    # show elements added or removed up to time 1
    y.snapshot(1)
    
    # check whether y contains an element
    y.contains(1) # True
    y.snapshot(1).contains(1) # False
    
    # check that y contains 2
    y.contains(2)
    
    # remove element 2 from y at time 4
    y.removeElement(2, 4)
    
    # check that 2 is gone
    y.contains(2)
    
    # merge two LWWElementSet objects
    y.merge(x)
    """
    def __init__(self, addSet, removeSet):
        
        # type checking
        if not isinstance(addSet, set) or not isinstance(removeSet, set):
            raise TypeError
        
        self.addSet = addSet
        self.removeSet = removeSet
        
    def __eq__(self, other):
        """
        test for equality (needed for later unit tests)
        """
        return (self.addSet == other.addSet) and (self.removeSet == other.removeSet)
        
    def __repr__(self):
        """
        print the contents of the object, for debugging
        """
        return 'addSet:   ' + str(self.addSet) +'\nremoveSet:' + str(self.removeSet)
        
    def addElement(self, x, timestamp):
        """
        add element x at timestamp
        """
        self.addSet.add((x, timestamp))
        
    def snapshot(self, timestamp):
        """
        return the elements which have been added and removed up to timestamp
        """
        snapshot = LWWElementSet(set([]), set([]))
        
        snapshot.addSet = set([a for a in self.addSet if a[1] <= timestamp])
        snapshot.removeSet = set([a for a in self.removeSet if a[1] <= timestamp])
        
        return snapshot
        
    def contains(self, x):
        """
        check whether the LWWElementSet contains an object x
        """
        if x not in [a[0] for a in self.addSet]:
            return False
        else:
            # x is in the addSet, check that it's not in the removeSet with
            # a higher timestamp
            add_ts = [a[1] for a in self.addSet if a[0] == x]
            max_add_ts = np.array(add_ts).max()
            rem_ts = [a[1] for a in self.removeSet if a[0] == x]
            if len(rem_ts) == 0:
                return True
            else:
                max_rem_ts = np.array(rem_ts).max()
                if max_rem_ts > max_add_ts:
                    # should this condition be > or >= ?
                    # according to the spec, it should be >
                    # note that according to this spec, if the same element is
                    # simultaneously added and removed, it counts as *added*
                    return False
                else:
                    return True
            
    def removeElement(self, x, timestamp):
        """
        remove element x at timestamp
        """
        # here we need to check that x is in the set
        # no, we don't actually. You are not supposed to check this
        #snapshot = self.snapshot(timestamp)
        #if not snapshot.contains(x):
        #    print("Error: object not in set.")
        #    return
        
        # because it doesn't matter if something was in the set with an earlier
        # timestamp, you can still remove it
        
        # but I'm not sure whether this is the intended behaviour, because it means you could delete things from someone else's set, which would then disappear when their set is merged with yours
        self.removeSet.add((x, timestamp))
        
    def merge(self, other):
        """
        merge two LWWElementSet objects by taking the union of addSets and
        removeSets
        """
        merged = LWWElementSet(set([]), set([]))
        merged.addSet = other.addSet.union(self.addSet)
        merged.removeSet = other.removeSet.union(self.removeSet)
        return merged
    
    # tests?