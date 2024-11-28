import json

import requests

def get_regional_data(search_query: str):
    cookies = {
        'RF_BROWSER_ID': 'V2vhRHVYSw6uwV_MkNqW-Q',
        'RF_BROWSER_ID_GREAT_FIRST_VISIT_TIMESTAMP': '2024-11-26T11%3A58%3A51.451746',
        'RF_BID_UPDATED': '1',
        '_gcl_au': '1.1.772515649.1732651139',
        '__pdst': '1ca4844ec1a54f4e9362c9faa4f838e0',
        '_scor_uid': 'c344b9ebc611452e8a039ba1cdb004df',
        '_pin_unauth': 'dWlkPVpUaGpZamhsTVdZdE4yVmpPQzAwTUdaakxUZzVZemt0WmpneFkyUXhZakE0TmpFMg',
        'RF_VISITED': 'true',
        'searchMode': '1',
        'sortOrder': '1',
        'sortOption': 'special_blend',
        '_fbp': 'fb.1.1732651267107.624212160447874825',
        'RF_BUSINESS_MARKET': '27',
        'save_search_nudge_flyout': '1%251732687110079%25false',
        # 'RF_MARKET': 'hamptonroads',
        # 'unifiedLastSearch': 'name%3DCoconino%2520County%26subName%3DAZ%252C%2520USA%26url%3D%252Fcounty%252F215%252FAZ%252FCoconino-County%26id%3D5_215%26type%3D5%26unifiedSearchType%3D5%26isSavedSearch%3D%26countryCode%3DUS',
        # 'RF_MARKET': 'flagstaff',
        'RF_BROWSER_CAPABILITIES': '%7B%22screen-size%22%3A3%2C%22events-touch%22%3Afalse%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%7D',
        'RF_TRAFFIC_SEGMENT': 'organic',
        'audS': 't',
        'FEED_COUNT': '%5B%22%22%2C%22f%22%5D',
        'AMP_TOKEN': '%24NOT_FOUND',
        '_gid': 'GA1.2.1877994105.1732761492',
        'OptanonAlertBoxClosed': '2024-11-28T02:38:27.527Z',
        '_rdt_uuid': '1732651141686.b9bfaab9-ac24-4939-8fcb-2aea8a63eadc',
        'RF_CORVAIR_LAST_VERSION': '551.1.0',
        '_ga_928P0PZ00X': 'GS1.1.1732760987.4.1.1732761508.44.0.0',
        '_ga': 'GA1.1.397345153.1732651141',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Nov+28+2024+07%3A38%3A29+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4cd1ba09-ff79-49e6-9a63-af530c5b60dd&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=PK%3BPB',
        'userPreferences': 'parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26viewedSwipeableHomeCardsDate%3D1732761513905',
        'RF_LAST_NAV': '0',
        '_ga_P8GPVZXD5S': 'GS1.1.1732760987.2.0.1732761517.0.0.0',
        'aws-waf-token': '2c2b8ed0-1abc-49d3-8eab-043c8d0a8acc:BQoAu4MSVukgAAAA:C13rMc9VviUC+xR/cXKDCBRdnNcdkkDG6L8+eUz4Ui3+DIHscIHNLWy1h8OounOImOWOk/A4tFscy3xbEzb1ckV+R2579Ve/38je79JMmZ12J6Opig8gu67wj4CXPN5SMafm8LBpXdrApsdRb0PRxdR6GV2jjwfsDuX4Xrj7nL8Pb9O1LP1xlKqiJFHaJca7KBQfQAi2UbvTS1+8OBsYURfD3Qeb2bo5NRZ9kWDEXhYEiOgp/cYy75Ahd23RZBVvzQ==',
        'tude-rvn-rel-Mdd5C': '1.4.0',
        'cw-test-20241121-viewable-refresh': 'test',
        'cw-test-20241121-intersection-observer': 'test',
        '_sharedid': 'a115397b-14ec-4b40-b6e9-f0952f29b382',
        '_sharedid_cst': 'VyxHLMwsHQ%3D%3D',
        'pbjs_fabrickId': '%7B%22fabrickId%22%3A%22E1%3AzyQdbCbYyw7QuJBJwX-zcmx54XXxMoqRfdBjvfg6yPY5RLPl2oCYYe7G78OlAqvxKjWkAuGfBVGXHw9GdGANziPENoQzsqO2J1URTI0X4WA%22%7D',
        'pbjs_fabrickId_cst': 'VyxHLMwsHQ%3D%3D',
        'cto_bidid': 'vZXNi19WZkN4JTJGaXc4aGhBQ3c5cFcyMnBFM0olMkZhRFVSZERCOEgwJTJGTFR5VVAwcWNuSjBZZVJDVXhNcG45JTJGM0klMkJab3pwRE1LOGxvcmdkellESGFLeW1WVkZtWndqZ2I3VXBNWjFHTnNaMDJaQ3BlOGMlM0Q',
        '_cc_id': 'ee373f584ba401bf60beac776650005b',
        'panoramaId_expiry': '1733366382137',
        'panoramaId': '8736f40d6e10207182b10e1aafa416d539382330039393f6f1b0fadce59c4bb1',
        'panoramaIdType': 'panoIndiv',
        'cto_bundle': 'iXBxK19GJTJGa212ZWtTMCUyQklhQkxvOGxGSVRpUEpvUWtsRU1MJTJCJTJCbjNUbCUyQkZYZzBsVGlob0VPUGM5REFzSENpYmxhdWFjbSUyRk43d1dxJTJGVCUyRm9pYkNMeGZZaWVpJTJGNDgyWEVxNmtDWUxab2RwanlpbXdTdnNHZm9neWZkVW5IbE1NSTlLWm5reFNYbW9EQUIwTXdLbndpS3M4UXZCWUI5NkolMkZQbjdVMFNhcDVzYmZBUGVRSlBnV3FvTldxQTBjRENQWXhOMDVBV0ZxSmpMNkFFS0o3a3lVejNoejZ2Y1RQT1VQNE9HNVdUMUZmUDJHeWluV3p1QjlVcTRCeTh0UkkwWGxPR09RSVdaa3BpM0lLZFQ1bzJMOVlqSk1RNWc4QUJZNk8xJTJGMiUyRmRkQXhsNGxTVnZyZnFqMDdFTjNFaUpMNzV1UDBVYUtPcA',
        '_uetsid': 'e2997f30ac3011ef90eacfd60cf552fb',
        '_uetvid': 'e299ab10ac3011efb3bd85d70640e806',
        '_dd_s': 'rum=0&expire=1732762576933',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'RF_BROWSER_ID=V2vhRHVYSw6uwV_MkNqW-Q; RF_BROWSER_ID_GREAT_FIRST_VISIT_TIMESTAMP=2024-11-26T11%3A58%3A51.451746; RF_BID_UPDATED=1; _gcl_au=1.1.772515649.1732651139; __pdst=1ca4844ec1a54f4e9362c9faa4f838e0; _scor_uid=c344b9ebc611452e8a039ba1cdb004df; _pin_unauth=dWlkPVpUaGpZamhsTVdZdE4yVmpPQzAwTUdaakxUZzVZemt0WmpneFkyUXhZakE0TmpFMg; RF_VISITED=true; searchMode=1; sortOrder=1; sortOption=special_blend; _fbp=fb.1.1732651267107.624212160447874825; RF_BUSINESS_MARKET=27; save_search_nudge_flyout=1%251732687110079%25false; RF_MARKET=hamptonroads; unifiedLastSearch=name%3DCoconino%2520County%26subName%3DAZ%252C%2520USA%26url%3D%252Fcounty%252F215%252FAZ%252FCoconino-County%26id%3D5_215%26type%3D5%26unifiedSearchType%3D5%26isSavedSearch%3D%26countryCode%3DUS; RF_MARKET=flagstaff; RF_BROWSER_CAPABILITIES=%7B%22screen-size%22%3A3%2C%22events-touch%22%3Afalse%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%7D; RF_TRAFFIC_SEGMENT=organic; audS=t; FEED_COUNT=%5B%22%22%2C%22f%22%5D; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1877994105.1732761492; OptanonAlertBoxClosed=2024-11-28T02:38:27.527Z; _rdt_uuid=1732651141686.b9bfaab9-ac24-4939-8fcb-2aea8a63eadc; RF_CORVAIR_LAST_VERSION=551.1.0; _ga_928P0PZ00X=GS1.1.1732760987.4.1.1732761508.44.0.0; _ga=GA1.1.397345153.1732651141; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Nov+28+2024+07%3A38%3A29+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4cd1ba09-ff79-49e6-9a63-af530c5b60dd&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=PK%3BPB; userPreferences=parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26viewedSwipeableHomeCardsDate%3D1732761513905; RF_LAST_NAV=0; _ga_P8GPVZXD5S=GS1.1.1732760987.2.0.1732761517.0.0.0; aws-waf-token=2c2b8ed0-1abc-49d3-8eab-043c8d0a8acc:BQoAu4MSVukgAAAA:C13rMc9VviUC+xR/cXKDCBRdnNcdkkDG6L8+eUz4Ui3+DIHscIHNLWy1h8OounOImOWOk/A4tFscy3xbEzb1ckV+R2579Ve/38je79JMmZ12J6Opig8gu67wj4CXPN5SMafm8LBpXdrApsdRb0PRxdR6GV2jjwfsDuX4Xrj7nL8Pb9O1LP1xlKqiJFHaJca7KBQfQAi2UbvTS1+8OBsYURfD3Qeb2bo5NRZ9kWDEXhYEiOgp/cYy75Ahd23RZBVvzQ==; tude-rvn-rel-Mdd5C=1.4.0; cw-test-20241121-viewable-refresh=test; cw-test-20241121-intersection-observer=test; _sharedid=a115397b-14ec-4b40-b6e9-f0952f29b382; _sharedid_cst=VyxHLMwsHQ%3D%3D; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3AzyQdbCbYyw7QuJBJwX-zcmx54XXxMoqRfdBjvfg6yPY5RLPl2oCYYe7G78OlAqvxKjWkAuGfBVGXHw9GdGANziPENoQzsqO2J1URTI0X4WA%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; cto_bidid=vZXNi19WZkN4JTJGaXc4aGhBQ3c5cFcyMnBFM0olMkZhRFVSZERCOEgwJTJGTFR5VVAwcWNuSjBZZVJDVXhNcG45JTJGM0klMkJab3pwRE1LOGxvcmdkellESGFLeW1WVkZtWndqZ2I3VXBNWjFHTnNaMDJaQ3BlOGMlM0Q; _cc_id=ee373f584ba401bf60beac776650005b; panoramaId_expiry=1733366382137; panoramaId=8736f40d6e10207182b10e1aafa416d539382330039393f6f1b0fadce59c4bb1; panoramaIdType=panoIndiv; cto_bundle=iXBxK19GJTJGa212ZWtTMCUyQklhQkxvOGxGSVRpUEpvUWtsRU1MJTJCJTJCbjNUbCUyQkZYZzBsVGlob0VPUGM5REFzSENpYmxhdWFjbSUyRk43d1dxJTJGVCUyRm9pYkNMeGZZaWVpJTJGNDgyWEVxNmtDWUxab2RwanlpbXdTdnNHZm9neWZkVW5IbE1NSTlLWm5reFNYbW9EQUIwTXdLbndpS3M4UXZCWUI5NkolMkZQbjdVMFNhcDVzYmZBUGVRSlBnV3FvTldxQTBjRENQWXhOMDVBV0ZxSmpMNkFFS0o3a3lVejNoejZ2Y1RQT1VQNE9HNVdUMUZmUDJHeWluV3p1QjlVcTRCeTh0UkkwWGxPR09RSVdaa3BpM0lLZFQ1bzJMOVlqSk1RNWc4QUJZNk8xJTJGMiUyRmRkQXhsNGxTVnZyZnFqMDdFTjNFaUpMNzV1UDBVYUtPcA; _uetsid=e2997f30ac3011ef90eacfd60cf552fb; _uetvid=e299ab10ac3011efb3bd85d70640e806; _dd_s=rum=0&expire=1732762576933',
        'priority': 'u=1, i',
        # 'referer': 'https://www.redfin.com/county/215/AZ/Coconino-County/filter/viewport=38.76543:32.29944:-109.66324:-114.44229,no-outline',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    params = {
        'location': f'{search_query}',
        'start': '0',
        'count': '10',
        'v': '2',
        'market': 'hamptonroads',
        'al': '1',
        'iss': 'false',
        'ooa': 'true',
        'mrs': 'false',
        # 'region_id': '2125',
        # 'region_type': '5',
        'lat': '35.63053000000001',
        'lng': '-112.05276500000001',
        'includeAddressInfo': 'false',
    }

    response = requests.get(
        'https://www.redfin.com/stingray/do/location-autocomplete',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    response_json = json.loads(response.content[4:])
    locations = []
    sections = response_json.get("payload", {}).get("sections", [])
    for section in sections:
        rows = section.get("rows", [])
        for row in rows:
            locations.append(row.get("id", "").split('_'))
    if locations.__len__() > 0:
        return locations[0]
    else:
        return ['0', '0000']
