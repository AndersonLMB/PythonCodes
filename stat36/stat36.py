import bs4
import urllib.request
import urllib.response
import _codecs_cn
import codecs

#输入url,输出content
def download(url):
    if url is None:
        return None
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0")
    res = urllib.request.urlopen(req)
    content = res.read()
    return content
    pass

#输入content,输出bs对象
def bsparse(html):
    soup = bs4.BeautifulSoup(html,"html.parser")
    return soup

def loadBranches(soup,type,url,superior):
    if type == "nation":
        provinces = soup.findAll("a",href=True, class_=False)
        branches = []
        for province in provinces:
            branch = Node()
            branch.url = province["href"]
            branch.name = province.text
            branch.code = province["href"].split(".")[0]
            branch.type = "province"
            branch.superior = superior
            branch.url = url + province["href"]
            print("------")
            print(str(branch.superior.name) + str(branch.name))
            branches.append(branch)
            branch.loadAllBranches()
            pass
        return branches
        pass
    if type == "province":
        cities = soup.findAll("tr", class_="citytr")
        branches = []
        for city in cities:
            branch = Node()
            branch.name = city.td.nextSibling.a.text
            branch.superior = superior
            branch.code = str(city.td.a["href"]).split("/")[1].split(str(city.td.a["href"]).split("/")[0])[1].split(".")[0]   
            branch.url = url.split(".html")[0] + "/" + str(city.td.a["href"]).split("/")[1]
            branch.type = "city"
            print(str(branch.superior.name) + " " + str(branch.name))
            branches.append(branch)
            branch.loadAllBranches()
            pass
        return branches

    if type == "city":
        #print(" └load all counties of " + str(superior))
        counties = soup.findAll("tr",class_="countytr")
        branches = []
        for county in counties:
            branch = Node()
            branch.superior = superior
            if county.td.a:
                branch.name = county.td.nextSibling.a.text

                pass
            else:
                branch.name = county.td.nextSibling.text
            print(branch.superior.name + " " + branch.name)
        pass

class Node():
    name = ""
    url = ""
    type = ""
    code = ""
    superior = ""
    branches = []

    def loadAllBranches(self):
        html = download(self.url)
        soup = bsparse(html)
        type = self.type
        self.branches = loadBranches(soup,type,self.url,self)
        pass
    pass

#china = Node()
#china.name = "中华人民共和国"
#china.url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/"
#china.type = "nation"
#china.loadAllBranches()
#print(china.branches)

anhui=Node()
anhui.name="安徽省"
anhui.url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/34.html"
anhui.type="province"
anhui.loadAllBranches()

#suzhou = Node()
#suzhou.url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/34/3413.html"
#suzhou.type = "city"
#suzhou.loadAllBranches()

#html = download("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/")
#soup = bsparse(html)
#print(soup.prettify())

    