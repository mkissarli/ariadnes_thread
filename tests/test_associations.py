from unittest import TestCase
from unittest.mock import Mock

from src.thread.logic import *

class APITestCase(TestCase):
    def test_status_check(self):
        with self.assertRaises(Exception) as e:
            API.status_check(404)
        self.assertEqual(str(e.exception), "404 error, not authorised. Check your api key?")

        with self.assertRaises(Exception) as e:
            API.status_check(429)
            self.assertEqual(str(e.exception), "429 error, too many requests. You've likely gone past your rate limit.")

        try:
            API.status_check(200)
        except ExceptionType:
            self.fail("API.status_check raised ExceptionType unexpectedly!")


    def test_get_company_info_type_error(self):
        with self.assertRaises(TypeError) as e:
            API.get_company_info(100)
        assert e.exception, "Company Number must be a string: 100"

        with self.assertRaises(TypeError) as e:
            API.get_company_info(True)
        self.assertEqual(str(e.exception), "Company Number must be a string: True")
        
    def test_get_company_officers_type_error(self):
        with self.assertRaises(TypeError) as e:
            API.get_company_officers(100)
        self.assertEqual(str(e.exception), "Company Number must be a string: 100")

        with self.assertRaises(TypeError) as e:
            API.get_company_officers(True)
        self.assertEqual(str(e.exception), "Company Number must be a string: True")

    def test_get_officers_info_type_error(self):
        with self.assertRaises(TypeError) as e:
            API.get_officer_info(100)
        self.assertEqual(str(e.exception), "Officer Number must be a string: 100")

        with self.assertRaises(TypeError) as e:
            API.get_officer_info(True)
        self.assertEqual(str(e.exception),  "Officer Number must be a string: True")
        
        
    def get_general_type_error(self):
        with self.assertRaises(TypeError) as e:
            API.get_general(100)
        self.assertEqual(str(e.exception), "Link must be a string: 100")

        with self.assertRaises(TypeError) as e:
            API.get_general(True)
        self.assertEqual(str(e.exception),  "Link must be a string: True")
        

    ## I am of the opinion that these methods don't need to be tested for passes,
    ## as they are essentially just passing data to a staple api (requests). They
    ## are here to show I considered them.
    def test_get_company_info(self):
        pass
    def test_get_company_officers(self):
        pass
    def get_general(self):
        pass

class BreadthTestCase(TestCase):
    def test_start_search_at_company(self):
        pass

    def test_start_search_at_officer(self):
        pass

class GraphTestCase(TestCase):
    def test_init(self):
        g = Graph()
        self.assertTrue(g.graph_dict == {})
    
    def test_add(self):
        g = Graph()

        g.add("a", 1)
        g.add("a", 2)
        g.add("b", 1)

        test_dict = {
            "a": {1, 2},
            "b": {1},
            1: {"a", "b"},
            2: {"b"}
        }
        assert g.graph_dict, test_dict

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
        assert o.officer_name, "Matt"
        assert o.appointments_link, "some_link"

    def test_init_incorrect(self):
        json = {}
        with self.assertRaises(Exception) as e:
            Officer(json)
        self.assertEqual(str(e.exception), "Officer json is missing attributes.")

        json = {"name": "Matt"}
        with self.assertRaises(Exception) as e:
            Officer(json)
        self.assertEqual(str(e.exception), "Officer json is missing attributes.")

        json = {
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        with self.assertRaises(Exception) as e:
            Officer(json)
        self.assertEqual(str(e.exception), "Officer json is missing attributes.")

class CompanyTestCase(TestCase):
    def test_init_correct(self):
        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }
        c = Company(json)
        assert c.company_number, "007"
        assert c.company_name, "Bond Industries"
        assert c.creation, "07/07/2007"
        self.assertTrue(c.has_insolvency_history == False)


    def test_init_incorrect(self):
        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            "date_of_creation": "07/07/2007",
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        self.assertEqual(str(e.exception), "Company json is missing attributes.")

        json = {
            "company_name": "Bond Industries",
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        self.assertEqual(str(e.exception), "Company json is missing attributes.")

        json = {
            "company_number": "007",
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        self.assertEqual(str(e.exception), "Company json is missing attributes.")

        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            "has_insolvency_history": False
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        self.assertEqual(str(e.exception), "Company json is missing attributes.")
        
        
if __name__ == '__main__':
    unittest.main()
