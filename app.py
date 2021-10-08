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
from dash.dependencies import Input, Output,State
import pandas_datareader
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
    #cardgroup to show average change in price,bearish candles and bullish candles
    dbc.CardGroup
        ([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Average Change", className="card-title",style={'textAlign': 'center'}),
                        html.P(id='average change'
                            ,
                            className="card-text",style={'textAlign': 'center'}
                        )
                    ]
                )
            ,color="primary", inverse=True
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Bullish Candles", className="card-title",style={'textAlign': 'center'}),
                        html.P(id='bullish'
                            ,
                            className="card-text",style={'textAlign': 'center'}
                        )
                    ]
                )
            ,color="success", inverse=True
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Bearish Candles", className="card-title",style={'textAlign': 'center'}),
                        html.P(id='bearish'
                            ,
                            className="card-text",style={'textAlign': 'center'}
                        )
                    ]
                )
            ,color="danger", inverse=True
            ),

        ]),
    #hidden div for storing dataframe as json to share between tabs 
    html.Div(id='hidden_div', style={'display': 'none'}),



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

#read from hidden div and calculate average price
@app.callback(Output('average change', 'children'),
    [Input('hidden_div', 'children')])
def average_card(json_df):
    df=pd.read_json(json_df, orient='split')
    avg_change=abs(df['change']).mean()
    return str(avg_change)[:4]+" $"
#read from hidden div and count bearish candles
@app.callback(Output('bearish', 'children'),
    [Input('hidden_div', 'children')])
def bearish_card(json_df):
    df=pd.read_json(json_df, orient='split')
    return (df['change']>0).value_counts()[0]
#read from hidden div and count bullish candles
@app.callback(Output('bullish', 'children'),
    [Input('hidden_div', 'children')])
def bullish_card(json_df):
    df=pd.read_json(json_df, orient='split')
    return (df['change']>0).value_counts()[1]

#get input and call stocktwits API
@app.callback(Output('hidden_div', 'children'),
    [Input('submit-button', 'n_clicks')],[State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),State('my_date_picker', 'end_date')])
def div(n_clicks,my_ticker_symbol,start_date,end_date):
    data=pandas_datareader.av.time_series.AVTimeSeriesReader(symbols=my_ticker_symbol, function='TIME_SERIES_DAILY', start=start_date, end=end_date, retry_count=3, pause=0.1, session=None, chunksize=25, api_key='EYGEIQ4DIRZYERUZ')
    df=data.read().reset_index()
    df['change']=df.close-df.open
    return df.to_json(date_format='iso', orient='split')

if __name__ == '__main__':
    app.run_server(debug=True)