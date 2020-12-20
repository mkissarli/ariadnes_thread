import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

from thread.logic import *
#comp = start_at_company("07798925")

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

app.layout = html.Div(
    #[
    #[html.H1("Company Graph")]
    [
        html.Label("Company Number: "),
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
    [Input(component_id ='input_cn', component_property ='value'),
    Input(component_id ='input_depth', component_property ='value')]
)

def update_value(input_cn, input_depth): 
    try:
        comp = start_at_company(input_cn, depth = int(input_depth))
        return cyto.Cytoscape(
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
            ])
    except:
        return "Error, the input is not valid"

app.run_server(debug=True)

