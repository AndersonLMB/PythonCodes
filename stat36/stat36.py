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
    soup = bs4.BeautifulSoup(html,"html.parser",from_encoding="gb18030")
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
            print(branch.getFullname())
            #print(str(branch.superior.name) + str(branch.name))
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
            branch.fullcode = city.td.text
            branch.url = url.split(".html")[0] + "/" + str(city.td.a["href"]).split("/")[1]
            branch.type = "city"
            print(branch.getFullname())
            #print(str(branch.fullcode) + " " + str(branch.superior.name) + " "
            #+ str(branch.name))
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
            branch.type = "county"
            branch.fullcode = county.td.text
            if county.td.a:
                branch.name = county.td.nextSibling.a.text
                temp = superior.url.split("/")
                temp[len(temp) - 1] = str(county.td.nextSibling.a["href"])
                temp = "/".join(temp)
                branch.url = temp
                print(branch.getFullname())
                #print(str(branch.fullcode) + " " + branch.superior.name + " "
                #+ branch.name)
                branch.loadAllBranches()
                pass
            else:
                branch.name = county.td.nextSibling.text
                print(branch.getFullname())
                #print(str(branch.fullcode) + " " + branch.superior.name + " "
                #+ branch.name)
                pass
            branches.append(branch)
            pass
        pass

    if type == "county":
        #print("load all town(s) of " + superior.name)
        towns = soup.findAll("tr",class_="towntr")
        branches = []
        for town in towns:
            branch = Node()
            branch.superior = superior
            branch.type = "town"
            branch.fullcode = town.td.text
            if town.td.a:
                branch.name = town.td.nextSibling.a.text
                temp = superior.url.split("/")
                temp[len(temp) - 1] = str(town.td.nextSibling.a["href"])
                temp = "/".join(temp)
                branch.url = temp
                print(branch.getFullname())
                #print(str(branch.fullcode) + " " + branch.superior.name + " "
                #+ branch.name)
                #print(branch.superior.name + " " + branch.name + branch.url)
                branch.loadAllBranches()
                pass
            else:
                branch.name = town.td.nextSibling.text
                print(branch.getFullname())
                #print(str(branch.fullcode) + " " + branch.superior.name + " "
                #+ branch.name)
                pass
            branches.append(branch)
        pass

    if type == "town":
        #print("load all town(s) of " + superior.name)
        villages = soup.findAll("tr",class_="villagetr")
        branches = []
        for village in villages:
            branch = Node()
            branch.superior = superior
            branch.type = "village"
            branch.fullcode = village.td.text
            if village.td.a:
                branch.name = village.td.nextSibling.nextSibling.a.text
                temp = superior.url.split("/")
                temp[len(temp) - 1] = str(village.td.nextSibling.a["href"])
                temp = "/".join(temp)
                branch.url = temp
                print(branch.getFullname())
                branch.loadAllBranches()
                pass
            else:
                branch.name = village.td.nextSibling.nextSibling.text
                #print(str(branch.fullcode) + " " + branch.superior.name + " "+
                #branch.name)
                print(branch.getFullname())
                #print(getSupAndSelf(branch))
                pass
            branches.append(branch)
        pass

    pass
class Node(object):
    def getFullname(self):
        if self.superior is None:
            return str(self.name)
        else:
            temp = str(self.superior.getFullname())
            return str(temp) + str(self.name)
        pass

    #def getFullname(self):
    #    if self.type == "village":
    #        return self.superior.superior.superior.superior.superior.name + "
    #        " + self.superior.superior.superior.superior.name + " " +
    #        self.superior.superior.superior.name + " " +
    #        self.superior.superior.name + " " + self.superior.name + " " +
    #        self.name
    #    if self.type == "town":
    #        return self.superior.superior.superior.superior.name + " " +
    #        self.superior.superior.superior.name + " " +
    #        self.superior.superior.name + " " + self.superior.name + " " +
    #        self.name
    #    if self.type == "county":
    #        return self.superior.superior.superior.name + " " +
    #        self.superior.superior.name + " " + self.superior.name + " " +
    #        self.name
    #    if self.type == "city":
    #        return (self.superior.superior.name + " " + self.superior.name + "
    #        " + self.name)
    #    if self.type == "province":
    #        return (self.superior.name + " " + self.name)

    name = ""
    url = ""
    type = ""
    code = ""
    fullcode = ""
    superior = None
    branches = []



    def loadAllBranches(self):
        html = download(self.url)
        soup = bsparse(html)
        type = self.type
        self.branches = loadBranches(soup,type,self.url,self)
        pass

    


    pass

#def getSupAndSelf(sel=Node()):
#    if sel.superior is None:
#        return sel.name
#    else:
#        return getSupAndSelf(sel.superior) + sel.name
#    pass
china = Node()
#print(china.getFullname())
china.name = "中华人民共和国"
china.url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/"
china.type = "nation"
#print(china.getFullname())
china.loadAllBranches()
print(china.branches)

#anhui=Node()
#anhui.name="河北省"
#anhui.url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/13.html"
#anhui.type="province"
#anhui.loadAllBranches()

#anhui=Node()
#anhui.name="安徽省"
#anhui.url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/34.html"
#anhui.type="province"
#anhui.loadAllBranches()

#wuhu = Node()
#wuhu.url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/34/3402.html"
#wuhu.type = "city"
#wuhu.loadAllBranches()

#suzhou = Node()
#suzhou.url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/34/3413.html"
#suzhou.type = "city"
#suzhou.loadAllBranches()

#html = download("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/")
#soup = bsparse(html)
#print(soup.prettify())

    