import requests
from requests.auth import HTTPBasicAuth
import os

class API:
    # Should be in an .env really.
    api_key = os.getenv("api_key")
    base = "https://api.companieshouse.gov.uk"
    auth = HTTPBasicAuth("{key}".format(key = api_key), '')

    @staticmethod
    def status_check(status: int):
        """
        Raises an exception if we recieve a failing status.
        Args:
        status (int): Http status code.
        """
        ## I will not do all of these, for a take home it is excessive.
        if status == 404:
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

        API.status_check(response.status_code)
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

        API.status_check(response.status_code)
 
        return response.json()

    def get_officer_info(officer_number: str):
        """
        Retrieves information about officers from Companies House.
        Args:
        company_number (str): Registered officer number
        Returns:
        Information Companies House holds on the officers appointments
        """

        if type(officer_number) != str:
            raise TypeError("Officer Number must be a string: {num}".format(num = officer_number))
        
        url = "{base}/officers/{num}/appointments".format(base = API.base, num = officer_number)
        response = requests.get(url, auth = API.auth)

        API.status_check(response.status_code)

        output = response.json()
        output["name"] = output["items"][0]["name"]
        output["links"]["officer"] = {"appointments": output["links"]["self"]}

        return output        
    
    def get_general(link: str):
        """
        Retrieves information from a link on Companies House.
        Args:
        link (str): Api link.
        Returns:
        Information from Companies House
        """

        if type(link) != str:
            raise TypeError("Link must be a string: {num}".format(num = link))
        
        url = "{base}{link}".format(base = API.base, link = link)
        response = requests.get(url, auth = API.auth)

        API.status_check(response.status_code)

        return response.json()
    
class CompanyGraph:
    def start_search(number: str, depth: int = 1, is_company: bool = True):
        """
        Breadth first search with max depth for creating a graph of companies and
        officers. Can be started from either.
        Args:
        number (str): Registered company number to start at.
        depth (int): Number greater than 0 that represents how deep down the company graph to go.
        is_company (bool): True we start at a company, False we start at an officer.
        Returns:
        Graph of companies and officers.
        """
        
        if type(is_company) != bool:
            raise TypeError("is_company must be a bool: {b}".format(b = is_company))
        if type(number) != str:
            raise TypeError("Number must be a string: {num}".format(num = number))
        if type(depth) != int or depth < 0:
            raise TypeError("Depth must be a positive int: {d}".format(d = depth))
        
        company_graph = Graph()
        company_queue = []
        officer_queue = []
        
        is_company_rem = 1
        
        if is_company:
            c = Company(API.get_company_info(number))
            company_queue.append(c)
            is_company_rem = 0
        else:
            o = Officer(API.get_officer_info(number))
            officer_queue.append(o)
            
        for i in range(depth):
            if i % 2 == is_company_rem:
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
    
    def return_company_graph(graph):
        """
        Takes a Company Graph and returns a Dash Cytoscape compatible object to 
        render in Dash.
        Args:
        graph (Graph): Company Graph to render. Must specifically  be a graph
          consisting only of Company and Officer objects.
        Returns:
        Dash Cytoscape object for render.
        """
        elements = []
        for key, value in graph.graph_dict.items():
            if (type(key) != Company and type(key) != Officer) or (not all(isinstance(x, (Company, Officer)) for x in value)):
                raise TypeError("Graphs passed to return_company_graph must be company graphs consisting only of Company and Officer types.")
            if type(key) is Company:
                elements.append({"data":
                                 {
                                     "id": key.company_name,
                                     "label": "{comp}: {risk}".format(comp = key.company_name, risk = round(CompanyGraph.risk(key, graph), 2))
                                 },
                                 "classes": "company"})
                for elem in value:
                    elements.append({"data":
                                    {
                                        "source": key.company_name,
                                        "target": elem.officer_name
                                    }})
            else:
                elements.append({"data":
                                 {
                                     "id": key.officer_name,
                                     "label": key.officer_name
                                 },
                                 "classes": "officer"})
                for elem in value:
                    elements.append({"data":
                                     {
                                         "source": key.officer_name,
                                         "target": elem.company_name
                                     }})
                        
        return elements

    def risk(company, graph):
        """
        Calculates the risk of working with a company. There are a million
        different ways to do this. Some good ideas are:
          + Bayesian Inference, to update probability of a failing company.
          + Using a geometric sequence such that if the company is insolvant then
            the risk is 1, and after then
            sum((1/depth)^(depth - 1) * (total fails at depth)/(total companies at depth)) for each depth.

        We go with a variation on the second one where an insolvant company fails,
        and every company one officer away that is insolvent adds to the overall
        fail rate. 

        I would prefer to go with one of the above methods, but between time
        constraints, my inexperience in rating companies and that it can get
        quite expensive to run this for each company, I've decided for the take
        home this is a better option.

        Args:
        company (Company): Company to rate.
        graph (Graph): Graph of relations to company
        Returns:
        (int): Risk of associating with a company as a percentage. 0 means no risk
          at all, and 1 means certain failure.
        """
        if type(company) != Company:
            raise TypeError("company arg must be an instance class Company.")
        
        # Inefficent.
        for key, value in graph.graph_dict.items():
            if (type(key) != Company and type(key) != Officer) or (not all(isinstance(x, (Company, Officer)) for x in value)):
                raise TypeError("Graphs passed to risk must be company graphs consisting only of Company and Officer types.")
        if company.has_insolvency_history:
            return 1

        company_connections = []

        for officer in graph.graph_dict[company]:
            for c in graph.graph_dict[officer]:
                if (not c in company_connections) and (c != company):
                    company_connections.append(c)
        
        if len(company_connections) == 0:
            ## If the company  has no connections we cant really predict anything.
            return 0.5
        
        value = 0
        for c in company_connections:
            if c.has_insolvency_history:
                value = value + 1

        value = value / len(company_connections)
        return value

    
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
