import os

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

from index import matches

files = [file for file in os.listdir('data') if os.path.isfile(os.path.join('data', file))]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True, )

# TODO: riempire il testo delle pagine
# TODO: sistemare download button
# TODO: aggiungere home page


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 60,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)

sidebar = html.Div(
    [
        html.H2("Statistiche", className="display-4"),
        html.Hr(),
        html.P("Elenco delle statistiche disponibili", className="lead"),
        dbc.Nav([dbc.NavLink("Home", href="/", active="exact")] +
                [dbc.NavLink(file.split('.')[0], href="/" + file.split('.')[0], external_link=True, active='exact') for file in
                 files] + [dbc.NavLink("Affluenza", href="/Affluenza", active="exact")],

                vertical=True,
                pills=True,
                ),
    ],
    style=SIDEBAR_STYLE,
)

layout = html.Div([dcc.Location(id="url"),
                   sidebar,
                   content])


@dash.callback(Output("page-content", "children"),
               [Input("url", "pathname")])
def render_page_content(pathname):
    return matches.get(pathname, 'Non abbiamo ancora questa statistica')


app.layout = html.Div([dcc.Location(id="url"),
                       dbc.NavbarSimple(brand='ParlamentoStats',
                                        color="primary",
                                        dark=True),
                       sidebar,
                       content])

if __name__ == "__main__":
    app.run_server(port=8020)
