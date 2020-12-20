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
        assert o.officer_name, "Matt"
        assert o.appointments_link, "some_link"

    def test_init_incorrect(self):
        json = {}
        with self.assertRaises(Exception) as e:
            Officer(json)
        assert e, "Officer json is missing attributes."

        json = {"name": "Matt"}
        with self.assertRaises(Exception) as e:
            Officer(json)
        assert e, "Officer json is missing attributes."

        json = {
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        with self.assertRaises(Exception) as e:
            Officer(json)
        assert e, "Officer json is missing attributes."

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
        assert e, "Company json is missing attributes."

        json = {
            "company_name": "Bond Industries",
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        assert e, "Company json is missing attributes."

        json = {
            "company_number": "007",
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        assert e, "Company json is missing attributes."

        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            "has_insolvency_history": False
        }

        with self.assertRaises(Exception) as e:
            Company(json)
        assert e, "Company json is missing attributes."
        
        
if __name__ == '__main__':
    unittest.main()
