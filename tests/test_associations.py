from unittest import TestCase

from src.thread.logic import *

class APITestCase(TestCase):
    def test_get_company_info(self):
        pass

    def test_get_company_officers(self):
        pass

    def get_general(self):
        pass

class BreadthTestCase(TestCase):
    def test_start_at_company(self):
        pass

class GraphTestCase(TestCase):
    def test_init(self):
        pass
    
    def test_add(self):
        pass

class OfficerTestCase(TestCase):
    def test_init_correct(self):
        json = {
            "name": "Matt",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o = Officer(json)
        assert(o.officer_name, "Matt")
        assert(o.appointments_link, "some_link")

class CompanyTestCase(TestCase):
    def test_init(self):
        pass


if __name__ == '__main__':
    unittest.main()
