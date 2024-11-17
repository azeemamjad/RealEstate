import urllib.parse
from datetime import datetime, timedelta
from typing import List
from typing import Optional

import pandas as pd
import requests


listed_filters = [
    "day",
    "week",
    "month",
    "2-months"
]


def search_query_parser(search_query: str) -> Optional[str]:
    headers_ = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'priority': 'u=1, i',
        'referer': 'https://www.land.com/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    encoded_search_query = urllib.parse.quote(search_query)

    response = requests.get(
        f'https://www.land.com/api/location/autocomplete/0/{encoded_search_query}',
        headers=headers_
    )
    if response.ok:
        response_data = response.json()
        if response_data:
            return response_data[0].get("searchPath", "")


def get_days_on_market(date_string):
    # Check if microseconds are present by looking for a dot in the time part
    if '.' in date_string:
        # Parse with microseconds
        parsed_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        # Parse without microseconds
        parsed_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
    days_on_market = (datetime.now() - parsed_date).days
    return days_on_market


def get_date_on_market(sales_date):
    days_on_market = get_days_on_market(sales_date)

    # Use the returned integer directly to compute the date
    current_date = datetime.now()
    date_on_market = current_date - timedelta(days=days_on_market)  # Should be an integer

    return date_on_market.date()


headers = {
    'sec-ch-ua-platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
}


def scrape_data_from_url(url: str, for_sale: bool):
    response = requests.get(
        url,
        headers=headers,
    )
    fetched_data = response.json()
    property_results: List[dict] = fetched_data.get("searchResults", {}).get("propertyResults", [])
    final_results: List[dict] = []
    for property_ in property_results:
        result = (
            {
                'address': property_.get("address", ""),
                'zipCode': property_.get("zip", ""),
                'state': property_.get("state", ""),
                'county': property_.get("county", ""),
                'city': property_.get("city", ""),
                'acres': property_.get("acres", ""),
                'linkToList': f'https://www.land.com{property_.get("canonicalUrl", "")}',
                "marketName": "Lands",
                "detailedData": property_,
                "hasImage": property_.get("thumbnailDocumentId")!=None,
                "imgSrc": f"https://assets.land.com/resizedimages/600/0/h/80/w/1-{property_.get('thumbnailDocumentId')}",
                'daysOnMarket': f'{get_days_on_market(property_.get("insertDate", ""))}',
            }
        )
        if for_sale:
            result.update({
                'price': property_.get("price", ""),
            })
        else:
            result.update({
                'soldPrice': property_.get("price", ""),
                'soldDate': get_date_on_market(property_.get("salesDate", ""))
            })
        final_results.append(result)
    next_page = fetched_data.get("searchResults", {}).get("paginationData", {}).get("nextLink", "")
    next_page = "https://www.land.com/api/property/search/0" + next_page if next_page else ""
    return final_results, next_page


def fetch_data_land_data(
        search_query: str,
        price_min: int,
        price_max: int,
        acre_min: int,
        acre_max: int,
        days_on_market: int,
        for_sale: bool,
):
    print("scraping Land")
    temp = str
    if days_on_market == 1:
        temp = listed_filters[0]
    elif days_on_market <= 7:
        temp = listed_filters[1]
    elif days_on_market <=30:
        temp = listed_filters[2]
    else:
        temp = listed_filters[3]
    days_on_market = temp
    search_query = search_query_parser(search_query=search_query)
    if not search_query:
        return []

    price_range = ""
    if price_min and price_max:
        price_range = f"/{price_min}-{price_max}"
    elif price_max:
        price_range = f"/under-{price_max}"
    elif price_min:
        price_range = f"/over-{price_min}"

    acre_range = ""
    if acre_min and acre_max:
        acre_range = f"/{acre_min}-{acre_max}-acres"
    elif acre_max:
        acre_range = f"/under-{acre_max}-acres"
    elif acre_min:
        acre_range = f"/over-{acre_min}-acres"

    if days_on_market and days_on_market in listed_filters:
        listed = f"/listed-last-{days_on_market}"
    else:
        listed = ""

    is_under_contract = f"/is-under-contract" if not for_sale else ""
    is_sold = "/is-sold" if not for_sale else ""
    is_active = "/is-active" if for_sale and (is_under_contract or is_sold) else ""
    final_url = f'https://www.land.com/api/property/search/0/{search_query}/all-land/no-house{price_range}{acre_range}{listed}{is_active}{is_under_contract}{is_sold}/'
    total_results = []
    page = 1
    try:
        while final_url:
            print(f"Page : {page}")
            page += 1
            final_results, final_url = scrape_data_from_url(final_url, for_sale)
            total_results.extend(final_results)
    except:
        pass
    return total_results


if __name__ == "__main__":
    properties_data = fetch_data_land_data(
        search_query="Colorado", # eg. "new york"
        price_max=200000, # eg. 250000
        price_min=5000, # eg. 5000
        acre_max=50,  # eg. 60
        acre_min=2,  # eg. 2
        days_on_market=1,   # listed_filters[0]("day") listed_filters[1]("week") listed_filters[4]("month") listed_filters[3]("2month")
        for_sale=False,    # True / False
    )
    df = pd.DataFrame(properties_data)
    df.to_csv("output.csv")

