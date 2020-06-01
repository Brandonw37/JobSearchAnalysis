from bs4 import BeautifulSoup
import urllib.request as ur
import re
import sys
from tqdm import tqdm

##remove things that we do not want
red_flags = ["senior", "intern", "contract", "staff"]

def qualifies(title):
    title = title.lower()

    for word in red_flags:
        if word in title: return False
    return True

''' TEST CONDITION 1
test = qualifies("Senior Software Engineer")
print(test)
'''
##Define Regex,
##should not have phrases 1+year, 1-2 years,...
p1 = re.compile('[2-9]\s*\+?-?\s*[1-9]?\s*[yY]e?a?[rR][Ss]?')
p2 = re.compile('[Cc]itizens?(ship)?')

''' TEST CONDITION 2
t1 = p1.search("2+ Years of experience")
t2 = p1.search("0-1 Year")

print(t1, "\n", t2)
'''

## First page
url = "https://www.indeed.com/jobs?q=data+engineer&l=United+states"
pgno = 0
try:
    response = ur.urlopen(url+"&start="+str(pgno))
    html_doc = response.read()
except:
    print("URL not found")
    exit()
soup = BeautifulSoup(html_doc, 'html.parser')
'Ready.'

##save to text file
with open('JobSearch.txt','w', encoding='utf-8') as f:
    f.write(soup.prettify())

try:
    total_results = soup.find(id="searchCountPages").get_text()
    last_page = re.findall(r'[0-9]+', total_results)
    LP = [last_page[1]+last_page[2]]
    for i in range(0, len(LP)):
        LP[i] = int(LP[i])
    LP2 = int(LP[0] / 18)
##    last_page = int(int(total_results[total_results.index("of")+2: total_results.index("jobs")].strip()))
    print(total_results)
    print(LP2)
except:
    print("No jobs found")

## iterates through each webpage

jobs_per_page =  10
goodlinks = []
word_count = []

for pgno in tqdm(range(0,20, jobs_per_page)):
    if pgno > 0:
        try:
            response = ur.urlopen(url+'&start='+str(pgno))
            html_doc = response.read()
        except:
            break
        soup = BeautifulSoup(html_doc,'html.parser')
    for job in soup.find_all(class_ = 'jobtitle turnstileLink'):
        try:
            jt = "http://www.indeed.com"+job.get('href')
            print(jt)
        except:
            jt = ""
        try:
            html_doc2 = ur.urlopen(jt).read().decode('utf-8')
        except:
            print("URL not found")
            continue
        soup2 = BeautifulSoup(html_doc2, 'html.parser')
        list2 = ['ETL', 'Spark', 'Hadoop', 'Terraform', 'Python']
        for words in list2:
            try:
                i = soup2.find(id="jobDescriptionText").get_text()
                word = re.findall(words, i)
                word_str = word.count('Python')
                print(word_str)
            except:
                print("Not Found")
            word_count.append(word_str)
            goodlinks.append(jt)

##print(goodlinks)