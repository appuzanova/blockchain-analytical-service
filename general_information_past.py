import requests
from lxml import html

def modify(string):
    i = 0
    while i < len(string) and string[i].isspace():
        i += 1
    j = len(string) - 1
    while j >= 0 and string[j].isspace():
        j -= 1
    for k in range(i, j + 2):
        if string[k] == '_' or string[k] == '*':
            string[k] = '?'
    return string[i:j + 1]


url = 'https://icorating.com/ico/past/?sort=postico&sort_un=rating&&&&#un_table'
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'}
r = requests.get(url, headers=headers)

tree = html.fromstring(r.text)

info = open('general_information_past.txt', 'w')
name = open('past_ico_name.txt', 'w')
date = open('past_dates.txt', 'w')
other = open('past_other.txt', 'w')

#general information about ico organisations from the first table(ico with rating)
i = 0
while True:
    try:
        i += 1
        s = '//*[@id="main_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[2]/text()'
        out = tree.xpath(s)[0]
        out = modify(out)
        info.write(out + ' ')
        name.write(out + '\n')
        s = '//*[@id="main_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[3]/text()'
        out = tree.xpath(s)[0]
        out = modify(out)
        info.write(out + ' ')
        date.write(out + '\n')
        try:
            s = '//*[@id="main_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[4]/a/span/text()'
            out = tree.xpath(s)[0]
            out = modify(out)
            info.write(out + ' ')
            other.write(out + ' ')
        except IndexError:
            info.write('NA ')
            other.write('NA ')
        try:
            s = '//*[@id="main_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[5]/a/span/text()'
            out = tree.xpath(s)[0]
            out = modify(out)
            info.write(out + ' ')
            other.write(out + ' ')
        except IndexError:
            info.write('NA ')
            other.write('NA ')
        s = '//*[@id="main_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[8]/span/text()'
        out = tree.xpath(s)[0]
        out = modify(out)
        info.write(out + '\n')
        other.write(out + '\n')
    except IndexError:
        break

#general information about ico organisations from the second table(ico without rating)
i = 0
while True:
    try:
        i += 1
        s = '//*[@id="un_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[2]/text()'
        out = tree.xpath(s)[0]
        out = modify(out)
        info.write(out + ' ')
        name.write(out + '\n')
        s = '//*[@id="un_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[3]/text()'
        out = tree.xpath(s)[0]
        out = modify(out)
        info.write(out + ' ')
        date.write(out + '\n')
        try:
            s = '//*[@id="un_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[4]/a/span/text()'
            out = tree.xpath(s)[0]
            out = modify(out)
            info.write(out + ' ')
            other.write(out + ' ')
        except IndexError:
            info.write('NA ')
            other.write('NA ')
        try:
            s = '//*[@id="un_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[5]/a/span/text()'
            out = tree.xpath(s)[0]
            out = modify(out)
            info.write(out + ' ')
            other.write(out + ' ')
        except IndexError:
            info.write('NA ')
            other.write('NA ')
        s = '//*[@id="un_table"]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[8]/span/text()'
        out = tree.xpath(s)[0]
        out = modify(out)
        info.write(out + '\n')
        other.write(out + '\n')
    except IndexError:
        break

info.close()
name.close()
date.close()
other.close()

