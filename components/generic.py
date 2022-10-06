import dash_bootstrap_components as dbc
from dash import html, dcc


def tabs_builder(data_dict, **kwargs):
    return dbc.Col(children=dbc.Tabs([dbc.Tab([html.Ul([html.Li(value) for value in data_dict[key]])],
                                              label=key) for key in data_dict.keys()]),
                   **kwargs)


def download_button_builder(name, ids):
    return [html.Button(name, id=ids[0]), dcc.Download(id=ids[1])]


def chart_block(config: dict,
                page,
                dd_default_value: str,
                stats: list,
                additional_component=None,
                index=None):
    block = [html.H2(config[page]['h2_title']),
             html.Br(),
             dcc.Dropdown(id=config[page]['dd_id'],
                          value=dd_default_value,
                          options=[{'label': stat,
                                    'value': stat} for stat in stats],
                          style=config['page_template']['dd_style']),
             html.Br(),
             dcc.Graph(id=config[page]['chart_id'],
                       )] + download_button_builder(name=config[page]['button_name'],
                                                    ids=config[page]['download_id'])
    if additional_component is None:
        return block
    else:
        block.insert(index, additional_component)
        return block
