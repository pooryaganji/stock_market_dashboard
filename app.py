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
import plotly.graph_objects as go

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
            id='candle_stick'
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

# histogram showing scale of daily price change and count them 
@app.callback(Output('histogram', 'figure'),
    [Input('hidden_div', 'children')])
def hist(json_df):
    df=pd.read_json(json_df, orient='split')
    fig=px.histogram(df, x="change")
    return fig.update_layout(title=dict(text='Count of change in price intervals',x=0.5),xaxis_title="price change ($)")

# candle Stick chart showing price in daily timeframe
@app.callback(Output('candle_stick', 'figure'),
    [Input('hidden_div', 'children')])
def func(json_df):
    df=pd.read_json(json_df, orient='split')
    return {'data':[go.Candlestick(x=df['index'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])],
                'layout': go.Layout(annotations=[],title='Candle stick chart in selected time period',yaxis_title="price ($)",
                xaxis_rangeslider_visible=False
        )}

# recieve twits and sentiments from stocktwits API
@app.callback(Output('table', 'children'),
    [Input('submit-button', 'n_clicks')],[State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),State('my_date_picker', 'end_date')])
def tableview(n_clicks,my_ticker_symbol,start_date,end_date):
    url = "https://api.stocktwits.com/api/2/streams/symbol/{}.json".format(my_ticker_symbol)

    querystring = {"filter":"all","limit":"30"}

    headers = {
        'accept': "application/json",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
        'authorization': "OAuth 17aad3e23d0878034ec414256347d1155e85bbb1",
        'Cache-Control': "no-cache",
        'origin': "https://stocktwits.com",
        'pragma': "no-cache",
        'referer': "https://stocktwits.com/",
        'sec-ch-ua': "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        'Postman-Token': "f15340d0-344d-deca-24c3-cd6db65ee147"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    text=[]
    time=[]
    sentiment=[]
    user=[]

    for msg in response.json()['messages']:
        text.append(msg['body'])
        time.append(msg['created_at'])
        try:
            sentiment.append(msg['entities']['sentiment']['basic'])
        except:
            sentiment.append(None)
        user.append(msg['user']['name'])

        d=dict(
        text=text,
        time=time,
        sentiment=sentiment,
        user=user)
    df=pd.DataFrame(d)
    return dbc.Table.from_dataframe(df=df,striped=True, bordered=True, hover=True)

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