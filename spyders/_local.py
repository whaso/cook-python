import requests
from bs4 import BeautifulSoup


base_url = "https://asmrs.live/movies?page={}"

base_urls = (base_url.format(i) for i in range(220))
music_urls = []

target_text = "寸"
result = []
for url in base_urls:
    if not url:
        pass
    res = requests.get(url)
    soap = BeautifulSoup(res.text)
    divs = soap.find_all("div", {"class": "card nopadding"})
    for div in divs:
        if target_text in div.text:
            u = f"https://asmrs.live{div.a['href']}"
            print(f"find {div.text}: {u}")
            music_urls.append()

music_urls = ["https://asmrs.live/movie/60b8c1f47032e64c727a35fd"]






print(result)
print("FINISH")