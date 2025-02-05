import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

from thread.logic import *

## Load .env file for api-key
import os
from dotenv import load_dotenv
load_dotenv()

app = dash.Dash(__name__)

app.layout = html.Div(
    #[
    [
        html.H1("Company Graph"),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Company Number', 'value': "company"},
                {'label': 'Officer Number', 'value': "officer"},
            ],
            value='company'
        ),
        #html.Label("Company Number: "),
        dcc.Input(
            id = "input_cn",
            placeholder='Enter company number',
            type='text',
            value=''
        ),
        html.Label("Depth: "),
        dcc.Input(
            id = "input_depth",
            placeholder='Enter company number',
            type='number',
            value='1'
        ),
        html.Div(id = "output")
    ]
)

@app.callback( 
    Output(component_id ='output', component_property ='children'), 
    [Input(component_id = "dropdown", component_property = "value"),
     Input(component_id ='input_cn', component_property ='value'),
     Input(component_id ='input_depth', component_property ='value')]
)

def update_value(dropdown, input_cn, input_depth): 
    try:
        is_company = True if dropdown == "company" else False
        comp = CompanyGraph.start_search(input_cn, depth = int(input_depth), is_company = is_company)
        return cyto.Cytoscape(
            id='cytoscape',
            elements=CompanyGraph.return_company_graph(comp),
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
            ])
    except:
        return "Error, the input is not valid"

app.run_server(debug=True)

