import os

import pandas as pd

from config import config
from pages.affluenza_page import affluenza_component, return_aff_callback
from pages.eta_gruppo_page import EtaGruppoComponent
from pages.eta_page import EtaComponent
from pages.gov_page import GovComponent
from pages.home_page import layout
from pages.prof_page import ProfComponent
from pages.sen_page import SenComponent
from pages.study_page import StudyComponent

BASE_PATH = '/'
FILES = [file for file in os.listdir('data') if os.path.isfile(os.path.join('data', file))]

governi_component = GovComponent(data=pd.read_csv('data/' + FILES[0]),
                                 stats=None,
                                 config=config)

sen_component = SenComponent(data=pd.read_csv('data/' + FILES[1]),
                             stats=['legislatura media', 'senatori alla prima legislatura'],
                             config=config)

eta_component = EtaComponent(data=pd.read_csv('data/' + FILES[2]),
                             stats=['Totale', 'Età media', '40-49', '50-59', '60-69', '70 e oltre'],
                             config=config)

eta_gruppo_component = EtaGruppoComponent(data=pd.read_csv('data/' + FILES[3]),
                                          stats=['Età media', 'Età min', 'Età max'],
                                          config=config)

prof_component = ProfComponent(data=pd.read_csv('data/' + FILES[4]),
                               stats=['Senatori'],
                               config=config)

study_component = StudyComponent(data=pd.read_csv('data/' + FILES[5]),
                                 stats=['Senatori'],
                                 config=config)

sen_callback = sen_component.callback_registry(page='sen')
sen_download_callback = sen_component.download_callback_registry(page='sen')

eta_callback = eta_component.callback_registry(page='eta')
eta_download_callback = eta_component.download_callback_registry(page='eta')

eta_gruppo_callback = eta_gruppo_component.callback_registry(page='eta_gruppo')
eta_gruppo_download_callback = eta_gruppo_component.download_callback_registry(page='eta_gruppo')

prof_callback = prof_component.callback_registry(page='prof')
prof_download_callback = prof_component.download_callback_registry(page='prof')

study_callback = study_component.callback_registry(page='study')
study_download_callback = study_component.download_callback_registry(page='study')

aff_callback = return_aff_callback()

matches = {BASE_PATH: layout,
           BASE_PATH + FILES[0].split('.')[0]: governi_component.define_component('gov'),
           BASE_PATH + FILES[1].split('.')[0]: sen_component.define_component('sen'),
           BASE_PATH + FILES[2].split('.')[0]: eta_component.define_component('eta'),
           BASE_PATH + FILES[3].split('.')[0]: eta_gruppo_component.define_component('eta_gruppo'),
           BASE_PATH + FILES[4].split('.')[0]: prof_component.define_component('prof'),
           BASE_PATH + FILES[5].split('.')[0]: study_component.define_component('study'),
           BASE_PATH + 'Affluenza': affluenza_component}
