import unittest
import app

class Testapp(unittest.TestCase):
    # Test that the password manager works
    def test_validator(self):
        self.assertEqual(app.validator("53564653KJNVRR"),False)
        self.assertNotEqual(app.validator("{1:[]}"),True)
        self.assertEqual(app.validator("{}"),True)
        test3={"1": {'title': 'Entry 1', 'body': 'This is the description for the first entry', 'category': 'TODO'}}
        self.assertEqual(app.validator(str(test3)), True)
    def test_jsonProcessor(self):
        test3={'title': 'Entry 1', 'body': 'This is the description for the first entry', 'category': 'TODO'}
        self.assertEqual(app.jsonProcessor(str(test3)),('Entry 1','This is the description for the first entry', 'TODO'))

if __name__=="__main__":
    unittest.main()