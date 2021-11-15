import requests
import bs4

url = "http://www.tcmap.com.cn/list/jiancheng_list.html"


rsp = requests.get(url)

content = rsp.content.decode("gbk")

a = bs4.BeautifulSoup(rsp.content, features="html.parser")

city_list = a.find_all(align="center")

# city_url_list = [d.a.get("href") for d in city_list if d.a.get("href") else ""]else

city_path_list = list()

for c in city_list:
    if c.a and c.a.get("href"):
        city_dict = dict(
            name=c.a.get_text("href"),
            url=f"http://www.tcmap.com.cn{c.a.get('href')}"
        )
        city_path_list.append(city_dict)

city_path_list.pop(0)

print(len(city_path_list), city_path_list)


for province in city_path_list:
    province_content = bs4.BeautifulSoup(requests.get(province.get("url")).content)
    province_table = province_content.find(width="396px")
    province_name = province_table.td.text.split(":")[1]
    province_code = province_table.text.split("  ")[2].split(":")[2]

    districts_table = province_content.find(width="728")

