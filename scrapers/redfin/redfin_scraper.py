from datetime import datetime, timezone

import requests
import json

import pandas as pd

cities_data = pd.read_excel("scrapers/zillow/datasets/uscities.xlsx")

def get_county_by_city(city_name, cities_data=''):
    """
    Load the data and return the county name for a given city.

    :param file_path: Path to the Excel or CSV file containing the data.
    :param city_name: Name of the city to look up.
    :return: County name as a string or an empty string if the city is not found.
    """
    try:
        # Load the data
        data = cities_data

        # Filter the data to find the city
        city_row = data[data['city_ascii'].str.lower() == city_name.lower()]

        # Check if the city exists and return the county name, or an empty string
        if not city_row.empty:
            return city_row['county_name'].values[0]
        else:
            return "County Not Found" # Return empty string if city not found
    except Exception as e:
        # Handle any exceptions and log them
        print(e)
        return "County Not Found"

def convert_seconds_to_days(seconds):
    """
    Converts the 'value' in the given time_data dictionary from seconds to days.

    :param time_data: A dictionary with a 'value' key representing seconds.
    :return: The number of days as a float.
    """
    days = seconds / (24 * 60 * 60)  # Convert seconds to days
    return round(days, 2)

def parse_date_sold(timestamp_ms: float) -> str:
    # Convert milliseconds to seconds by dividing by 1000
    timestamp_s = timestamp_ms / 1000
    # Convert to a timezone-aware datetime object in UTC
    date_sold = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
    # Format the date as a string (e.g., "YYYY-MM-DD HH:MM:SS UTC")
    return date_sold.strftime('%Y-%m-%d')

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
    if len(locations) > 5:
        return locations[:5]
    else:
        return locations


