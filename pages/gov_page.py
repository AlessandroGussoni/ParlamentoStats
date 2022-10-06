import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc

from components.generic import tabs_builder
from components.helpers import update_dict_params
from components.templates import PageMixin


class GovComponent(PageMixin):

    def __init__(self,
                 stats,
                 data,
                 config):
        super().__init__(stats, data, config)

    def define_render_data(self):
        return [self.data.groupby('anno', as_index=False).leg.nunique()]

    def define_component(self, page):
        return [dbc.Row([dbc.Col(children=dcc.Loading([html.H2(self.config[page]['h2_title']),
                                                       html.Br(),
                                                       dcc.Graph(figure=self.build_figure())]),
                                 width=self.config['page_template']['Chart width']),
                         tabs_builder(data_dict=self.config[page]['tabs'])])]

    def build_figure(self):
        render_data = self.define_render_data()[0]
        render_data.loc[render_data.anno == 1948, 'leg'] = 6
        fig = px.line(x=render_data['anno'],
                      y=render_data['leg'],
                      markers=True)
        font_dict = update_dict_params(self.config['page_template']['title'],
                                       title='Numero di governi per legislatura')
        fig.update_layout(title=font_dict,
                          xaxis_title="Anno",
                          yaxis_title="Numero di governi",
                          )
        fig.update_traces(marker=dict(size=self.config['page_template']['chart']['m']))
        return fig
