import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import sys
import codecs


class SBI_Scraper():

    def __init__(self,user_id,password):
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
        res = self.session.post(self.base_url,data=post)
        res.encoding = res.apparent_encoding

    def int_float_multiply(self,int_,num):
        if isinstance(int_,int) or isinstance(int_,float):
            return int_ * ((10)**num)
        return int_

    def int_converter(self,str_):
        if isinstance(str_,str):
            if re.compile('-|‥').search(str_):
                return str_
            elif str_.find('.') != -1:
                float_ = float(str_.replace(',',''))
                return float_
            else:
                int_ = int(str_.replace(',',''))
                return int_
        return str_

    def dividend_converter(self,str):
            str = re.sub( u'[一-龥]', "", str)
            str = re.sub( '\*', "", str)

            if str.find('〜') != -1:
                return str[:str.find('〜')]
            return str


    def financePage_html(self,ticker):
        post={
                "_ControlID": "WPLETsiR001Control",
                "_DataStoreID": "DSWPLETsiR001Control",
                "_PageID": "WPLETsiR001Idtl50",
                "getFlg": "on",
                "_ActionID": "goToSeasonReportOfFinanceStatus",
                "s_rkbn": "2",
                "s_btype": "",
                "i_stock_sec": str(ticker),
                "i_dom_flg": "1",
                "i_exchange_code": "JPN",
                "i_output_type": "4",
                "exchange_code": "TKY",
                "stock_sec_code_mul": str(ticker),
                "ref_from": "1",
                "ref_to": "20",
                "wstm4130_sort_id": "" ,
                "wstm4130_sort_kbn":  "",
                "qr_keyword": "1",
                "qr_suggest": "1",
                "qr_sort": "1"
                }
        html = self.session.post(self.base_url,data=post)
        html.encoding = html.apparent_encoding
        return html

    def get_fi_param(self,ticker):
        pd_data_all = pd.DataFrame(columns=['flag','証券コード','期末期','売上高','営業益','経常益','最終益','1株益','1株配'])
        dict_={}
        html=self.financePage_html(ticker)
        soup = BeautifulSoup(html.text, 'html.parser')
        div_shikihou = soup.find_all('div',{'class':'shikihouBox01'})[0]
        table = div_shikihou.find_all('table')[1]
        gyousyu_str = table.find_all('tr')[1].string
        tr_list = table.tr.td.table.find_all('tr',{'align':'right'})
        for i in tr_list:
            if re.compile("連|単|◎|◇|□").search(str(i.td.string)):
                dict_['証券コード'] = ticker
                dict_['flag'] = 'S'
                dict_['期末期'] = i.td.string.replace('\n','')
                td_list = i.contents
                dict_['売上高'] = self.int_float_multiply(self.int_converter(td_list[3].string.replace('\n','')),6)
                dict_['営業益'] = self.int_float_multiply(self.int_converter(td_list[5].string.replace('\n','')),6)
                dict_['経常益'] = self.int_float_multiply(self.int_converter(td_list[7].string.replace('\n','')),6)
                dict_['最終益'] = self.int_float_multiply(self.int_converter(td_list[9].string.replace('\n','')),6)
                dict_['1株益'] = self.int_float_multiply(self.int_converter(td_list[11].string.replace('\n','')),0)
                # dict_['1株配'] = self.int_float_multiply(self.int_converter(self.dividend_converter(td_list[13].string.replace('\n',''))),0)
                pd_data=pd.DataFrame(dict_,index=['1'])
                pd_data_all=pd_data_all.append(pd_data)
                pd_data_all = pd_data_all.ix[:, ['flag', '証券コード', '期末期', '売上高', '営業益', '経常益', '最終益', '1株益', '1株配']]
                print(pd_data_all)
        return pd_data_all
