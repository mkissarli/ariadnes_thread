import requests
from requests.auth import HTTPBasicAuth
from collections import deque

class API:
    api_key = "yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt"
    base = "https://api.companieshouse.gov.uk"
    auth = HTTPBasicAuth("{key}".format(key = api_key), '')

    def get_company_info(company_number: str):
        """
        Retrieves information about a company from Companies House.
        Args:
        company_number (str): Registered company number.
        Returns:
        Information Companies House holds on the company.
        """
        
        url = "{base}/company/{company_num}".format(base = API.base, company_num = company_number)
        response = requests.get(url, auth = API.auth)
        return response.json()
    
    def get_company_officers(company_number: str):
        """
        Retrieves information about officers from Companies House.
        Args:
        company_number (str): Registered company number.
        Returns:
        Information Companies House holds on the company's officers.
        """
        
        url = "{base}/company/{company_num}/officers".format(base = API.base, company_num = company_number)
        response = requests.get(url, auth = API.auth)
        return response.json()
    
    def get_general(link: str):
        """
        Retrieves information from a link on Companies House.
        Args:
        link (str): Api link.
        Returns:
        Information from Companies House
        """
        url = "{base}{link}".format(base = API.base, link = link)
        response = requests.get(url, auth = API.auth)
        return response.json()

def start_at_company(company_number: str, depth: int = 1):
    """
    Breadth first search with max depth for creating a graph of companies and
    officers.
    Args:
    company_number (str): Registered company number to start at.
    Returns:
    Graph of companies and officers.
    """
    company_graph = Graph()
    c = Company(API.get_company_info(company_number))
    company_queue = [c]
    officer_queue = []

    for i in range(depth + 1):
        print(i)
        if i % 2 == 0:
            print("Is company level")
            while company_queue:
                node = company_queue.pop(0)
                response = API.get_company_officers(node.company_number)
                for i in response["items"]:
                    o = Officer(i)
                    company_graph.add(node, o)
                    officer_queue.append(o)
        else:
            while officer_queue:
                node = officer_queue.pop(0)
                response = API.get_general(node.appointments_link)
                for appointments in response["items"]:
                    num = appointments["appointed_to"]["company_number"]
                    c = Company(API.get_company_info(num))
                    company_graph.add(c, node)
                    company_queue.append(c)

    return company_graph
            
        

class Graph:
    def __init__(self):
        # Dictionary of Sets
        self.graph_dict = {}

    def add(self, vertex, vertex2):

        ## Adds the vertex to each others edges after check if the dict has the
        ## key already, otherwise it creates a set there.
        if not vertex in self.graph_dict:
            self.graph_dict[vertex] = set()

        self.graph_dict[vertex].add(vertex2)

        if not vertex2 in self.graph_dict:
            self.graph_dict[vertex2] = set()
            
        self.graph_dict[vertex2].add(vertex)
    
class Officer:
    def __init__(self, json):
        self.officer_name = json["name"]
        self.appointments_link = json["links"]["officer"]["appointments"]

class Company:
    def __init__(self, json):
        self.has_insolvency_history = json["has_insolvency_history"]
        ## Inconsistant json..
        # self.active = True if json["status"] == "active" else False
        self.company_number = json["company_number"]
        self.company_name = json["company_name"]
        self.creation = json["date_of_creation"]
