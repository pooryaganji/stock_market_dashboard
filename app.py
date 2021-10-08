"""

a simple dashboard to call stocktwits api and show the result in a dashboard
first tab shows informations on price changes (default TSLA) and second tab 
demonstrates sentiments of users about the stock quote

**************
by pooryaganji
**************
"""


# Initialise the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])