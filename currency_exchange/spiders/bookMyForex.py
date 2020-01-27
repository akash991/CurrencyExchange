# -*- coding: utf-8 -*-
import scrapy
import pprint
from bs4 import BeautifulSoup
import json
import datetime
import os

class ExchangeRate():
    def __init__(self, country, currency_name, currency_symbol, rate=1,
                 comapred_to_country="India", compared_to_currency="Ruppee",
                 compared_to_symbol="INR" ):
        self.country = country
        self.currency_name = currency_name
        self.currency_symbol = currency_symbol
        self.rate = rate
        self.comapred_to_country = compared_to_currency
        self.compared_to_currency = compared_to_currency
        self.compared_to_symbol = compared_to_symbol
        
    def __str__(self):
        message = "{} VS {}".format(self.country, self.currency_symbol)
        message += "\n 1 {} = {} {}\n".format(self.comapred_to_country, self.rate, self.compared_to_symbol)
        return message

class BookmyforexSpider(scrapy.Spider):
    name = 'bookMyForex'
    allowed_domains = ['www.bookmyforex.com']
    start_urls = ['https://www.bookmyforex.com/blog/world-currencies-indian-currency-exchange-rate/']
    details = []
    current_time = ""

    def parse(self, response):
        self.get_current_time()
        path = "//table[@class='table table-bordered']"
        list_of_tables = response.xpath(path).extract()
        for data in list_of_tables:
            table = BeautifulSoup(data, "lxml")
            entries = table.findAll("tr")
            for rows in entries:
                dataEntry = rows.findAll("td")
                if len(dataEntry) > 0:
                    country = dataEntry[0].text
                    currency = dataEntry[1].text
                    symbol = dataEntry[2].text
                    rate = float(dataEntry[3].text.replace("\xa0", " ").rstrip("INR").split(" ")[0])
                    exchangeRate = ExchangeRate(country, currency, symbol, rate)
                    self.details.append(exchangeRate)
        self.jsonify(self.details)
    
    def jsonify(self, class_list):
        data_list = []
        for data in class_list:
            temp = {}
            temp['country'] = data.country
            temp['currency_name'] = data.currency_name
            temp['currency_symbol'] = data.currency_symbol
            temp['rate'] = data.rate
            temp['source_currency'] = data.compared_to_currency
            temp['time'] = self.current_time
            data_list.append(temp)
        self.dump_json_response(data_list)
            
    def dump_json_response(self, data_list):
        _file = "data.json"
        _file_size = os.path.getsize(_file)
        if _file_size == 0:
            data = json.dumps(data_list, indent=2)
            with open("data.json", "r+") as _file:
                _file.write(data)
        else:
            with open("data.json", "r+") as _file:
                json_data = json.load(_file)
            for _ in data_list:
                json_data.append(_)
            json_data = json.dumps(json_data, indent=2)
            with open("data.json", "r+") as _file:
                _file.write(json_data)
        
    def get_current_time(self):
        time = datetime.datetime.now()
        self.current_time = time.strftime("%h-%m-%Y %H:%M:%S")
        
        
            
        

            
        