def fetch_data_from_redfin(
        search_term: str,
        lot_size_min: int,
        lot_size_max: int,
        days_on_market: str,
        price_min: int,
        price_max: int,
        for_sale: bool,
        cities_data: cities_data
):
    cookies = {
        'RF_BROWSER_ID': 'V2vhRHVYSw6uwV_MkNqW-Q',
        'RF_BROWSER_ID_GREAT_FIRST_VISIT_TIMESTAMP': '2024-11-26T11%3A58%3A51.451746',
        'RF_BID_UPDATED': '1',
        '_gcl_au': '1.1.772515649.1732651139',
        '__pdst': '1ca4844ec1a54f4e9362c9faa4f838e0',
        'AMP_TOKEN': '%24NOT_FOUND',
        '_gid': 'GA1.2.1319959066.1732651144',
        '_scor_uid': 'c344b9ebc611452e8a039ba1cdb004df',
        '_pin_unauth': 'dWlkPVpUaGpZamhsTVdZdE4yVmpPQzAwTUdaakxUZzVZemt0WmpneFkyUXhZakE0TmpFMg',
        'RF_VISITED': 'true',
        'searchMode': '1',
        'sortOrder': '1',
        'sortOption': 'special_blend',
        '_fbp': 'fb.1.1732651267107.624212160447874825',
        'RF_LAST_NAV': '0',
        'RF_MARKET': 'hamptonroads',
        'RF_BROWSER_CAPABILITIES': '%7B%22screen-size%22%3A3%2C%22events-touch%22%3Afalse%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%7D',
        'RF_BUSINESS_MARKET': '27',
        'OptanonAlertBoxClosed': '2024-11-26T20:14:31.990Z',
        'RF_CORVAIR_LAST_VERSION': '550.4.1',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Nov+27+2024+01%3A14%3A33+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4cd1ba09-ff79-49e6-9a63-af530c5b60dd&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=PK%3BPB',
        '_rdt_uuid': '1732651141686.b9bfaab9-ac24-4939-8fcb-2aea8a63eadc',
        '_ga_928P0PZ00X': 'GS1.1.1732651140.1.1.1732652074.60.0.0',
        '_ga': 'GA1.1.397345153.1732651141',
        'userPreferences': 'parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26viewedSwipeableHomeCardsDate%3D1732652075452',
        '_ga_P8GPVZXD5S': 'GS1.1.1732651417.1.1.1732652076.0.0.0',
        'aws-waf-token': '497568a3-acd3-4b54-bd8f-7dc0855f90ef:BQoAhVONKdYRAAAA:4ug1uHTX7N2BXSkohCzMarFqLxMEP43T/K1CM7fSUxkViNixbhvuXS/4iZFTq0H26gdBI+vAzIj+nx70tFncrIWxwqzpAiL/LUqrdchpZulQYtswngb8uOLaHNDRRGzzce/gCZeT1fImGyknqcGdpHIsRaBXEcCMkeCIHE9MIXB8mUsZ0lE6QEZ78NbA/gVeAfglPQpwltJmW0NEfYDkvbD1hU74SzBTmYlrNa5eSPLOBOhwbwG0Enr76KTwPpcBDw==',
        '_uetsid': 'e2997f30ac3011ef90eacfd60cf552fb',
        '_uetvid': 'e299ab10ac3011efb3bd85d70640e806',
        '_dd_s': 'rum=0&expire=1732653250738',
        # 'unifiedLastSearch': 'name%3DLos%2520Angeles%26subName%3DLos%2520Angeles%252C%2520CA%252C%2520USA%26url%3D%252Fcity%252F11203%252FCA%252FLos-Angeles%26id%3D2_11203%26type%3D2%26unifiedSearchType%3D2%26isSavedSearch%3D%26countryCode%3DUS',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'RF_BROWSER_ID=V2vhRHVYSw6uwV_MkNqW-Q; RF_BROWSER_ID_GREAT_FIRST_VISIT_TIMESTAMP=2024-11-26T11%3A58%3A51.451746; RF_BID_UPDATED=1; _gcl_au=1.1.772515649.1732651139; __pdst=1ca4844ec1a54f4e9362c9faa4f838e0; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1319959066.1732651144; _scor_uid=c344b9ebc611452e8a039ba1cdb004df; _pin_unauth=dWlkPVpUaGpZamhsTVdZdE4yVmpPQzAwTUdaakxUZzVZemt0WmpneFkyUXhZakE0TmpFMg; RF_VISITED=true; searchMode=1; sortOrder=1; sortOption=special_blend; _fbp=fb.1.1732651267107.624212160447874825; RF_LAST_NAV=0; RF_MARKET=hamptonroads; RF_BROWSER_CAPABILITIES=%7B%22screen-size%22%3A3%2C%22events-touch%22%3Afalse%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%7D; RF_BUSINESS_MARKET=27; OptanonAlertBoxClosed=2024-11-26T20:14:31.990Z; RF_CORVAIR_LAST_VERSION=550.4.1; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+27+2024+01%3A14%3A33+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4cd1ba09-ff79-49e6-9a63-af530c5b60dd&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=PK%3BPB; _rdt_uuid=1732651141686.b9bfaab9-ac24-4939-8fcb-2aea8a63eadc; _ga_928P0PZ00X=GS1.1.1732651140.1.1.1732652074.60.0.0; _ga=GA1.1.397345153.1732651141; userPreferences=parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26viewedSwipeableHomeCardsDate%3D1732652075452; _ga_P8GPVZXD5S=GS1.1.1732651417.1.1.1732652076.0.0.0; aws-waf-token=497568a3-acd3-4b54-bd8f-7dc0855f90ef:BQoAhVONKdYRAAAA:4ug1uHTX7N2BXSkohCzMarFqLxMEP43T/K1CM7fSUxkViNixbhvuXS/4iZFTq0H26gdBI+vAzIj+nx70tFncrIWxwqzpAiL/LUqrdchpZulQYtswngb8uOLaHNDRRGzzce/gCZeT1fImGyknqcGdpHIsRaBXEcCMkeCIHE9MIXB8mUsZ0lE6QEZ78NbA/gVeAfglPQpwltJmW0NEfYDkvbD1hU74SzBTmYlrNa5eSPLOBOhwbwG0Enr76KTwPpcBDw==; _uetsid=e2997f30ac3011ef90eacfd60cf552fb; _uetvid=e299ab10ac3011efb3bd85d70640e806; _dd_s=rum=0&expire=1732653250738; unifiedLastSearch=name%3DLos%2520Angeles%26subName%3DLos%2520Angeles%252C%2520CA%252C%2520USA%26url%3D%252Fcity%252F11203%252FCA%252FLos-Angeles%26id%3D2_11203%26type%3D2%26unifiedSearchType%3D2%26isSavedSearch%3D%26countryCode%3DUS',
        'priority': 'u=1, i',
        # 'referer': 'https://www.redfin.com/city/20418/VA/Virginia-Beach/filter/viewport=37.15872:36.36218:-75.74925:-76.34663,no-outline',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    params = {
        "al": "1",
        # "include_nearby_homes": "false",
        # "market": "hamptonroads",

        # 'max_price': '8000000',
        # 'min_price': '125000',

        # "max_parcel_size": "4356000",
        # "min_parcel_size": "8000",

        "mpt": "99",
        "num_homes": "30000",
        # "ord": "redfin-recommended-asc",
        "page_number": "1",

        # "sf": "1,2,3,5,6,7",
        # "start": "0",
        # "status": "9",
        # "time_on_market_range": "3-",
        # 'sold_within_days': '90',

        "uipt": "5",
        "v": "8"
    }

    data = []


    for region in get_regional_data(search_term):
        # setting region
        region_type, region_id = region
        params.update({'region_id':f'{region_id}', 'region_type': f'{region_type}'})

        print(region_id, region_type)

        # for sale or sold? days on market?
        if for_sale:
            if days_on_market:
                params.update({'time_on_market_range':f'{days_on_market}_'})
        else:
            if days_on_market:
                params.update({'sold_within_days': f'{days_on_market}'})
            else:
                params.update({'sold_within_days': '7'}) # necessary to get for sold data

        # price
        if price_max:
            params.update({'max_price': f'{price_max}'})
        if price_min:
            params.update({'min_price': f'{price_min}'})

        # acres
        if lot_size_min:
            params.update({'min_parcel_size': f'{lot_size_min*43560}'})
        if lot_size_max:
            params.update({'max_parcel_size': f'{lot_size_max * 43560}'})



        # Make the GET request
        response = requests.get(
            "https://www.redfin.com/stingray/api/gis",
            headers=headers,
            cookies=cookies,
            params=params
        )
        response_json = json.loads(response.content[4:])
        homes = response_json.get("payload", {}).get("homes", [])
        homes.extend(response_json.get("payload", {}).get("originalHomes", {}).get("homes", []))
        for home in homes:
            datum = {}
            datum.update(
                {
                    'address': f'{home.get("streetLine", {}).get("value", "")}, {home.get("city", "")}, {home.get("state", "")} {home.get("zip", "")}',
                    'zipCode': f'{home.get("zip", "")}',
                    'state': f'{home.get("state", "")}',
                    'county': f'{get_county_by_city(city_name=home.get('city', ""), cities_data=cities_data)}',
                    'city': f'{home.get('city', "")}',
                    'acres': f'{round(home.get("lotSize", {}).get("value", 0)/43560, 3)}',
                    'linkToList': f'https://www.redfin.com{home.get("url", "")}',
                    'marketName': 'Redfin',
                })
            if for_sale:
                datum.update({
                    'daysOnMarket': f'{convert_seconds_to_days(home.get("timeOnRedfin", {}).get("value", 0))}',
                    'price': f'{home.get("price", {}).get("value", 0)}',
                })
            else:
                datum.update({
                    'soldPrice': f'{home.get("price", {}).get("value", 0)}',
                    'soldDate': f'{parse_date_sold(home.get("soldDate", 0))}'
                })
            data.append(datum)

    print(len(data))
    return data

if __name__ == "__main__":
    data = fetch_data_from_redfin(
            search_term="Virginia",
            price_min=0,  # usd
            price_max=0,  # usd
            for_sale=True,  # True/False
            lot_size_max=0,  # sqft
            lot_size_min=0,  # sqft
            days_on_market="",  # days
            cities_data=cities_data,
        )

    print(len(data))