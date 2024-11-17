import random
import uuid
from typing import List

import pandas as pd
import requests
from datetime import datetime, timezone


def parse_date_sold(timestamp_ms: float) -> str:
    # Convert milliseconds to seconds by dividing by 1000
    timestamp_s = timestamp_ms / 1000
    # Convert to a timezone-aware datetime object in UTC
    date_sold = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
    # Format the date as a string (e.g., "YYYY-MM-DD HH:MM:SS UTC")
    return date_sold.strftime('%Y-%m-%d')


def get_headers() -> dict:
    return {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.zillow.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }


def get_region_list(query: str) -> List[dict]:
    query_params = {
        'q': query,
        'resultTypes': 'allRegion',
        'abKey': '05c27e88-5dbb-498d-bf81-032be478d637',
        'clientId': 'static-search-page'
    }

    response = requests.get(
        'https://www.zillowstatic.com/autocomplete/v3/suggestions',
        headers=get_headers(),
        params=query_params
    )

    if response.ok:
        response_data = response.json()

        results = response_data.get("results", [])
        results = [
            {
                "regionId": result.get("metaData", {}).get("regionId", 0)
            }
            for result in results
        ]
        return results
    return []


def scrape_data(
        current_page: int,
        search_term: str,
        lot_size_min: int,
        lot_size_max: int,
        days_on_zillow: str,
        price_min: int,
        price_max: int,
        for_sale: bool,
):
    cookies = {
        'zguid': f'24|{uuid.uuid4()}',
        'zgsession': f'1|{uuid.uuid4()}',
        '_ga': f'GA1.2.{random.randint(10000000, 99999999)}.{random.randint(1000000000, 9999999999)}',
        'zjs_anonymous_id': f'"{uuid.uuid4()}"',
        'zjs_user_id': 'null',
        'zg_anonymous_id': f'"{uuid.uuid4()}"',
        'pxcts': str(uuid.uuid4()),
        '_pxvid': str(uuid.uuid4()),
        '_gcl_au': f'1.1.{random.randint(1000000000, 9999999999)}.{random.randint(1000000000, 9999999999)}',
        '_scid': str(uuid.uuid4()),
        '_tt_enable_cookie': '1',
        '_ttp': str(uuid.uuid4()),
        '_pin_unauth': str(uuid.uuid4()),
        '_ScCbts': '[]',
        'DoubleClickSession': 'true',
        '_sctr': f'1|{random.randint(1000000000000, 9999999999999)}',
        'FSsampler': str(random.randint(100000000, 999999999)),
        '_gid': f'GA1.2.{random.randint(10000000, 99999999)}.{random.randint(1000000000, 9999999999)}',
        'JSESSIONID': str(uuid.uuid4()),
        '_rdt_uuid': f'{random.randint(1000000000000, 9999999999999)}.{uuid.uuid4()}',
        '_scid_r': str(uuid.uuid4()),
        '_clck': f'nkfqm|{random.randint(1, 10)}|fpp|{random.randint(0, 10)}|{random.randint(1000, 9999)}',
        '_dd_s': f'rum={random.randint(0, 1)}&expire={random.randint(1000000000000, 9999999999999)}',
        'AWSALB': str(uuid.uuid4()),
        'AWSALBCORS': str(uuid.uuid4()),
        '_px3': str(uuid.uuid4()),
        '_uetsid': str(uuid.uuid4()),
        '_uetvid': str(uuid.uuid4()),
        '_clsk': f'1gnyhel|{random.randint(1000000000000, 9999999999999)}|4|0|{random.choice(["f.clarity.ms/collect", "other_url"])}',
        'search': f'6|{random.randint(1000000000, 9999999999)}|rect={random.uniform(-90, 90)},{random.uniform(-180, 180)},{random.uniform(-90, 90)},{random.uniform(-180, 180)}&rid={random.randint(1, 30000)}',
    }

    filter_state = {
        'isAllHomes': {
            'value': True,
        },
        'isApartment': {
            'value': False,
        },
        'isApartmentOrCondo': {
            'value': False,
        },
        'isManufactured': {
            'value': False,
        },
        'isCondo': {
            'value': False,
        },
        'isMultiFamily': {
            'value': False,
        },
        'isTownhouse': {
            'value': False,
        },
        'isSingleFamily': {
            'value': False,
        },
        'sortSelection': {
            'value': 'globalrelevanceex',
        },
    }


    if lot_size_max:
        filter_state.update({
            'lotSize': {
                'min': lot_size_min,
                'max': lot_size_max,
            }
        })

    if days_on_zillow:
        filter_state.update({
            'doz': {
                'value': days_on_zillow,
            },
        })

    if price_max:
        filter_state.update({
            'price': {
                'min': price_min,
                'max': price_max,
            },
        })

    if not for_sale:
        filter_state.update({
            'isRecentlySold': {
                'value': True,
            },
            'isForSaleByAgent': {
                'value': False,
            },
            'isForSaleByOwner': {
                'value': False,
            },
            'isForSaleForeclosure': {
                'value': False,
            },
            "isAuction": {
                "value": False
            },
            "isComingSoon": {
                "value": False
            },
            "isNewConstruction": {
                "value": False
            },
        })

    json_data = {
        'searchQueryState': {
            'pagination': {
                'currentPage': current_page,
            },
            'isMapVisible': True,
            'mapBounds': {
                'west': -180,
                'east': 180,
                'south': -90,
                'north': 90
            },
            'mapZoom': 11,
            'usersSearchTerm': search_term,
            'regionSelection': get_region_list(query=search_term),
            'filterState': filter_state,
            'isListVisible': True,
        },
        'wants': {
            'cat1': [
                'listResults',
                'mapResults',
            ],
            'cat2': [
                'total',
            ],
        },
        'requestId': 22,
        'isDebugRequest': False,
    }

    response = requests.put(
        'https://www.zillow.com/async-create-search-page-state',
        cookies=cookies,
        headers=get_headers(),
        json=json_data
    )

    total_results: List[dict] = []

    is_next_page = False

    if response.ok:
        response_data: dict = response.json()

        is_next_page = response_data.get("cat1", {}).get("searchList", {}).get("pagination", {})
        is_next_page = is_next_page.get("nextUrl", None) if is_next_page else None
        is_next_page = True if is_next_page else False
        results: List[dict] = response_data.get("cat1", {}).get("searchResults", {}).get("listResults", [])
        for result in results:
            res = ({
                    'address': result.get("hdpData").get("homeInfo").get("streetAddress", ""),
                    'zipCode': result.get("addressZipcode", ""),
                    'state': result.get("addressState", ""),
                    'city': result.get("addressCity", ""),
                    'acres': result.get("hdpData", {}).get("homeInfo", {}).get("lotAreaValue", "") 
                            if result.get("hdpData", {}).get("homeInfo", {}).get("lotAreaUnit", "")=="acres" else float(result.get("hdpData", {}).get("homeInfo", {}).get("lotAreaValue", 0))/43560,
                    'linkToList': result.get("detailUrl", ""),
                    "marketName": "Zillow",
                    "hasImage": result.get("hasImage"),
                    "imgSrc": result.get("imgSrc"),
                    'daysOnMarket' : result.get("hdpData", {}).get("homeInfo", {}).get("daysOnZillow", ""),
                    "detailedData": result
                }
            )
            if for_sale:
                res.update({
                    'price': result.get("price", ""),

                })
            else:
                res.update({
                    'soldPrice': result.get("hdpData", {}).get("homeInfo", {}).get("price", ""),
                    'soldDate': parse_date_sold(float(result.get("hdpData", {}).get("homeInfo", {}).get("dateSold", 0))),
                })
            total_results.append(res)

    else:
        print("\n\n\n")

    return total_results, is_next_page


def fetch_data_from_zillow(
        search_term: str,
        lot_size_min: int,
        lot_size_max: int,
        days_on_market: str,
        price_min: int,
        price_max: int,
        for_sale: bool,
):
    print("scraping Zillow")
    user_total_results = []

    user_current_page = 1
    while True:
        current_results, next_page = scrape_data(
            current_page=user_current_page,
            search_term=search_term,
            price_min=price_min,
            price_max=price_max,
            for_sale=for_sale,
            lot_size_max=lot_size_max,
            lot_size_min=lot_size_min,
            days_on_zillow=days_on_market,
        )
        user_current_page = user_current_page + 1
        user_total_results.extend(current_results)
        print(len(user_total_results))
        if not next_page:
            break

    return user_total_results


if __name__ == "__main__":

    total_results = fetch_data_from_zillow(
        search_term="Richmond",
        price_min=0,  # usd
        price_max=0,  # usd
        for_sale=False,  # True/False
        lot_size_max=0,  # sqft
        lot_size_min=0,  # sqft
        days_on_market="12m",  # days
    )

    df = pd.DataFrame(total_results)
    df.to_csv(f'scraped_data_{int(datetime.now().timestamp())}.csv', index=False)
