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
        company_no (str): Registered company number.
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
        company_no (str): Registered company number.
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
        company_no (str): Registered company number.
        Returns:
        Information from Companies House
        """
        url = "{base}{link}".format(base = API.base, link = link)
        response = requests.get(url, auth = API.auth)
        return response.json()

def start_at_company(company_number: str, depth: int = 1):
    company_graph = Graph()
    officer_count = 0
    q = deque(set())
    q.append({company_number})
    depth = depth + 1
    while len(q) > 0 and depth > 0:
        number_list = q.popleft()
        new_number_list = set()
        for number in number_list:
            # If the value already exists in the graph then skip the rest of the loop.
            #if len({k: v for k, v in company_graph.graph_dict.items()
            #        if type(v) == Company and v.company_number == number}):
            #    continue
            
            response = API.get_company_info(number)
            c = Company(response)
            depth = depth - 1
            
            response = API.get_company_officers(number)
            if depth > 0:
                depth = depth - 1
                for i in response["items"]:
                    o = Officer(i)
                    company_graph.add(c, o)
                    if depth > 0:
                        cur_response = API.get_general(i["links"]["officer"]["appointments"])
                        for appointments in cur_response["items"]:
                            new_num = appointments["appointed_to"]["company_number"]
                            new_c = Company(API.get_company_info(new_num))
                            company_graph.add(new_c, o)
                            ## @TODO: Multiple calls to the ssame data
                            new_number_list.add(new_num)

        q.append(new_number_list)

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

class Company:
    def __init__(self, json):
        self.has_insolvency_history = json["has_insolvency_history"]
        ## Inconsistant json..
        # self.active = True if json["status"] == "active" else False
        self.company_number = json["company_number"]
        self.company_name = json["company_name"]
        self.creation = json["date_of_creation"]

