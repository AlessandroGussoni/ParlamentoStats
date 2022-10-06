import json

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from components.generic import download_button_builder, tabs_builder
from components.helpers import update_dict_params
from config import config


def cast_string(x):
    x = str(int(x))
    if len(x) == 1:
        return '00' + x
    elif len(x) == 2:
        return '0' + x
    return x


with open('data/elettori/geojson.json') as file:
    geojson = json.load(file)

grouped = pd.read_csv('data/elettori/Elettori_provincia.csv')
grouped.prov_istat_code = grouped.prov_istat_code.apply(cast_string)
grouped.Affluenza = grouped.Affluenza.apply(lambda x: round(x * 100, 2))

reg_stats = pd.read_csv('data/elettori/Elettori_regione.csv')
reg_stats.Affluenza = reg_stats.Affluenza.apply(lambda x: round(x * 100, 2))

naz_stats = pd.read_csv('data/elettori/Elettori_nazionale.csv')
naz_stats['Affluenza'] = naz_stats.Votanti - naz_stats.Elettori
naz_stats.Affluenza = naz_stats.Affluenza.apply(lambda x: round(x * 100, 2))

fig = px.choropleth_mapbox(grouped,
                           geojson=geojson,
                           color="Affluenza",
                           locations="prov_istat_code",
                           featureidkey="properties.prov_istat_code",
                           center={"lat": 41.5357, "lon": 12.3242},
                           mapbox_style="carto-positron",
                           animation_frame='anno',
                           range_color=(min(grouped['Affluenza']), max(grouped['Affluenza'])),
                           zoom=3.5)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  title='Affluenza Per regione')

affluenza_component = [dbc.Row([dbc.Col(children=dcc.Loading([html.H2(config['aff']['h2_title']),
                                                              html.Br(),
                                                              dcc.Graph(figure=fig),
                                                              html.Br()]),
                                        width=config['page_template']['Chart width']),
                                tabs_builder(data_dict=config['aff']['tabs'])]),
                       html.Br(),
                       html.Br(),
                       dcc.Dropdown(id='aff_dd_id',
                                    value='Nazionale',
                                    options=[{'label': regione,
                                              'value': regione} for regione in
                                             list(reg_stats.Regione.unique()) + ['Nazionale']],
                                    style=config['page_template']['dd_style']),
                       dcc.Graph(id='aff_chart_id')] + download_button_builder(name=config['aff']['button_name'],
                                                                               ids=config['aff']['download_id'])

def return_aff_callback():
    @dash.callback(Output('aff_chart_id', 'figure'),
                   Input('aff_dd_id', 'value'))
    def plot_eta_gruppo_stat(stat):
        if stat == 'Nazionale':
            data = naz_stats.copy()
        else:
            data = reg_stats.loc[reg_stats.Regione == stat]

        fig = px.line(data,
                      x='Anno',
                      y='Affluenza',
                      markers=True)
        font_dict = update_dict_params(config['page_template']['title'],
                                       title='Affluenza ' + stat + config['page_template']['title']['text'])
        fig.update_layout(title=font_dict)
        fig.update_traces(marker=dict(size=config['page_template']['chart']['m']))
        return fig

    return plot_eta_gruppo_stat


def download_callback_registry(page):
    @dash.callback(Output(config[page]['download_id'][1], "data"),
                   Input(config[page]['download_id'][0], "n_clicks"),
                   Input(config[page]['dd_id'], 'value'),
                   prevent_initial_call=True)
    def generate_excel(n_nlicks, stat):
        if n_nlicks is None:
            return
        elif n_nlicks > 0:
            print(1)
            def to_xlsx(bytes_io):
                data = reg_stats.loc[reg_stats.Regione == stat]
                xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")  # requires the xlsxwriter package
                data.to_excel(xslx_writer, index=False, sheet_name="foglio")
                xslx_writer.save()

            return dcc.send_bytes(to_xlsx, 'senato_' + stat + ".xlsx")

    return generate_excel
