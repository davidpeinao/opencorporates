import unittest
import main

class Test_TestMain(unittest.TestCase):
    def test_build_url(self):
        self.assertEqual(main.build_url("smartt","1234abc","0.4"), 
        "https://api.opencorporates.com/0.4/companies" \
        "/search?q=smartt&fields=name" \
        "&api_token=1234abc&per_page=100")
    
    def test_build_url_empty(self):
        self.assertEqual(main.build_url("","",""), 
        "https://api.opencorporates.com//companies" \
        "/search?q=&fields=name" \
        "&api_token=&per_page=100")


if __name__ == '__main__':
    unittest.main()