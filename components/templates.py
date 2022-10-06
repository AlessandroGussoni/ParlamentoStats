from abc import ABC, abstractmethod

import dash
import pandas as pd
from dash import dcc
from dash.dependencies import Input, Output


def stats_validator(f):
    def wrapped(self, *args, **kwargs):

        res = f(*args, **kwargs)
        check = all([key in getattr(self, 'stats') for key in res.keys()])
        if check:
            return res
        else:
            raise KeyError

    return wrapped


class IAbstractPageComponent(ABC):

    @abstractmethod
    def __init__(self,
                 stats,
                 data):
        self.data = data
        self.stats = stats

    @abstractmethod
    def define_component(self, page):
        return

    @stats_validator
    @abstractmethod
    def define_mapper(self):
        return

    @abstractmethod
    def define_render_data(self):
        return

    @abstractmethod
    def callback_registry(self):
        return


class PageMixin:

    def __init__(self,
                 stats,
                 data,
                 config):
        self.data = data
        self.stats = stats
        self.config = config

    def define_mapper(self):
        render_data = self.define_render_data()
        return {stat: render_data[i] for i, stat in enumerate(self.stats)}

    @staticmethod
    def to_xlsx(data, bytes_io):
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")  # requires the xlsxwriter package
        data.to_excel(xslx_writer, index=False, sheet_name="foglio")
        xslx_writer.save()
