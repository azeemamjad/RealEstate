import statistics
from collections import defaultdict
from datetime import datetime
import os
from pathlib import Path
from uuid import uuid4

from numpy.ma.core import empty

from scrapers.realtor.realtor_scraper import scrap_realtor_data
from scrapers.land.land_scrapper import fetch_data_land_data
from scrapers.zillow.zillow_scraper import fetch_data_from_zillow
from typing import List, Optional

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule


def prepare_data(properties_list):
    """Extracts and processes property data to remove duplicates and calculate PPA."""
    unique_entries = set()
    processed_data = []

    for property in properties_list:
        acers = property.get("acres", 0)
        total_price = property.get("price", 0) if property.get("price", 0) else property.get("soldPrice", 0)
        if acers is not None and acers > 0 and total_price is not None:
            ppa = round(float(str(total_price).replace("$", "").replace(",", "").replace("K", "000") if total_price else 0) / acers, 2)
            entry = (acers, total_price, ppa)
            if entry not in unique_entries:
                unique_entries.add(entry)
                processed_data.append({"Acers": acers, "Price": total_price, "PPA": ppa})

    return sorted(processed_data, key=lambda x: x["Acers"])

def create_excel(data, base_dir="static/excel"):
    """
    Creates an Excel workbook and adds property data with conditional formatting
    based on custom ranges provided by the user.

    Args:
        ranges: List of range dictionaries for conditional formatting.
        data: List of property dictionaries.
        base_dir: Base directory for storing Excel files.

    Returns:
        str: Relative path to the generated Excel file.
    """
    # Create directory if it doesn't exist
    Path(base_dir).mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid4())[:8]
    filename = f"property_data_{timestamp}_{unique_id}.xlsx"
    file_path = os.path.join(base_dir, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Property Data"

    # Append headers
    headers = ["Acers", "Price", "PPA"]
    ws.append(headers)

    # Append data, ensuring that Price is handled correctly
    for item in data:
        price = item["Price"]
        price = str(price) if isinstance(price, (int, float)) else price
        price = float(price.replace("$", "").replace(",", "").replace("K", "000") if price else 0)
        ws.append([item["Acers"], price, item["PPA"]])

    ws.append([])

    # Save the workbook
    wb.save(file_path)

    # Return relative path
    return file_path

# Example usage in your get_data function:
def get_data(
    search_term: str,
    for_sale: bool,
    price_min: int,
    price_max: int,
    lot_size_min: int,
    lot_size_max: int,
    days_on_market: int,
    website: Optional[List[str]] = None,
):
    total_results = []

    if "zillow" in website:
        zillow_data = fetch_data_from_zillow(
            search_term=search_term,
            for_sale=for_sale,
            price_min=price_min,
            price_max=price_max,
            lot_size_min=lot_size_min,
            lot_size_max=lot_size_max,
            days_on_market=str(days_on_market),
        )
        total_results.extend(zillow_data)

    if "land" in website:
        land_data = fetch_data_land_data(
            search_query=search_term,
            for_sale=for_sale,
            price_min=price_min,
            price_max=price_max,
            acre_min=lot_size_min,
            acre_max=lot_size_max,
            days_on_market=days_on_market,
        )
        total_results.extend(land_data)

    if "realtor" in website:
        realtor_data = scrap_realtor_data(
            search_query=search_term,
            for_sale=for_sale,
            price_min=price_min,
            price_max=price_max,
            lot_area_min=lot_size_min,
            lot_area_max=lot_size_max,
            days_on_market=days_on_market,
        )
        total_results.extend(realtor_data)
        
    # Process the data and create Excel file
    processed_data = prepare_data(total_results)
    file_path = create_excel(data=processed_data)
    
    return total_results, file_path

def calculate_sale_ratio_with_website(*data_lists):
    # Initialize dictionaries to store counts, websites, and ratios by platform for cities and zip codes
    city_sale_count = defaultdict(lambda: {'forsalezillow': 0, 'forsoldzillow': 0,
                                           'forsaleland': 0, 'forsoldland': 0,
                                           'forsalerealtor': 0, 'forsoldrealtor': 0})
    zip_sale_count = defaultdict(lambda: {'forsalezillow': 0, 'forsoldzillow': 0,
                                          'forsaleland': 0, 'forsoldland': 0,
                                          'forsalerealtor': 0, 'forsoldrealtor': 0})

    # Process each list of properties
    for data in data_lists:
        for property in data:
            # Extract relevant information from each property
            city = property.get('city')
            zip_code = property.get('zip_code')
            website = property.get('website')  # Assumes website is included
            for_sale = property.get('for_sale', False)  # Default to False if not specified

            # Determine which platform the property came from
            if website == 'zillow':
                platform_prefix = 'zillow'
            elif website == 'land_data':
                platform_prefix = 'land'
            elif website == 'realtor':
                platform_prefix = 'realtor'
            else:
                continue  # Skip if the website is not recognized

            # Update counts based on for_sale status
            if for_sale:
                city_sale_count[city][f'forsale{platform_prefix}'] += 1
                zip_sale_count[zip_code][f'forsale{platform_prefix}'] += 1
            else:
                city_sale_count[city][f'sold{platform_prefix}'] += 1
                zip_sale_count[zip_code][f'sold{platform_prefix}'] += 1

    # Prepare the final structure with cities and zip codes, including ratios
    result = {
        "cities": [],
        "zipcodes": []
    }

    # Process cities
    for city, counts in city_sale_count.items():
        city_data = {
            "city": city,
            "forsalezillow": counts['forsalezillow'],
            "forsoldzillow": counts['forsoldzillow'],
            "ratiozillow": (counts['forsalezillow'] / counts['forsoldzillow'] if counts['forsoldzillow'] != 0 else float('inf')),
            "forsaleland": counts['forsaleland'],
            "forsoldland": counts['forsoldland'],
            "ratioland": (counts['forsaleland'] / counts['forsoldland'] if counts['forsoldland'] != 0 else float('inf')),
            "forsalerealtor": counts['forsalerealtor'],
            "forsoldrealtor": counts['forsoldrealtor'],
            "ratiorealtor": (counts['forsalerealtor'] / counts['forsoldrealtor'] if counts['forsoldrealtor'] != 0 else float('inf'))
        }
        result['cities'].append(city_data)

    # Process zip codes
    for zip_code, counts in zip_sale_count.items():
        zip_data = {
            "zip_code": zip_code,
            "forsalezillow": counts['forsalezillow'],
            "forsoldzillow": counts['forsoldzillow'],
            "ratiozillow": (counts['forsalezillow'] / counts['forsoldzillow'] if counts['forsoldzillow'] != 0 else float('inf')),
            "forsaleland": counts['forsaleland'],
            "forsoldland": counts['forsoldland'],
            "ratioland": (counts['forsaleland'] / counts['forsoldland'] if counts['forsoldland'] != 0 else float('inf')),
            "forsalerealtor": counts['forsalerealtor'],
            "forsoldrealtor": counts['forsoldrealtor'],
            "ratiorealtor": (counts['forsalerealtor'] / counts['forsoldrealtor'] if counts['forsoldrealtor'] != 0 else float('inf'))
        }
        result['zipcodes'].append(zip_data)

    return result

def create_excel_ratio(
    search_term: str,
    price_min: int,
    price_max: int,
    lot_size_min: int,
    lot_size_max: int,
    days_on_market: int
):
    zillow_for_sale = fetch_data_from_zillow(
        search_term=search_term,
        for_sale=True,
        price_min=price_min,
        price_max=price_max,
        lot_size_min=lot_size_min,
        lot_size_max=lot_size_max,
        days_on_market=str(days_on_market),
    )
    zillow_for_sold = fetch_data_from_zillow(
        search_term=search_term,
        for_sale=False,
        price_min=price_min,
        price_max=price_max,
        lot_size_min=lot_size_min,
        lot_size_max=lot_size_max,
        days_on_market=str(days_on_market),
    )
    land_for_sale = fetch_data_land_data(
        search_query=search_term,
        for_sale=True,
        price_min=price_min,
        price_max=price_max,
        acre_min=lot_size_min,
        acre_max=lot_size_max,
        days_on_market=days_on_market,
    )
    land_for_sold = fetch_data_land_data(
        search_query=search_term,
        for_sale=False,
        price_min=price_min,
        price_max=price_max,
        acre_min=lot_size_min,
        acre_max=lot_size_max,
        days_on_market=days_on_market,
    )
    realtor_for_sale = scrap_realtor_data(
        search_query=search_term,
        for_sale=True,
        price_min=price_min,
        price_max=price_max,
        lot_area_min=lot_size_min,
        lot_area_max=lot_size_max,
        days_on_market=days_on_market,
    )
    realtor_for_sold = scrap_realtor_data(
        search_query=search_term,
        for_sale=False,
        price_min=price_min,
        price_max=price_max,
        lot_area_min=lot_size_min,
        lot_area_max=lot_size_max,
        days_on_market=days_on_market,
    )

    output = calculate_sale_ratio_with_website(zillow_for_sale, zillow_for_sold,
    land_for_sale, land_for_sold,
    realtor_for_sale, realtor_for_sold)

    print(output)




    ...

create_excel_ratio(
                search_term='Virginia',
                price_min=0,
                price_max=0,
                lot_size_max=10,
                lot_size_min=0,
                days_on_market=200
)