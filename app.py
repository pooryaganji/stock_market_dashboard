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
from datetime import datetime
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

#header content
card_content = [
    dbc.CardHeader("By Poorya Ganji (pooryaganji1368@gmail.com)"),
    dbc.CardBody(
        [
            html.H5("Stock Ticker Dashboard", className="card-title"),
            html.P(
                #"This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]


# emty dataframe to store data receiving from stock twits api
df=pd.DataFrame(columns=['text',
'time',
'sentiment',
'user'])


# defining app layout
app.layout = dbc.Container(        

    [   
        #add herader
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="grey", inverse=True)),

            ],
            className="mb-4",
        ),

    html.Div([
        # add text box for stock symbol
        html.H3('Enter a stock symbol:', style={'paddingRight':'30px'}),
        dcc.Input(
            id='my_ticker_symbol',
            value='TSLA',
            style={'fontSize':24, 'width':100}
        )
    ], style={'display':'inline-block', 'verticalAlign':'top'}),
    # add a date picker
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed = datetime(2015, 1, 1),
            max_date_allowed = datetime.today(),
            start_date = datetime(2021, 1, 1),
            end_date = datetime.today()
        )
    ], style={'display':'inline-block', 'marginLeft':'340px'}),
    #add submit button to refresh input data
    html.Div([
        dbc.Button("Submit",id='submit-button', color="dark", className="mr-1",style={'fontSize':24, 'marginLeft':'30px'}),

    ], style={'display':'inline-block'}),
    html.P(),




    # tabs ui structure
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
        )])

if __name__ == '__main__':
    app.run_server(debug=True)