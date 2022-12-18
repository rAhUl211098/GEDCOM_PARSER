import unittest
from User_stories import *


class Sprint1_Test(unittest.TestCase):


    def test_us1_birth_less_than_6( self ):
        obj = GedcomParser(r'./data/test_data.ged', pt=False)
        families = us1_birth_less_than_6(obj,debug=True)
        self.assertTrue('@F6@',families)
        self.assertIn('@F6@', families)
        self.assertEqual(len(families), 1)

    def test_us2_less_than_15_siblings(self):
        obj = GedcomParser(r'./data/test_data.ged', pt=False)
        families = us2_less_than_15_siblings(obj,debug=True)
        self.assertIn('@F6@', families)
        self.assertEqual(len(families), 1)

    def test_us3_orphans_list(self):
        obj = GedcomParser(r'./data/test_data.ged', pt=False)
        orphans = us3_orphans_list(obj,debug=True)
        self.assertTrue(len(orphans) == 1)
        self.assertFalse(len(orphans) == 0)

    def test_us4_next_dob( self ):
        obj = GedcomParser(r'./data/test_data.ged', pt=False)
        debug_list = us4_next_dob(obj,pt=False, debug=True)
        for time_delta in debug_list:
            self.assertTrue(time_delta.days < 30)
        for time_delta in debug_list:
            self.assertFalse(time_delta.days >= 30)

if __name__ == '__main__':

    unittest.main(exit=False, verbosity=2)
