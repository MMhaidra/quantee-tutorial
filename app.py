import flask # Flask server on which Dash app is build

import pandas as pd # Data-Frames

import dash # Dash app
from dash.dependencies import Input, Output # For Dash callbacks
import dash_core_components as dcc # Dash components
import dash_html_components as html # Dash html components

from utils_dash import dash_surface, dash_choropleth_map # Custom Utilities written for this tutorial

df = pd.read_csv('https://raw.githubusercontent.com/quanteeai/dash-yield-curves-demo/master/data/yc.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   
server = flask.Flask('app')
app = dash.Dash('app', server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    # Container for first row: header
    html.H1('Example Dash App'),
    
    # Container for second row: dropdowns
    html.Div([
        
        # Container for dropdown
        html.Div([
            dcc.Dropdown(
                id='main-dropdown',
                options=[
                    {'label': '2019-02-28', 'value': '2019-02-28'},
                    {'label': '2019-01-31', 'value': '2019-01-31'},
                    {'label': '2018-11-30', 'value': '2018-11-30'}
                ],
                value='2019-02-28'
            ), 
        ], className='six columns')
        
    ], className='row'),
    
    # Container for third row: Plotly charts
    html.Div([
        
        # Container for left chart (updated in callback)
        html.Div([
            dcc.Graph(id='left-graph')
        ], className='six columns'),
        
        # Container for right chart (updated straightaway)
        html.Div([
            dcc.Graph(id='right-graph', figure=dash_surface(df))
        ], className='six columns')
        
    ], className='row')
    
])
            
@app.callback(Output('left-graph', 'figure'),
              [Input('main-dropdown', 'value')])
def update_left_graph(selected_dropdown_value):
    dff = df[(df.date == selected_dropdown_value) & (df.term == 1)]
    return dash_choropleth_map(dff)

if __name__ == '__main__':
    app.run_server()

