from Extra import *
from Crawler import Crawler

class Data(Crawler):

    def __init__(self, homepage):
        super().__init__(homepage)
        self.tsites=list()

    def get_tsites(self, a, b=[]):

        for link in self.urls:

            for i in b:   #Negative filter
                if bool(i.search(link)):
                    break
            else:
                for j in a:
                    if bool(j.search(link)):
                        self.tsites.append(link)
                        break




    def __img_hpage(self, s):
        pass


    def get_logo(self):

        ht=load_page(self.home_page)

        soup = BeautifulSoup(ht, features='lxml', parse_only=SoupStrainer('img', attrs={'src':re.compile('logo', re.IGNORECASE)}))
        t = soup.find('img', attrs={'src':re.compile('logo', re.IGNORECASE)})   #image with 'logo' in the source

        if t is None:
            # u=url_normalize(self.home_page, t['src'])
            # ur.urlretrieve(u, "logo")
            soup = BeautifulSoup(ht, features='lxml', parse_only=SoupStrainer('a'))
            t=soup.find(self.__img_hpage)              #image with link to the home page





a=input("Enter URL address: ")
b=float(input("Input delay: "))

web=Data(a)
web.crawl(b)

# while True:
#     web.crawl(b)
#     if web.index == len(web.urls):
#         break
#     c=input("Continue crawling? ")
#     if c=='n':
#         break

print("\nNo. of URLs =", len(web.urls))
print("No. of pages crawled =", web.index)


s=[]
p=[]

s.append(re.compile('vacanc', re.IGNORECASE))
s.append(re.compile('job', re.IGNORECASE))
s.append(re.compile('career', re.IGNORECASE))
s.append(re.compile('opportunit', re.IGNORECASE))
# s.append(re.compile('notice', re.IGNORECASE))   #Very generous filter
# s.append(re.compile('announcement', re.IGNORECASE))
s.append(re.compile('recruit(?!er(s)?)', re.IGNORECASE))
s.append(re.compile('position', re.IGNORECASE))
s.append(re.compile('role', re.IGNORECASE))
s.append(re.compile('walk( )?(-)?( )?in', re.IGNORECASE))
s.append(re.compile('interview', re.IGNORECASE))

p.append(re.compile('result', re.IGNORECASE))


web.get_tsites(s, p)

for i in web.tsites:
    print(i)
