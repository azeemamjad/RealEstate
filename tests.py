import requests

cookies = {
    'Authorisation': '"{\'access_token\': \'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidW1hciIsImlhdCI6MTczMjIxNTcwNywiZXhwIjoxNzMyMjMzNjAwLCJpc3MiOiJodHRwczovL2N5YmVydGhlZnR3YXRjaC5jb20iLCJhdWQiOiJjbGllbnRzIn0.tjKJ1QsDf03w9c90QAil1opY_SjOyNGkOWkQRZ-qxLg\'\\054 \'XSRF-TOKEN\': \'9A77EFD4740CC0CA6515DC51E3AC4B3B79FE97C2CB9C3E13987E26237DEAAFE1\'}"',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'Authorisation="{\'access_token\': \'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidW1hciIsImlhdCI6MTczMjIxNTcwNywiZXhwIjoxNzMyMjMzNjAwLCJpc3MiOiJodHRwczovL2N5YmVydGhlZnR3YXRjaC5jb20iLCJhdWQiOiJjbGllbnRzIn0.tjKJ1QsDf03w9c90QAil1opY_SjOyNGkOWkQRZ-qxLg\'\\054 \'XSRF-TOKEN\': \'9A77EFD4740CC0CA6515DC51E3AC4B3B79FE97C2CB9C3E13987E26237DEAAFE1\'}"',
    'Origin': 'https://staging.cybertheftwatch.com',
    'Referer': 'https://staging.cybertheftwatch.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'XSRF-TOKEN': 'PmHVrJ7c9TKzi-HKgjESU5an7So5pdUct5r4gKmQVCU',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

json_data = {
    'users': [],
    'types': [],
    'clients': [
        15,
    ],
    'assets': [
        1594,
    ],
    'dateRange': None,
}

response = requests.post(
    'https://internal.cybertheftwatch.com:8020/admin/cyboverview/export',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.json())