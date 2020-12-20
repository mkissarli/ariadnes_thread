import requests
from requests.auth import HTTPBasicAuth
from collections import deque

class API:
    # Should be in an .env really.
    api_key = "yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt"
    base = "https://api.companieshouse.gov.uk"
    auth = HTTPBasicAuth("{key}".format(key = api_key), '')

    def status_check(status):
        ## I will not do all of these, for a take home it is excessive.
        if staus == 404:
            raise Exception("404 error, not authorised. Check your api key?")
        if status == 429:
            raise Exception("429 error, too many requests. You've likely gone past your rate limit.")
    
    def get_company_info(company_number: str):
        """
        Retrieves information about a company from Companies House.
        Args:
        company_number (str): Registered company number.
        Returns:
        Information Companies House holds on the company.
        """

        if type(company_number) != str:
            raise TypeError("Company Number must be a string: {num}".format(num = company_number)) 

        url = "{base}/company/{company_num}".format(base = API.base, company_num = company_number)
        response = requests.get(url, auth = API.auth)

        self.status_check(response.status)
        
        return response.json()
    
    def get_company_officers(company_number: str):
        """
        Retrieves information about officers from Companies House.
        Args:
        company_number (str): Registered company number.
        Returns:
        Information Companies House holds on the company's officers.
        """

        if type(company_number) != str:
            raise TypeError("Company Number must be a string: {num}".format(num = company_number))
        
        url = "{base}/company/{company_num}/officers".format(base = API.base, company_num = company_number)
        response = requests.get(url, auth = API.auth)

        self.status_check(response.status)
        
        return response.json()
    
    def get_general(link: str):
        """
        Retrieves information from a link on Companies House.
        Args:
        link (str): Api link.
        Returns:
        Information from Companies House
        """

        if type(company_number) != str:
            raise TypeError("Company Number must be a string: {num}".format(num = company_number))
        
        url = "{base}{link}".format(base = API.base, link = link)
        response = requests.get(url, auth = API.auth)

        self.status_check(response.status)
        
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
    
    if type(company_number) != str:
        raise TypeError("Company Number must be a string: {num}".format(num = company_number))

    if type(depth) != int or depth < 0:
        raise TypeError("Depth must be a positive int: {d}".format(d = depth))

    company_graph = Graph()
    c = Company(API.get_company_info(company_number))
    company_queue = [c]
    officer_queue = []
        
    for i in range(depth):
        if i % 2 == 0:
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
    """
    Class representing a bi-directional graph, implamented with an adjacency
    matrix.
    
    Attributes:
    graph_dict: Adjacency Matrix, represented as a dictionary. Shows connections
      between nodes.
    """
    def __init__(self):
        # Dictionary of Sets
        self.graph_dict = {}

    def add(self, vertex, vertex2):
        """
        Connects vertex to vertex2 and vice-versa in graph_dict.
        Args:
        vertex: Any type
        vertex2: Any type
        """
        if not vertex in self.graph_dict:
            self.graph_dict[vertex] = set()

        self.graph_dict[vertex].add(vertex2)

        if not vertex2 in self.graph_dict:
            self.graph_dict[vertex2] = set()
            
        self.graph_dict[vertex2].add(vertex)
    
class Officer:
    """
    Represents an Officer of a company.
    Args:
    json (obj): The json object from the Officer resource at Companies Houses.
    Attributes:
    officer_name (str)
    appointments_link (str): Link provided in json to see related appointments.
    """
    def __init__(self, json):
        try:
            self.officer_name = str(json["name"])
            self.appointments_link = str(json["links"]["officer"]["appointments"])
        except:
            raise Exception("Officer json is missing attributes.")

class Company:
    """
    Represents a Company.
    Args:
    json (obj): The json object from the Company resource at Companies Houses.
    Attributes:
    company_name (str)
    company_number (str): Stored as a string as it may have leading 0s.
    creation (str): Date of creation
    has_insolvency_history (bool)
    """
    def __init__(self, json):
        try:
            self.has_insolvency_history = json["has_insolvency_history"]
            ## Inconsistant json..
            # self.active = True if json["status"] == "active" else False
            self.company_number = str(json["company_number"])
            self.company_name = str(json["company_name"])
            self.creation = str(json["date_of_creation"])
        except:
            raise Exception("Company json is missing attributes.")
