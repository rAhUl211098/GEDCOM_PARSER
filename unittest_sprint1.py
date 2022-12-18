import unittest
from User_stories import *

def us1_birth_less_than_6_test(self):
    obj = GedcomParser(r'./data/test_data.ged', pt=False)
    families = obj.us1_birth_less_than_6(debug=True)
    self.assertIn('@F6@', families)
    self.assertEqual(len(families), 1)

def us2_less_than_15_siblings_test(self):
    obj = GedcomParser(r'./data/test_data.ged', pt=False)
    families = obj.us2_less_than_15_siblings(debug=True)
    self.assertIn('@F6@', families)
    self.assertEqual(len(families), 1)

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
