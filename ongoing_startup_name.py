import requests
from lxml import html

url = 'https://icorating.com/ico/?filter=ongoing' #url to get information from
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'} #header for better access to sites
r = requests.get(url, headers=headers) #make request to site

tree = html.fromstring(r.text) #make tree of elements

file = open('ongoing_startup_name.txt', 'w')

#print names of ico organisations from the first table(ico with rating)
i = 0
while True:
    try:
        i += 1
        s = '/html/body/main/div[4]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[2]/text()'
        comp_list_lxml = tree.xpath(s)
        out = comp_list_lxml[0]
        file.write(''.join(elem for elem in out if not elem.isspace()) + '\n')
    except IndexError:
        break

#print names of ico organisations from the second table(ico without rating)
i = 0
while True:
    try:
        i += 1
        s = '/html/body/main/div[5]/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']/td[2]/text()'
        comp_list_lxml = tree.xpath(s)
        out = comp_list_lxml[0]
        file.write(''.join(elem for elem in out if not elem.isspace()) + '\n')
    except IndexError:
        break
file.close()