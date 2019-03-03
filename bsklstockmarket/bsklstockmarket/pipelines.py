# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from datetime import datetime
from decimal import *

class BsklstockmarketPipeline(object):
    def open_spider(self, spider):
        print('open spider')
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="password",
          database="stocksmarket"
        )

    def close_spider(self, spider):
        print('close spider')

    def process_item(self, item, spider):
        mycursor = self.mydb.cursor()
        if item['high_price'] != '-':
            sql = "INSERT INTO stocks" \
                    "(board, high_price, last_price, " \
                    "logged_date, logged_time, low_price, " \
                    "open_price, stock_code, stock_name, counter)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            val = (
                    item['board'], 
                    Decimal(item['high_price']),
                    Decimal(item['last_price']),
                    datetime.strptime(item['logged_date'], '%d %b %Y'),
                    datetime.strptime(item['logged_time'], '%I:%M %p'),
                    Decimal(item['low_price']),
                    Decimal(item['open_price']),
                    item['stock_code'],
                    item['stock_name'],
                    item['counter']
                )
        else:
            sql = "INSERT INTO stocks" \
                    "(board, last_price, " \
                    "logged_date, logged_time, " \
                    "stock_code, stock_name, counter)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            
            val = (
                    item['board'],
                    Decimal(item['last_price']),
                    datetime.strptime(item['logged_date'], '%d %b %Y'),
                    datetime.strptime(item['logged_time'], '%I:%M %p'),
                    item['stock_code'],
                    item['stock_name'],
                    item['counter']
                )

        mycursor.execute(sql, val)
        self.mydb.commit()
        
        print('Saving .. Company %s' % item['stock_name'])
        return item
