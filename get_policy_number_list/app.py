#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import yaml


def lambda_handler(event, context):
        d = SBI_Scraper('ID', 'password')
        json = d.get_fi_param()
        return json


class SBI_Scraper():

    def __init__(self, user_id, password):
        self.base_url = "https://site1.sbisec.co.jp/ETGate/"
        self.user_id = user_id
        self.password = password
        self.login()

    def login(self):
        post = {
                'JS_FLG': "0",
                'BW_FLG': "0",
                "_ControlID": "WPLETlgR001Control",
                "_DataStoreID": "DSWPLETlgR001Control",
                "_PageID": "WPLETlgR001Rlgn20",
                "_ActionID": "login",
                "getFlg": "on",
                "allPrmFlg": "on",
                "_ReturnPageInfo": "WPLEThmR001Control/DefaultPID/DefaultAID/DSWPLEThmR001Control",
                "user_id": self.user_id,
                "user_password": self.password
                }
        self.session = requests.Session()
        res = self.session.post(self.base_url, data=post)
        res.encoding = res.apparent_encoding

    def financePage_html(self, ticker):
        post = {
                "_ControlID": "WPLETsiR001Control",
                "_DataStoreID": "DSWPLETsiR001Control",
                "_PageID": "WPLETsiR001Idtl10",
                "getFlg": "on",
                "_ActionID": "stockDetail",
                "s_rkbn": "",
                "s_btype": "",
                "i_stock_sec": "",
                "i_dom_flg": "1",
                "i_exchange_code": "JPN",
                "i_output_type": "0",
                "exchange_code": "TKY",
                "stock_sec_code_mul": str(ticker),
                "ref_from": "1",
                "ref_to": "20",
                "wstm4130_sort_id": "",
                "wstm4130_sort_kbn":  "",
                "qr_keyword": "",
                "qr_suggest": "",
                "qr_sort": ""
                }

        html = self.session.post(self.base_url, data=post)
        html.encoding = html.apparent_encoding
        return html

    def get_fi_param(self):
        investment_indicators = {}
        with open('list.yml') as file:
            obj = yaml.safe_load(file)

        ticker_list = obj.get('ticker')
        investment_indicators_list = []
        for ticker in ticker_list:
            dict_ = {}
            html = self.financePage_html(ticker)
            soup = BeautifulSoup(html.text, 'html.parser')
            div_clmsubarea = soup.find_all('div', {'id': 'clmSubArea'})[0]
            table = div_clmsubarea.find_all('table')[1]
            p_list = table.tbody.find_all('p', {'class': 'fm01'})
            dict_['証券コード'] = ticker
            dict_['予想PER'] = p_list[1].string.replace('\n', '')
            dict_['予想EPS'] = p_list[3].string.replace('\n', '')
            dict_['実績PBR'] = p_list[5].string.replace('\n', '')
            dict_['実績BPS'] = p_list[7].string.replace('\n', '')
            dict_['予想配当利'] = p_list[9].string.replace('\n', '')
            investment_indicators_list.append(dict_)
        investment_indicators['投資指標'] = investment_indicators_list

        return investment_indicators

