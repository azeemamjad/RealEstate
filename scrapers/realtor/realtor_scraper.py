from datetime import datetime, timezone, timedelta
from typing import List


import requests

def get_days_on_market(date_str):
        # Parse the date string into a timezone-aware datetime object
        parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        # Get the current date and time in UTC, timezone-aware
        current_date = datetime.now(timezone.utc)
        # Calculate the difference in days
        delta = current_date - parsed_date
        # Return the number of days
        return delta.days


def get_date_on_market(days_on_market):
        # Get the current date in UTC
        current_date = datetime.now(timezone.utc).date()  # Get only the date part

        # Calculate the date on market by subtracting days_on_market from current_date
        date_on_market = current_date - timedelta(days=days_on_market)

        # Return the date in YYYY-MM-DD format
        return date_on_market.isoformat()


def get_properties_data(json_response: dict, for_sale: bool) -> List[dict]:
        if json_response.get("data"):
                properties : List[dict] = json_response.get("data", {}).get("home_search", {}).get("properties", [])
                results : List[dict] = []
                for property_ in properties:
                        result = {
                                'address' : property_.get("location", {}).get("address", {}).get("line", "") if property_.get("location", {}).get("county", {}) else "",
                                'state' : property_.get("location", {}).get("address", {}).get("state", "") if property_.get("location", {}).get("county", {}) else "",
                                'county' : property_.get("location", {}).get("county", {}).get("name", "") if property_.get("location", {}).get("county", {}) else "",
                                'city' : property_.get("location", {}).get("address", {}).get("city", "") if property_.get("location", {}).get("address", {}) else "",
                                'zipCode' : property_.get("location", {}).get("address", {}).get("postal_code", "") if property_.get("location", {}).get("address", {}) else "",
                                'acres' : round(float(property_.get("description", {}).get("lot_sqft", 0)) / 43560, 2) if property_.get("description", {}).get("lot_sqft") else None,
                                "marketName": "Realtor",
                                "hasImage": property_.get("primary_photo")!=None,
                                "imgSrc": property_.get("primary_photo").get("href") if property_.get("primary_photo") else None,
                                'daysOnMarket' : get_days_on_market(property_.get("list_date", "")),
                                "detailedData": property_
                        }
                        if for_sale:
                                result.update({
                                        'price': property_.get("list_price"),
                                })
                        else:
                                result.update({
                                        "soldPrice": property_.get("description", {}).get("sold_price", ""),
                                        "soldDate" : property_.get("description", {}).get("sold_date", ""),
                                })

                        result.update({
                                'linkToList': f"https://www.realtor.com/realestateandhomes-detail/{property_.get("permalink", "")}",
                        })

                        results.append(result)
                return results
        return []

