

import requests
import datetime
from bs4 import BeautifulSoup
import random
from util import *

class InfoCrawler():

    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list = [
        	#Chrome
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        	#Firefox
        	'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    	]


    def set_random_user_agent(self):
        user_agent = random.choice(self.user_agent_list)     # user_agent_list에서 random하게 하나 뽑기
        self.headers["User-Agent"] = user_agent
        return user_agent

    def set_tor_proxy(self):
        pass

    def get_result_data(self, *args, **kwargs):
        # this method is the goal of class
        # argument should be considered with efficiency
        # if range input is date, date format is 'YYYY/MM/DD'159
        pass


    def parse_page(self, raw_response):
        pass
        


class YahooFinanceCrawler(InfoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://query2.finance.yahoo.com/v8/finance/chart/{}?includeAdjustedClose=true&interval=1d&period1={}&period2={}"
        self.set_random_user_agent()


    def get_result_data(self, target_code, from_date_str, to_date_str):
        # 최후에 나와야 하는 느낌! -> 아랫줄 ts:INT~ 이부분
        # [ {ts:INT, open_price:FLOAT, close_price:FLOAT, .....},  {}, {}  ]
        res_list = self.parse_page(target_code, from_date_str, to_date_str)
        return res_list

    def parse_page(self, target_code, from_date_str, to_date_str):
        # parse the json. Check response by network inspector
        res_list = [] 

        from_ts = convert_date_str_to_ts(from_date_str)
        to_ts = convert_date_str_to_ts(to_date_str)
        target_url = self.base_url.format(target_code, from_ts, to_ts)

        res = requests.get(target_url, headers=self.headers)
        res_json = res.json()
        # print(res_json) -> logging으로 대체하는게 이상적임

        ts_list = res_json["chart"]["result"][0]["timestamp"]
        price_dict = res_json["chart"]["result"][0]["indicators"]["quote"][0]
        
        open_price_list = price_dict["open"]
        close_price_list = price_dict["close"]
        high_price_list = price_dict["high"]
        low_price_list = price_dict["low"]

        for ts, open_price, close_price, high_price, low_price in zip(ts_list, open_price_list, close_price_list, high_price_list, low_price_list):
            info_dict = {
                "ts": ts,
                "open": open_price,
                "close": close_price,
                "high": high_price,
                "low": low_price,
            }
        
        res_list.append(info_dict)
        
        return res_list
        # print(res_list)
    
class NaverFinanceCrawler(InfoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://finance.naver.com"

    def get_result_data(self, *args, **kwargs):
        pass

    def parse_page(self, raw_response):
        pass

class NaverDiscussionCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        

    def get_result_data(self, code, from_page, to_page):
        # [ {ts:INT, view_count:INT},  {}, {}  ]

        pass

    def parse_page(self, code, page_idx):
        info_dict_list = []
        pass

class MarketBuyerInfoCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = self.base_url + "/sise/investorDealTrendDay.naver"

    def get_result_data(self, from_page, to_page):
        # [ {ts:INT, ant:FLOAT, inst:FLOAT, foreigner:FLOAT,.....},  {}, {}  ]
        pass

    def parse_page(self, page_idx):
        pass

if __name__ == "__main__":

    yfc = YahooFinanceCrawler()
    res = yfc.get_result_data("000660.KS","2024/02/10", "2024/03/13")
    print(res)
    save_result_data(res, "test.csv")
    # yfc.parse_page("000660.KS","2024/03/10", "2024/03/13")

