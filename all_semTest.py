import bs4
import requests
import re

baseUrl = 'http://google.com/search?q='
gtuinfoUrl = 'http://gtu-info.com/'

branchSem = input(print('Enter Your Branch Name and Semester to download the syllabus file....'))
baseString = 'gtuinfo syllabus' + branchSem
resMain = requests.get(baseUrl + baseString)
soupMain = bs4.BeautifulSoup(resMain.text, 'html.parser')
eleMain = soupMain.select('.r a')
target = eleMain[0].get('href')
res = requests.get('https://google.com' + target)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
element = soup.select('.odd a')
store = []
for i in range(2, len(element), 3):
    store.append(element[i])

for each_element in store:
    link = each_element.get('href')
    subName = each_element.get_text()
    print('Downloading syllabus for: ' + subName)
    match = re.compile(r'/S.*')
    search = match.findall(link)
    url = gtuinfoUrl + ''.join(search)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    element = soup.select('.pull-right')
    target = element[0].get('href')
    res = requests.get(target)
    file = open(subName + '.pdf', 'wb')
    for chunks in res.iter_content(1000000):
        file.write(chunks)
    file.close()

print('Done!')
