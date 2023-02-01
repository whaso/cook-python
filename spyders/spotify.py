
import requests
import os

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://open.spotify.com',
    'Range': 'bytes=0-2379400',
    'Referer': 'https://open.spotify.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    '1674955636_Tsr9nVObS20eet7SnH03KpgbRTafDxmFPCVmK998r1Q': '',
}

res = requests.get(
    'https://audio-fa.scdn.co/audio/d8693b2902709919560e06bd330ad677777544b0?1674955636_Tsr9nVObS20eet7SnH03KpgbRTafDxmFPCVmK998r1Q=',
    # params=params,
    headers=headers,
)
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = f"{current_dir}/mp3/test.mp3"
with open(file_path, 'wb') as fd:
    fd.write(res.content)
    # for chunk in res.iter_content():
    #     fd.write(chunk)