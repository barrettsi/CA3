import unittest
from commits import get_num_changes, split_details, get_date_time_info

class TestCommits(unittest.TestCase):

    def setUp(self):
        # Setting up list as commits to test get_num_changes
        self.test_commit_info = [ 'a / test path', 'a test', 'd', 'd /path/', 'm ', 'm /path', 'd /another/path']
        # Create a test details list to test split_details function
        self.test_details = [' r1537319  ', ' vnai0001 ', '  2015-10-27 13:15:19 +0000 (Tue, 27 Oct 2015) ', '  2 lines ']
        # Setting up a list of date and time information to test get_date_time_info
        self.date_time_info = '2015-11-12 10:32:06 +0000 (Thu, 12 Nov 2015)'.strip().split(' ')
        
    # Test the get_num_changes function which takes as arguments a string representing the type of change and a list of changes information to search for the string
    # Tests there are 2 strings in the test list above which start with 'd /' for delete
    # Tests there is 1 string in the test list which starts with 'a / ' for addition
    # Tests that the function raises a type error when give the incorrect number of arguments
    def test_get_num_changes(self):
        self.assertEqual(2, get_num_changes('d /', self.test_commit_info))
        self.assertEqual(1, get_num_changes('a /', self.test_commit_info))
        self.assertRaises(TypeError, get_num_changes, self.test_commit_info)
        
    # Test the split_details function which takes a list of details data as an argument and returns the revision, author, list of date/time info and number of comment lines 
    # Call the function with the test_details list above to ensure it gives the expected output 
    # Function raises a TypeError if given too many inputs 
    def test_split_details(self):
        self.assertEqual(('r1537319', 'vnai0001', ['2015-10-27', '13:15:19', '+0000', '(Tue,', '27', 'Oct', '2015)'], 2 ), split_details(self.test_details))
        self.assertRaises(TypeError, split_details, ['r1537320'], [' r1537319  ', ' vnai0001 ', '  2015-10-27 13:15:19 +0000 (Tue, 27 Oct 2015) ', '  2 lines '])
    
    # Test the get_date_time_info which takes a string of date and time info as an argument and returns the date, month, hour and day
    # Calling the function with the self.date_time_info list above gives the expected output
    # Calling the function with a list where items are not in the expected format gives a ValueError
    def test_get_date_time_info(self):
       self.assertEqual(('2015-11-12', 11, 10, 'Thu'), get_date_time_info(self.date_time_info))
       self.assertRaises(ValueError, get_date_time_info, ['2015-11-12', 'Mon'] )
        
        
if __name__ == '__main__':
    unittest.main()        
    
  