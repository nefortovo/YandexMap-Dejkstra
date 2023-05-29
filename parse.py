import json
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import bs4
import pandas as pd
from bs4 import BeautifulSoup
from random import randint

# s = {'static': []}
FILE_PATH = 'index.html'
PARSED_FILE_PATH = "flats.json"



class Parser:
    __apartments = NotImplemented
    id = -1
    def __init__(self, source: str):
        self.__source = source

    @classmethod
    def counter_id(cls):
        cls.id += 1
        return cls.id

    def parse(self):

        self.__result = {'Points': [], 'Ways': []}
        with open(self.__source, 'r', encoding='utf-8') as f:
            self.__html = f.read()
        # print(self.__html)

        self.__soup = bs4.BeautifulSoup(self.__html, 'html.parser')

        self.__edge = (self.__soup.find_all('line'))

        for path in self.__edge:
            tmp = {
                'way': {
                    'from': int(path['x1']) * 10000 + int(path['y1']),
                    'to': int(path['x2']) * 10000 + int(path['y2']),
                }
            }
            self.__result['Ways'].append(tmp)

        self.__edge = (self.__soup.find_all('path', attrs={'fill': 'none'}))

        for path in self.__edge:
            crd = path['d'].strip().split('M')[1:]
            res = list
            # print(crd)
            for word in crd:
                res = (re.split(' |, ', word.strip()))
                try:
                    tmp = {
                        'way': {
                            'from': int(res[0]) * 10000 + int(res[1]),
                            'to': int(res[-2:-1][0]) * 10000 + int(res[-1:][0]),
                            # 'weight': 1,
                        }
                    }
                    self.__result['Ways'].append(tmp)
                except:
                    pass

        self.__flat = (self.__soup.find_all('g', attrs={'class': 'scheme-objects-view__station'}))
        # print(self.__flat)

        for room in self.__flat:
            self.__price = (room.find_all('circle')[1])
            # print(self.__price)
            # print(self.__price['x'])
            # print(self.__price['y'])
            tmp = {
                'point': {
                    'id': int(self.__price['x']) * 10000 + int(self.__price['y']),
                    'true_id':self.counter_id(),
                    'x': self.__price['x'],
                    'y': self.__price['y'],
                    'color': self.__price['fill'],
                },

            }
            self.__result["Points"].append(tmp)
        self.__apartments = json.dumps(self.__result, ensure_ascii=False, indent=2)
        return (self.__result)

    def save(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.__apartments)

if __name__ == '__main__':
    p = Parser(FILE_PATH)
    p.parse()
    p.save(PARSED_FILE_PATH)
