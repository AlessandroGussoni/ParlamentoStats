import dash_bootstrap_components as dbc
from dash import html

from config import config

loghi = dbc.Row([dbc.Col(html.A(href="https://www.senato.it/home",
                                children=[html.Img(alt="Link al Senato",
                                                   src=config['assets']['logo_senato'])]), lg=4),
                 dbc.Col(html.A(href="https://www.senato.it/home",
                                children=[html.Img(alt="Link al Senato",
                                                   src=config['assets']['logo_eligendo'])]), lg=4)])
layout = [html.H2('Benvenuto su ParlamentoStats'),
          html.Br(),
          html.H4('Il progetto'),
          html.P(
              "Raccogliamo dati relativi al Senato per rendere l'Istituzione più accessibile al pubblico. Alcune statistiche (come ad esempio numero di Senatori per età) vengono calcolate per legislatura direttamente dal sito del Senato, altre (numero di Governi, Legislatura media, affluenza) vengono calcolate a partire da dati pubblicati nell'archivio storico del Senato"),
          html.H4('Le fonti dati'),
          loghi,
          html.Br(),
          html.H4('Accesso ai dati'),
          html.P(
              "Al momento gli unici dati esposti e accessibili agli utenti sono quelli utilizzati per le visualizzazioni. Nelle prossime versioni del sito èin programma l'esposizione di un API per l'accesso completo alla base dati"),
          html.H4('Coming soon...'),
          html.P(
              'Nelle prossime versioni del sito verranno aggiunte statistiche su assenze, voti contrari e cambi gruppo parlamentare'),
          html.H4('Contatti'),
          html.P('Per suggerimenti, informazioni e richieste:'),
          html.P(['mail: ', html.A('aleguss@gmail.com', href='mailto:aleguss@gmail.com'), ' Twitter: ',
                  html.A('twitter/account', href='https://twitter.com/LP_Gustar8')])
          ]
