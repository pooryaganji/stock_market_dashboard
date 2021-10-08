"""

a simple dashboard to call stocktwits api and show the result in a dashboard
first tab shows informations on price changes (default TSLA) and second tab 
demonstrates sentiments of users about the stock quote

**************
by pooryaganji
**************
"""

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash
import plotly.offline
import plotly.express as px
import pandas as pd
import requests

# Initialise the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling two tabs in dashboard (price chart tab and sentiment tab)
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# defining app layout
app.layout = dbc.Container(        
    dcc.Tabs(
        [dcc.Tab([html.P(),
        dcc.Graph(
            id='my_graph'
        )
        ,

        dcc.Graph(
            id='histogram'
        )
                ],label='Price chart', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(children=[html.Div(id='table')],label='sentiment of Stocktwits.com', value='tab-2', style=tab_style, selected_style=tab_selected_style)
        ]
        ))

if __name__ == '__main__':
    app.run_server(debug=True)