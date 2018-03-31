import requests
from lxml import html

def delete_spaces(string):
    i = 0
    while i < len(string) and string[i].isspace():
        i += 1
    j = len(string) - 1
    while j >= 0 and string[j].isspace():
        j -= 1
    return string[i:j + 1]


url = 'https://icorating.com/ico/' #url to get information from
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'} #header for better access to sites
r = requests.get(url, headers=headers) #make request to site

tree = html.fromstring(r.text) #make tree of elements

file = open('ongoing_industry.txt', 'w')

#print industry names of ico organisations from the first table(ico with rating)
i = 0
while True:
    try:
        i += 1
        j = 0
        s = '/html/body/main/div[4]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[7]/text()'
        out = tree.xpath(s)[0]
        while True:
            try:
                out = tree.xpath(s)[j]
                tmp = delete_spaces(out)
                if j == 0:
                    file.write(tmp)
                elif len(tmp) > 0:
                    file.write(', ' + tmp)
                j += 1
            except IndexError:
                break
        file.write('\n')
    except IndexError:
        break

#print industry names of ico organisations from the second table(ico without rating)
i = 0
while True:
    try:
        i += 1
        j = 0
        s = '/html/body/main/div[5]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[7]/text()'
        out = tree.xpath(s)[0]
        while True:
            try:
                out = tree.xpath(s)[j]
                tmp = delete_spaces(out)
                if j == 0:
                    file.write(tmp)
                elif len(tmp) > 0:
                    file.write(', ' + tmp)
                j += 1
            except IndexError:
                break
        file.write('\n')
    except IndexError:
        break
file.close()