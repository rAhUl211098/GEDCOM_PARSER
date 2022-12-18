import unittest
from User_stories import *



def us3_orphans_list_test(self):
    obj = GedcomParser(r'./data/test_data.ged', pt=False)
    orphans = obj.us3_orphans_list(debug=True)
    self.assertTrue(len(orphans) == 1)
    self.assertFalse(len(orphans) == 0)

def us4_next_dob_test( self ):
    obj = GedcomParser(r'./data/test_data.ged', pt=False)
    debug_list = obj.us4_next_dob(pt=False, debug=True)
    for time_delta in debug_list:
        self.assertTrue(time_delta.days < 30)

unittest.main(exit=False, verbosity=2)