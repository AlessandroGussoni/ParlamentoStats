import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc

from components.generic import tabs_builder, chart_block
from components.helpers import update_dict_params
from components.templates import PageMixin

import pandas as pd


class ProfComponent(PageMixin):

    def __init__(self,
                 stats,
                 data,
                 config):
        super().__init__(stats, data, config)

    def get_default_value(self):
        return 'Avvocato'

    def define_render_data(self):
        return [self.data] * len(self.stats)

    def define_component(self, page):
        return [dbc.Row([
            dbc.Col(children=dcc.Loading(chart_block(config=self.config,
                                         page=page,
                                         stats=self.data.Professione.unique(),
                                         dd_default_value=self.get_default_value())),
                    width=self.config['page_template']['Chart width']),
            tabs_builder(data_dict=self.config[page]['tabs'])])]

    def callback_registry(self, page):
        @dash.callback(Output(self.config[page]['chart_id'], 'figure'),
                       Input(self.config[page]['dd_id'], 'value'))
        def plot_eta_gruppo_stat(stat):
            data = self.define_mapper()[self.stats[0]]
            data = data.loc[data.Professione == stat, :]
            fig = px.line(data,
                          x='anno',
                          y='Senatori',
                          markers=True)
            font_dict = update_dict_params(self.config['page_template']['title'],
                                           title=stat + self.config['page_template']['title']['text'])
            fig.update_layout(title=font_dict)
            fig.update_traces(marker=dict(size=self.config['page_template']['chart']['m']))
            return fig

        return plot_eta_gruppo_stat

    def download_callback_registry(self, page):
        @dash.callback(Output(self.config[page]['download_id'][1], "data"),
                       Input(self.config[page]['download_id'][0], "n_clicks"),
                       Input(self.config[page]['dd_id'], 'value'),
                       prevent_initial_call=True)
        def generate_excel(n_nlicks, stat):
            if n_nlicks is None:
                return
            elif n_nlicks > 0:
                print(1)

                def to_xlsx(bytes_io):
                    data = self.define_mapper()[self.stats[0]]
                    data = data.loc[data.Professione == stat, :]
                    xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")  # requires the xlsxwriter package
                    data.to_excel(xslx_writer, index=False, sheet_name="foglio")
                    xslx_writer.save()

                return dcc.send_bytes(to_xlsx, 'senato_' + stat + ".xlsx")

        return generate_excel
