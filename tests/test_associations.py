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

class CompanyGraphTestCase(TestCase):
    def test_search_type_error(self):
        with self.assertRaises(TypeError) as e:
            CompanyGraph.start_search(11)
        self.assertEqual(str(e.exception),  "Number must be a string: 11")

        with self.assertRaises(TypeError) as e:
            CompanyGraph.start_search("11", depth = "p")
        self.assertEqual(str(e.exception),  "Depth must be a positive int: p")

        with self.assertRaises(TypeError) as e:
            CompanyGraph.start_search("11", depth = 1, is_company = 11)
        self.assertEqual(str(e.exception),  "is_company must be a bool: 11")
    # This is a huge pain to test, and makes much more sense testing it in
    # context that is as an integration/system test, which I have done and it
    # works.
    #def test_start_search_at_company(self):
    #    pass
    #def test_start_search_at_officer(self):
    #    pass

    def test_return_company_graph_not_company_graph(self):
        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }
        c = Company(json)
        json = {
            "name": "Matt",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o = Officer(json)

        g = Graph()
        g.add("1", "2")
        
        with self.assertRaises(TypeError) as e:
            CompanyGraph.return_company_graph(g)
        self.assertEqual(str(e.exception), "Graphs passed to return_company_graph must be company graphs consisting only of Company and Officer types.")

        g = Graph()
        g.add("1", c)
        
        with self.assertRaises(TypeError) as e:
            CompanyGraph.return_company_graph(g)
        self.assertEqual(str(e.exception), "Graphs passed to return_company_graph must be company graphs consisting only of Company and Officer types.")

        g = Graph()
        g.add("1", o)
        
        with self.assertRaises(TypeError) as e:
            CompanyGraph.return_company_graph(g)
        self.assertEqual(str(e.exception), "Graphs passed to return_company_graph must be company graphs consisting only of Company and Officer types.")

        g = Graph()
        g.add("1", c)
        g.add(c, o)

        with self.assertRaises(TypeError) as e:
            CompanyGraph.return_company_graph(g)
        self.assertEqual(str(e.exception), "Graphs passed to return_company_graph must be company graphs consisting only of Company and Officer types.")

    def test_return_company_graph_correct(self):
        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": True
        }
        c = Company(json)
        json = {
            "name": "Matt",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o = Officer(json)

        json = {
            "company_number": "0070",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }
        c2 = Company(json)
        json = {
            "name": "Matty",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o2 = Officer(json)

        graph = Graph()
        graph.add(c, o)
        graph.add(c, o2)

        assert CompanyGraph.return_company_graph(graph), [
            {
                'data': {
                    'id': 'Bond Industries', 'label': 'Bond Industries: 1'
                },
                'classes': 'company'},
            {
                'data': {
                    'source': 'Bond Industries', 'target': 'Matt'
                }},
            {
                'data': {
                    'source': 'Bond Industries', 'target': 'Matty'
                }},
            {
                'data': {
                    'id': 'Matt', 'label': 'Matt'},
                'classes': 'officer'},
            {
                'data': {
                    'source': 'Matt', 'target': 'Bond Industries'
                }},
            {
                'data': {
                    'id': 'Matty', 'label': 'Matty'},
                'classes': 'officer'},
            {
                'data': {
                    'source': 'Matty', 'target': 'Bond Industries'}}]
        
    def test_risk_incorrect(self):
        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": True
        }
        c = Company(json)
        json = {
            "name": "Matt",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o = Officer(json)

        json = {
            "company_number": "0070",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }
        c2 = Company(json)
        json = {
            "name": "Matty",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o2 = Officer(json)

        graph = Graph()
        graph.add(c, o)
        graph.add(c, o2)

        with self.assertRaises(TypeError) as e:
            CompanyGraph.risk("2", graph)
        self.assertEqual(str(e.exception), "company arg must be an instance class Company.")

        graph.add(c, "1")
        with self.assertRaises(TypeError) as e:
            CompanyGraph.risk(c, graph)
        self.assertEqual(str(e.exception), "Graphs passed to risk must be company graphs consisting only of Company and Officer types.")

    def test_risk_correct(self):
        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": True
        }
        c = Company(json)
        json = {
            "name": "Matt",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o = Officer(json)

        json = {
            "company_number": "0070",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": False
        }
        c2 = Company(json)
        json = {
            "name": "Matty",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o2 = Officer(json)

        graph = Graph()
        graph.add(c, o)
        graph.add(c, o2)

        assert CompanyGraph.risk(c, graph), 1

        graph = Graph()
        graph.add(c2, o)

        assert CompanyGraph.risk(c2, graph), 0.5

        graph.add(c, o)
        graph.add(c2, o2)

        assert CompanyGraph.risk(c, graph), 1.5
        assert CompanyGraph.risk(c2, graph), 0.5

        json = {
            "company_number": "007",
            "company_name": "Bond Industries",
            # Could add a date test.
            "date_of_creation": "07/07/2007",
            "has_insolvency_history": True
        }
        c = Company(json)
        json = {
            "name": "Matt",
            "links": {
                "officer": {
                    "appointments": "some_link"
                }
            }
        }
        o = Officer(json)
        graph = Graph()
        graph.add(c, o)


        
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
