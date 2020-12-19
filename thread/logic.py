import requests
from requests.auth import HTTPBasicAuth

api_key = "yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt"
auth = HTTPBasicAuth("{key}".format(key = api_key), '')

# Note Company_no has to be str as it has leading 0s

def get_company_info(company_number: str):
    """
    Retrieves information about a company from Companies House.
    Args:
        company_no (str): Registered company number.
    Returns:
        Information Companies House holds on the company.
    """

    url = "https://api.companieshouse.gov.uk/company/{company_num}".format(company_num = company_number)
    response = requests.get(url, auth = auth)
    return response.json()

def get_company_officers(company_number: str):
    url = "https://api.companieshouse.gov.uk/company/{company_num}/officers".format(company_num = company_number)
    response = requests.get(url, auth = auth)
    return response.json()
    

def get_associated_companies_info_by_company(company_no: str, depth: int = 1):
    """
    Finds information about all companies associated through officers with the starting company.

    Args:
        company_no (str):  The company number we want to search associated companies with.
        depth (int): The depth of search in the graph of companies.

    Returns:
        A list of information about all associated companies up to the given depth.
    """
    company_info = get_company_info(company_no)
    return []

from collections import deque

def start_at_company(company_number: str, depth: int = 1):
    company_graph = Graph()
    count = 0
    q = deque([])
    q.append(company_number)
    while len(q) > 0 and depth > 0:
        number = q.popleft()
        response = get_company_info(number)
        c = Company(response)
        response = get_company_officers(number)
        for i in response["items"]:
            o = Officer(i)
            company_graph.add(c, o)

        depth = depth - 1

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
        self.active = True if json["status"] == "active" else False
        self.company_number = json["company_number"]
        self.company_name = json["company_name"]
        self.creation = json["date_of_creation"]

        ##url = "https://api.companieshouse.gov.uk/company{officers}".format(officers = json.links.officers)
        ##response = requests.get(url, auth = auth)


comp = start_at_company("07798925")

g = Graph()
g.add("Apple", "Steve Jobs")
g.add("Steve Jobs", "Pixar")
g.add("Apple", "Tom Cook")

print(g.graph_dict)

#print()
### TEST

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

def return_company_graph(graph):
    elements = []
    for key, value in graph.graph_dict.items():
        if type(key) is Company:
            elements.append({"data":
                             {
                                 "id": key.company_name,
                                 "label": key.company_name
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

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=return_company_graph(comp),
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '480px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)'
                }
            },
            {
                'selector': '.officer',
                'style': {
                    'background-color': 'red',
                }
            },
            {
                'selector': '.company',
                'style': {
                    'background-color': 'blue',
                }
            }
        ]
    )
])

app.run_server(debug=True)