def scrap_realtor_data(search_query: str,
                       price_min: int,
                       price_max: int,
                       lot_area_min: float,
                       lot_area_max: float,
                       for_sale: bool,
                       days_on_market: int,
                       ):
        print("scraping Realtor")

        cookies = {
                'split': 'n',
                '__vst': 'aa589f4b-a0a2-412b-a5aa-b5a0bdfcd59b',
                '__ssn': '56ce7015-1d0c-4f55-bfdc-9ac28f3e7c3f',
                '__ssnstarttime': '1728385877',
                '__bot': 'false',
                'isAuth0EnabledOnGnav': 'C1',
                '__split': '62',
                '_lr_env_src_ats': 'false',
                'G_ENABLED_IDPS': 'google',
                's_ecid': 'MCMID%7C89846725839295072570747248804457502038',
                'AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg': '1',
                'mdLogger': 'false',
                'kampyle_userid': '428f-4740-4dab-c658-3b22-9804-3b81-0310',
                'kampyleUserSession': '1728385883149',
                'kampyleUserSessionsCount': '1',
                'srchID': '4e4242bdaa224667975c8c367ad98b55',
                'kampyleUserPercentile': '2.2132827759527407',
                'criteria': 'sprefix%3D%252Fnewhomecommunities%26area_type%3Dcity%26city%3DWilmington%26pg%3D1%26state_code%3DNC%26state_id%3DNC%26loc%3DWilmington%252C%2520NC%26locSlug%3DWilmington_NC',
                'split_tcv': '182',
                'AMCV_8853394255142B6A0A4C98A4%40AdobeOrg': '-1124106680%7CMCIDTS%7C20005%7CMCMID%7C89846725839295072570747248804457502038%7CMCAID%7CNONE%7CMCOPTOUT-1728396491s%7CNONE%7CvVersion%7C5.2.0',
                'kampyleSessionPageCounter': '9',
        }

        headers = {
                'accept': 'application/json, text/javascript',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                # 'cookie': 'split=n; split_tcv=177; __vst=73337a6a-9092-4a16-b602-6c31bb3da60a; __ssn=37021017-263d-4511-b5a4-74abcebbdfba; __ssnstarttime=1728349882; __bot=false; isAuth0EnabledOnGnav=C1; _lr_env_src_ats=false; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; __split=95; permutive-id=3725c1cf-3660-41e7-a965-efeffe9f03c5; _pbjs_userid_consent_data=3524755945110770; s_ecid=MCMID%7C34001635615924350711663768626827774154; _cq_duid=1.1728349886.tD79oW59CzuctSr7; _cq_suid=1.1728349886.iUhkPkS0LUw423wh; _gcl_au=1.1.269079072.1728349887; _scid=yqLUKHjuiSDR0GsHck6huL-3kKLuyiV5; pxcts=3e008a08-8512-11ef-87b7-96a865695d86; _pxvid=3e007510-8512-11ef-87b7-237b5da02deb; G_ENABLED_IDPS=google; _fbp=fb.1.1728349887558.218810944365316409; _tac=false~self|not-available; _ta=us~1~89df68bc35032d48c293adce8574aa42; _ScCbts=%5B%5D; _tt_enable_cookie=1; _ttp=FBwrjLns6dxw_Aq5InPAd0zT0YA; _ncg_id_=1bab6c09-ceaa-456a-b319-c76340c25eb2; AMCVS_AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=1; _sctr=1%7C1728345600000; _lr_sampling_rate=100; __qca=P0-2043241693-1728349886543; _ncg_domain_id_=1bab6c09-ceaa-456a-b319-c76340c25eb2.1.1728349888349.1791421888349; _ncg_g_id_=3ebfb539-bebe-4c9d-9b8b-3924ac70d802.3.1728349890.1791421888349; ajs_anonymous_id=cfd9ea6c-ca11-4619-8bb1-201d84143b23; _gid=GA1.2.158004334.1728349892; mdLogger=false; kampyle_userid=4dae-8cfc-4df2-b512-9291-3c37-63e2-fea1; panoramaId_expiry=1728436929214; _cc_id=ee373f584ba401bf60beac776650005b; panoramaId=34c53f7cc4dce5208444e96d0bc1a9fb927a6cdc5e054fe3a9d8b81618a211dc; _lr_retry_request=true; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Aed49bc87-6806-006e-744b-2fe2a926e96a%7Ce%3Aundefined%7Cc%3A1728349886794%7Cl%3A1728380041071; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Avisitor_73337a6a-9092-4a16-b602-6c31bb3da60a%7Ce%3Aundefined%7Cc%3A1728349886785%7Cl%3A1728380041073; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C20005%7CMCMID%7C34001635615924350711663768626827774154%7CMCAAMLH-1728984844%7C3%7CMCAAMB-1728984844%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1728387244s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; _ncg_sp_ses.cc72=*; _tas=2wg0jlpij3n; AMCV_AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCMID%7C34001635615924350711663768626827774154%7CMCIDTS%7C20005%7CMCOPTOUT-1728387260s%7CNONE%7CvVersion%7C5.2.0; adcloud={%22_les_v%22:%22c%2Cy%2Crealtor.com%2C1728381860%22}; __gsas=ID=a9a33e4be1d73931:T=1728380536:RT=1728380536:S=ALNI_ManA0eXllbW_AmONYz_cU6mMChhcA; kampyleUserSession=1728380588824; kampyleUserSessionsCount=5; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3A354f2c0d-7d64-d4cb-cc45-4908edfdb6b9%7Ce%3A1728382637237%7Cc%3A1728380041070%7Cl%3A1728380837237; srchID=3376c057aae148e598241b3c5561e196; criteria=sprefix%3D%252Fnewhomecommunities%26area_type%3Dcity%26city%3DWilmington%26pg%3D1%26state_code%3DNC%26state_id%3DNC%26loc%3DWilmington%252C%2520NC%26locSlug%3DWilmington_NC%26county_fips%3D37129%26county_fips_multi%3D37129; _ncg_sp_id.cc72=1bab6c09-ceaa-456a-b319-c76340c25eb2.1728349888.2.1728380932.1728351221.0ad9f599-4d08-4973-be74-bfa9b161c473; cto_bundle=ao4aMV9JaXZIcEdxWmxsbWI4aGpySXZ5JTJGSzkwRmpKWEVlakdFSG8zQ0RrckR2cyUyRk9wT3g1QjhRZEx5REZvZXFzajhudFNURVpnTVlGJTJCUXc0MFUzTHJCZWElMkIlMkZFMnZ4dEgyNnA2am9FOXZodGV3UFdLYWxQVmE0a20xamFkVVhyMWt5ZllxJTJGM0t0R1N6WkN3cTJndTJMRUk1V1ElM0QlM0Q; cto_bundle=ao4aMV9JaXZIcEdxWmxsbWI4aGpySXZ5JTJGSzkwRmpKWEVlakdFSG8zQ0RrckR2cyUyRk9wT3g1QjhRZEx5REZvZXFzajhudFNURVpnTVlGJTJCUXc0MFUzTHJCZWElMkIlMkZFMnZ4dEgyNnA2am9FOXZodGV3UFdLYWxQVmE0a20xamFkVVhyMWt5ZllxJTJGM0t0R1N6WkN3cTJndTJMRUk1V1ElM0QlM0Q; _rdt_uuid=1728349886897.fa58487f-0dda-4fd7-a138-17bdfee1115f; _scid_r=ySLUKHjuiSDR0GsHck6huL-3kKLuyiV5PTa-_Q; cto_bundle=ZlpeIF95VEFPUElvR25UOW1DSlU5eFNwaml0ZTlza001aVQzaFhMZzBhM2R5NW9YVXFMcTFxQXFHSnVJVFIybGhhbzR2eU5XelRTVGE2cDA1MjZjMHAwayUyRiUyRnV4NUF1JTJCbHVXNHIzJTJGcVczbEVMMEpKWXk4UlVEWFZ4JTJGVVJZOGpqSlU2YSUyRmdwNlo4Q01jdGptTmNnaCUyQmxoeDlCdyUzRCUzRA; _ga=GA1.2.119667990.1728349888; kampyleUserPercentile=68.7859883338004; leadid_token-27789EFE-7A9A-DB70-BB9B-97D9B7057DBB-01836014-7527-FD48-9B7F-1A40A9705CFE=4B53CE9E-8A6D-C42F-090D-9F0C1722BA8B; __gads=ID=220852d2303c9ee2:T=1728349886:RT=1728381504:S=ALNI_MYzT1AhbDLDNtgRUNRjZYKGCLuB8w; __gpi=UID=00000f2cf8f0b691:T=1728349886:RT=1728381504:S=ALNI_Mai-l3txZKNcDekVbCcPVgN5FsmwQ; __eoi=ID=0823af2422c7156c:T=1728349886:RT=1728381504:S=AA-AfjYZ7I8_eLZZt78y4P3iUyMl; _px3=35308f250fc911936282a0bbfa3751373042c300f5e5b0dbe4baf0e506e53b18:097ePnXgth4CupoZJws2FQnq2MCOhzJ9tmdyHWnnLduP2zHKNlhh0piU/T0zbykNEnqEbPXi5gE0FaXj8cWK2A==:1000:6t1ngt37MStWWO1psWKsEhp5O2CpblwmtqTBjdTD+Mpuy9UtihuzBvZSLyKvD7LRLzyJa7L9MrkonakAJOCWcnw4dPfk/j/4TLkR49bV5Yp/jnxg/Cbue+sXCPj/Y1ejiQ8mAav3wZOaHu26Bxqu84024Mhe+psJoLgcBVaAzuyZ9Sx317PrNrsSkzuaD/cXvIqza8pdiV8pztPX86LWtas50zKcc+BIQ/2tugz0Aj8=; _gat=1; _uetsid=417667e0851211efa8469da08c5c522f|1ajvmbe|2|fpu|0|1742; _uetvid=41767420851211efacf431f4513337af|y40h9t|1728381704153|11|1|bat.bing.com/p/insights/c/p; kampyleSessionPageCounter=8; _ga_MS5EHT6J6V=GS1.1.1728380054.2.1.1728381732.0.0.0',
                'origin': 'https://www.realtor.com',
                'priority': 'u=1, i',
                'rdc-ab-test-client': 'rdc-search-for-sale',
                'rdc-ab-tests': 'commute_travel_time_variation:v1',
                'referer': 'https://www.realtor.com/realestateandhomes-search/Wilmington_NC/type-land/price-120000-1200000',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            }

        params = {
                'client_id': 'rdc-search-for-sale-search',
                'schema': 'vesta',
            }

        query = {
                        'unique': True,
                        'search_location': {
                                'location': search_query,
                                'buffer': 20,
                        },
                        'type': [
                                'land',
                        ],
                }
        # status
        status = []
        if for_sale:
                if days_on_market:
                        list_date = get_date_on_market(days_on_market)
                        query.update({'list_date':{'min':list_date}})
                list_price = {}
                if price_max:
                        list_price.update({"max": price_max})
                if price_min:
                        list_price.update({"min": price_min})
                if list_price:
                        query.update({"list_price": list_price})
                status = ['for_sale',
                          'ready_to_build',
                          ]
                query.update({"status":status})
        else:
                if days_on_market:
                        sold_date = get_date_on_market(days_on_market)
                        query.update({'sold_date':{'min':sold_date}})
                sold_price = {}
                if price_max:
                        sold_price.update({"max": price_max})
                if price_min:
                        sold_price.update({"min": price_min})
                if sold_price:
                        query.update({"sold_price": sold_price})
                status = [
                        'sold',
                ]
        if status:
                query.update({"status": status})

        # lot area range
        lot_sqft = {}
        if lot_area_min:
                lot_sqft.update({"min" : int(lot_area_min*43560)})
        if lot_area_max:
                lot_sqft.update({"max" : int(lot_area_max*43560)})
        if lot_sqft:
                query.update({"lot_sqft" : lot_sqft})



        json_data = {
                'query': '\n  query ConsumerSearchQuery(\n    $query: HomeSearchCriteria!\n    $limit: Int\n    $offset: Int\n    $search_promotion: SearchPromotionInput\n    $sort: [SearchAPISort]\n    $sort_type: SearchSortType\n    $client_data: JSON\n    $bucket: SearchAPIBucket\n    $mortgage_params: MortgageParamsInput\n  ) {\n    home_search: home_search(\n      query: $query\n      sort: $sort\n      limit: $limit\n      offset: $offset\n      sort_type: $sort_type\n      client_data: $client_data\n      bucket: $bucket\n      search_promotion: $search_promotion\n      mortgage_params: $mortgage_params\n    ) {\n      count\n      total\n      search_promotion {\n        names\n        slots\n        promoted_properties {\n          id\n          from_other_page\n        }\n      }\n      mortgage_params {\n        interest_rate\n      }\n      properties: results {\n        property_id\n        list_price\n        search_promotions {\n          name\n          asset_id\n        }\n        primary_photo(https: true) {\n          href\n        }\n        rent_to_own {\n          right_to_purchase\n          rent\n        }\n        listing_id\n        matterport\n        virtual_tours {\n          href\n          type\n        }\n        status\n        products {\n          products\n          brand_name\n        }\n        source {\n          id\n          type\n          spec_id\n          plan_id\n          agents {\n            office_name\n          }\n        }\n        lead_attributes {\n          show_contact_an_agent\n          opcity_lead_attributes {\n            cashback_enabled\n            flip_the_market_enabled\n          }\n          lead_type\n          ready_connect_mortgage {\n            show_contact_a_lender\n            show_veterans_united\n          }\n        }\n        community {\n          description {\n            name\n          }\n          property_id\n          permalink\n          advertisers {\n            office {\n              hours\n              phones {\n                type\n                number\n                primary\n                trackable\n              }\n            }\n          }\n          promotions {\n            description\n            href\n            headline\n          }\n        }\n        permalink\n        price_reduced_amount\n        description {\n          name\n          beds\n          baths_consolidated\n          sqft\n          lot_sqft\n          baths_max\n          baths_min\n          beds_min\n          beds_max\n          sqft_min\n          sqft_max\n          type\n          sub_type\n          sold_price\n          sold_date\n        }\n        location {\n          street_view_url\n          address {\n            line\n            postal_code\n            state\n            state_code\n            city\n            coordinate {\n              lat\n              lon\n            }\n          }\n          county {\n            name\n            fips_code\n          }\n        }\n        open_houses {\n          start_date\n          end_date\n        }\n        branding {\n          type\n          name\n          photo\n        }\n        flags {\n          is_coming_soon\n          is_new_listing(days: 14)\n          is_price_reduced(days: 30)\n          is_foreclosure\n          is_new_construction\n          is_pending\n          is_contingent\n        }\n        list_date\n        photos(limit: 2, https: true) {\n          href\n        }\n        advertisers {\n          type\n          builder {\n            name\n            href\n            logo\n          }\n        }\n      }\n    }\n\n    commute_polygon: get_commute_polygon(query: $query) {\n      areas {\n        id\n        breakpoints {\n          width\n          height\n          zoom\n        }\n        radius\n        center {\n          lat\n          lng\n        }\n      }\n      boundary\n    }\n  }\n',
                'variables': {
                        'geoSupportedSlug': 'Wilmington_NC',
                        'query': query,
                        'client_data': {
                                'device_data': {
                                        'device_type': 'desktop',
                                },
                        },
                        'limit': 42,
                        'offset': 0,
                        'sort_type': 'relevant',
                        'search_promotion': {
                                'names': [
                                        'CITY',
                                ],
                                'slots': [
                                        5,
                                        6,
                                        7,
                                        8,
                                ],
                                'promoted_properties': [
                                        [],
                                ],
                        },
                },
                'isClient': True,
                'visitor_id': 'aa589f4b-a0a2-412b-a5aa-b5a0bdfcd59b',
                'operationName': 'ConsumerSearchQuery',
        }
        response = requests.post(
                'https://www.realtor.com/api/v1/rdc_search_srp',
                params=params,
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
        properties_data: List[dict] = get_properties_data(response.json(), for_sale=for_sale)
        return properties_data
if __name__ == "__main__":
        print(
                scrap_realtor_data(
                search_query='Virginia',
                price_min=0,
                price_max=0,
                for_sale=True,
                lot_area_max=0,
                lot_area_min=10,
                days_on_market=200)
        )