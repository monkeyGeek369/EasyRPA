import unittest
from database.site_manager import *

class TestDbTmpDataOperation(unittest.TestCase):
    def test_create_site(self):
        id = add_site("name","des")
        print(id)
