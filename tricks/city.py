
from requests_html import HTMLSession
import re
session = HTMLSession()

year = 2017
count = 0

province_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{year}/index.html'
city_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{year}/{pid}.html'
country_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{year}/{pid}/{cid}.html'


def get_Province_list():
    response = session.get(province_url.format(year=year))
    content = response.html.find('table.provincetable', first=True)
    li_list = content.find('a')
 
    for li in li_list:
        url = li.attrs['href']
        code=re.findall("\d+",url)[0]
        name=li.text
        parent_code = "000000"
        print("name,  code,  parent_code")
        print(f"{name}, {f_code(code)}, {parent_code}")
        save_data(name, f_code(code), parent_code)
 
        get_City_list(code)


def get_City_list(pid):
    response = session.get(city_url.format(year=year, pid=pid))
 
    content = response.html.find('table.citytable', first=True)
    citys = content.find('tr.citytr')
 
    for city in citys:
        td_list = city.find('td')
        ycode=td_list[0].find('a')[0]
        ccode=ycode.text[0:4]
        cname=td_list[1].find('a')[0].text

        # SQL 插入语句
        print(f"{cname}, {f_code(ccode)}, {f_code(pid)}")
        save_data(cname, f_code(ccode), f_code(pid))
 
        get_County_list(pid,ccode)


#获取县级市
def get_County_list(pid, cid):
    global count
    empty_list = []
    response = session.get(country_url.format(year=year, pid=pid, cid=cid))
    content = response.html.find('table.countytable', first=True)
    if content:
        citys = content.find('tr.countytr')
        for city in citys:
            td_list = city.find('td')
            ycode=td_list[0].find('a')
      
            if len(ycode) == 0:
                ccode =td_list[0].text
                cname = td_list[1].text
            else:
                ccode = ycode[0].text[0:6]
                cname = td_list[1].find('a')[0].text
 
        print(f"{cname}, {f_code(ccode)}, {f_code(cid)}")
        save_data(cname, f_code(ccode), f_code(cid))
        count += 1
            
    else:
        empty_list.append((pid, cid))
        print(f"ERROR!!!!!!!!{empty_list}")

    print(f"count: {count}, empty: {empty_list}")


def f_code(code, length=6):
    code += "0" * (length - len(code))
    return code


def save_data(name, code, parent_code):
    pass


if __name__ == '__main__':
    get_Province_list()
