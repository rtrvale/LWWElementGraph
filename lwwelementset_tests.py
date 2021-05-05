# -*- coding: utf-8 -*-


import unittest
from lwwelementset import LWWElementSet

class testLWWElementSet(unittest.TestCase):

    def test_addElement(self):
        # create instance of LWWElementSet
        u = LWWElementSet(set([]), set([]))
            
        # add element 1 at timestamp 0
        u.addElement(1, 0)
        self.assertEqual(u.contains(1), True)
    
    def test_snapshot(self):
        # create instance of LWWElementSet
        u = LWWElementSet(set([]), set([]))
        
        # add element 1 at timestamp 0
        u.addElement(1, 0)
        
        # add element 2 at timestamp 1
        u.addElement(2, 1)
        
        self.assertEqual(u.snapshot(0).contains(1), True)        
        self.assertEqual(u.snapshot(0).contains(2), False)
        
    def test_removeElement(self):
        # create instance of LWWElementSet
        u = LWWElementSet(set([]), set([]))
        
        # add element 1 at timestamp 0
        u.addElement(1, 0)
        
        # remove element 1 at timestamp 1
        u.removeElement(1, 1)        
        
        # check that element 1 was removed
        self.assertEqual(u.contains(1), False)
        
        # remove element 1 before it was first added
        u.removeElement(1, -1)
        
        # check that 1 exists at the time when it was added
        self.assertEqual(u.snapshot(0).contains(1), True)