#!/usr/bin/env python3
#coding:utf8

"""
Author:         ottocho
Filename:       getmodels.py
Last modified:  2016-08-22 02:18
Description:
    iPhone wiki about models and generations
    get model->generation map
"""

import sys
import urllib

from pprint import pprint
from bs4 import BeautifulSoup

URL = 'https://www.theiphonewiki.com/wiki/Models'

def get_page_content(url=URL):
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

def parse_html(html):
    '''
    return format:
    { brand: list_of_generations }

    example:
    {
        u'iPod touch': [
            {
                u'"A" Number': u'A1213',
                u'Bootrom': u'Bootrom Rev.2',
                u'Color': u'Black',
                u'FCC ID': u'BCGA1213',
                u'Generation': u'iPod touch',
                u'Identifier': u'iPod1,1',
                u'Internal Name': u'N45AP',
                u'Model': u'A1213',
                u'Storage': u'iPod touch'
            },
            ...
        ],
        u'iPhone': [... ]
        ...
    }
    '''
    soup = BeautifulSoup(html, 'html.parser')
    all_table_data = {}

    for table in soup.find_all('table', class_='wikitable'):
        _table_data = []

        # get the `brand` from the head(H2 tag)
        _h2 = table.find_previous_sibling('h2')
        brand = _h2.find('a').contents[0]

        # fill the tds to solve the `rowspan` problem
        tmp_tds = {}
        n_column = 0
        names_column = []

        # collect data from each row(tr)
        for n, tr in enumerate(table.find_all('tr')):
            if n == 0:
                # initialize the tmp data by the first row
                ths = tr.find_all('th')
                names_column = [ th.contents[0].strip() for th in ths ]
                n_column = len(names_column)
                tmp_tds = dict((i, None) for i in range(n_column))
                continue

            tds = tr.find_all('td')
            if n == 1:
                # initialize the `tmp_tds` by the second row
                for idx, td in enumerate(tds):
                    if td.has_attr("rowspan"):
                        rowspan = int(td.attrs['rowspan'])
                        tmp_tds[idx] = [td, rowspan]
            _iter = iter(tds)
            _colected_tds = []
            for i in range(n_column):
                if tmp_tds.get(i):
                    tmp_tds[i][1] -= 1
                    td, cols = tmp_tds[i]
                    _colected_tds.append(td)
                    if cols == 0:
                        tmp_tds[i] = None
                else:
                    td = next(_iter)
                    # append the `rowspan` rd
                    if td.has_attr("rowspan"):
                        _colected_tds.append(td)
                        rowspan = int(td.attrs['rowspan'])-1
                        if rowspan > 0:
                            tmp_tds[i] = [td, rowspan]
                    else:
                        _colected_tds.append(td)

            # append each row data to table data
            _row_data = {}
            for i in range(n_column):
                value = None
                td = _colected_tds[i]
                if td.find('a'):
                    value = td.find('a').contents[0].strip()
                else:
                    value = td.contents[0].strip()
                _row_data[names_column[i]] = value
            _table_data.append(_row_data)
        all_table_data[brand] = _table_data
    return all_table_data

def print_table_csv(table_data):
    spliter = '|'
    print(spliter.join(('Identifier', 'Generation', 'Device')))
    for brand, dlist in table_data.iteritems():
        _bd = dict((_d['Identifier'], _d['Generation']) for _d in dlist)
        for _i, _g in _bd.iteritems():
            print(spliter.join((_i, _g, brand)))

def main():
    html = get_page_content()
    table_data = parse_html(html)

    import json
    print(json.dumps(table_data, indent=4))
    # print_table_csv(table_data)

if __name__ == '__main__':
    main()
