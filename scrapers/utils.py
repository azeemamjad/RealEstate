import statistics
from datetime import datetime
import os
from pathlib import Path
from uuid import uuid4

from numpy.ma.core import empty
from numpy.ma.extras import unique

from scrapers.realtor.realtor_scraper import scrap_realtor_data
from scrapers.land.land_scrapper import fetch_data_land_data
from scrapers.zillow.zillow_scraper import fetch_data_from_zillow
from typing import List, Optional

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule

from collections import defaultdict


def prepare_data(properties_list):
    """Extracts and processes property data to remove duplicates and calculate PPA."""
    unique_entries = set()
    processed_data = []

    for property in properties_list:
        acers = property.get("acres", 0)
        total_price = property.get("price", 0) if property.get("price", 0) else property.get("soldPrice", 0)
        if acers is not None and acers > 0 and total_price is not None:
            ppa = round(float(str(total_price).replace("$", "").replace(",", "").replace("K", "000").replace("C", "") if total_price else 0) / acers, 2)
            entry = (acers, total_price, ppa)

            if entry not in unique_entries:
                unique_entries.add(entry)
                processed_data.append({"Acers": acers, "Price": total_price, "PPA": ppa})

    return sorted(processed_data, key=lambda x: x["Acers"])

def create_excel(ranges: list[dict], data, base_dir="static/excel"):
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
        price = float(price.replace("$", "").replace(",", "").replace("K", "000").replace("C", "") if price else 0)
        ws.append([item["Acers"], price, item["PPA"]])

    # Define color fills for each range condition
    colors = [
        "FF0000",  # Red
        "00FF00",  # Green
        "0000FF",  # Blue
        "FFFF00",  # Yellow
        "FFA500",  # Orange
        "800080",  # Purple
    ]
    fills = [PatternFill(start_color=color, end_color=color, fill_type="solid") for color in colors]

    # Apply conditional formatting based on Acers column for PPA (column C)
    if ranges is not None:
        for i, range_item in enumerate(ranges):
            fill = fills[i % len(fills)]  # Use a new color fill for each range item

            # Condition for "<" (Acers < value)
            if "<" in range_item:
                value = float(range_item["<"]["value"])  # Convert to float for comparison
                for row in range(2, len(data) + 2):  # Start from row 2
                    ws.conditional_formatting.add(
                        f"C{row}",
                        FormulaRule(formula=[f'A{row}<{value}'], fill=fill)
                    )

            # Condition for ">" (Acers > value)
            elif ">" in range_item:
                value = float(range_item[">"]["value"])  # Convert to float for comparison
                for row in range(2, len(data) + 2):  # Start from row 2
                    ws.conditional_formatting.add(
                        f"C{row}",
                        FormulaRule(formula=[f'A{row}>{value}'], fill=fill)
                    )

            # Condition for "ranged" (Acers between start and end)
            elif "ranged" in range_item:
                start = float(range_item["ranged"]["start"])
                end = float(range_item["ranged"]["end"])
                for row in range(2, len(data) + 2):  # Start from row 2
                    ws.conditional_formatting.add(
                        f"C{row}",
                        FormulaRule(formula=[f'AND(A{row}>={start}, A{row}<={end})'], fill=fill)
                    )

    # Append extra information at the end
    ws.append([])  # Empty row for separation

    if ranges is not None:
        for i, range_ in enumerate(ranges):
            if "<" in range_:
                value = float(range_["<"]["value"])
                prices = [float(x['PPA']) for x in data if float(x['Acers']) < value]
                if prices:
                    median = round(statistics.median(prices), 3)
                    median50 = round(median * 0.50, 3)
                    median75 = round(median * 0.75, 3)
                    ws.append([f'Less Than {int(value)} Acers'])
                    ws.append([f'{median}', 'Median PPA'])
                    ws.append([f'{median50}', '50%'])
                    ws.append([f'{median75}', '75%'])
                else:
                    ws.append([f'Less Than {int(value)} Acers'])
                    ws.append([f'0', 'Median PPA'])
                    ws.append([f'0', '50%'])
                    ws.append([f'0', '75%'])
            elif ">" in range_:
                value = float(range_[">"]["value"])
                prices = [float(x['PPA']) for x in data if float(x['Acers']) > value]
                if prices:
                    median = round(statistics.median(prices), 3)
                    median50 = round(median * 0.50, 3)
                    median75 = round(median * 0.75, 3)
                    ws.append([f'Greater Than {int(value)} Acers'])
                    ws.append([f'{median}', 'Median PPA'])
                    ws.append([f'{median50}', '50%'])
                    ws.append([f'{median75}', '75%'])
                else:
                    ws.append([f'Less Than {int(value)} Acers'])
                    ws.append([f'0', 'Median PPA'])
                    ws.append([f'0', '50%'])
                    ws.append([f'0', '75%'])
            elif "ranged" in range_:
                start = float(range_["ranged"]["start"])
                end = float(range_["ranged"]["end"])
                prices = [float(x['PPA']) for x in data if end >= float(x['Acers']) >= start]
                if prices:
                    median = round(statistics.median(prices), 3)
                    median50 = round(median * 0.50, 3)
                    median75 = round(median * 0.75, 3)
                    ws.append([f'Between {int(start)}-{int(end)} Acers'])
                    ws.append([f'{median}', 'Median PPA'])
                    ws.append([f'{median50}', '50%'])
                    ws.append([f'{median75}', '75%'])
                else:
                    ws.append([f'Less Than {int(value)} Acers'])
                    ws.append([f'0', 'Median PPA'])
                    ws.append([f'0', '50%'])
                    ws.append([f'0', '75%'])
            else:
                continue

    fill_index = 0
    for i in range(len(data) + 3, ((len(ranges) * 4) + 1 + len(data) + 2) , 4):
        fill = fills[fill_index % len(fills)]
        ws.conditional_formatting.add(
            f"A{i}",
            FormulaRule(formula=[f'1=1'], fill=fill)
        )
        fill_index += 1

    ws.append([])
    if data:
        ws.append(["Total Properties", len(data)])
        total_price = sum(round(float(str(item["Price"]).replace("$", "").replace(",", "").replace("K", "000").replace("C", "") if item['Price'] else 0), 3)  for item in data)
        ws.append(["Total Price", total_price])
        avg_price = total_price / len(data) if len(data) > 0 else 0
        ws.append(["Average Price", avg_price])
        min_price = min(round(float(str(item["Price"]).replace("$", "").replace(",", "").replace("K", "000").replace("C", "") if item['Price'] else 0), 3) for item in data)
        ws.append(["Min Price", min_price])
        max_price = max(round(float(str(item["Price"]).replace("$", "").replace(",", "").replace("K", "000").replace("C", "") if item['Price'] else 0), 3) for item in data)
        ws.append(["Max Price", max_price])

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
    ranges: list[dict],
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
    file_path = create_excel(ranges=ranges,data=processed_data)
    
    return total_results, file_path

def get_data_for_excel_ratio(properties_data):
    for_sale_results = properties_data.get("for_sale_results", {})
    sold_results = properties_data.get("sold_results", {})

    # Step 1: Separate data by marketName
    market_data = defaultdict(lambda: defaultdict(lambda: {
        "for_sale_count": 0,
        "sold_count": 0,
        "zip_codes": defaultdict(lambda: {"for_sale_count": 0, "sold_count": 0})
    }))

    # Process for_sale_results
    for address, properties in for_sale_results.items():
        for prop in properties:
            market_name = prop["marketName"]
            if market_name.lower() == "zillow":
                market_key = "Zillow"
            elif market_name.lower() == "realtor":
                market_key = "Realtor"
            elif market_name.lower() == "land":
                market_key = "Land"
            else:
                continue

            county = prop["county"]
            zip_code = prop["zipCode"]
            market_data[market_key][county]["for_sale_count"] += 1
            market_data[market_key][county]["zip_codes"][zip_code]["for_sale_count"] += 1

    # Process sold_results
    for address, properties in sold_results.items():
        for prop in properties:
            market_name = prop["marketName"]
            if market_name.lower() == "zillow":
                market_key = "Zillow"
            elif market_name.lower() == "realtor":
                market_key = "Realtor"
            elif market_name.lower() == "land":
                market_key = "Land"
            else:
                continue

            county = prop["county"]
            zip_code = prop["zipCode"]
            market_data[market_key][county]["sold_count"] += 1
            market_data[market_key][county]["zip_codes"][zip_code]["sold_count"] += 1

    # Step 2: Create output structure
    result = []
    for market_name, county_data in market_data.items():
        market_summary = {"marketName": market_name, "counties": []}
        for county, details in county_data.items():
            county_summary = {
                "county": county,
                f"{market_name.lower()}_for_sale_count": details["for_sale_count"],
                f"{market_name.lower()}_sold_count": details["sold_count"],
                "zip_codes": []
            }
            for zip_code, counts in details["zip_codes"].items():
                county_summary["zip_codes"].append({
                    "zip_code": zip_code,
                    f"{market_name.lower()}_for_sale_count": counts["for_sale_count"],
                    f"{market_name.lower()}_sold_count": counts["sold_count"]
                })
            market_summary["counties"].append(county_summary)
        result.append(market_summary)

    return result


def generate_properties_ratio_excel(excel_ratio, base_dir="static/excel"):
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid4())[:8]
    filename = f"property_ratio_{timestamp}_{unique_id}.xlsx"
    file_path = os.path.join(base_dir, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Property Data"

    # Define headers based on your specified structure
    headers = [
        "County / Zipcode",
        "Zillow For Sale Property $40k-1M",
        "Zillow For Sold Property - 12 mos. on market $40k-1M",
        "For Sale/ Sold Ratio (Zillow)",
        "DOM For Sale (Zillow)",
        "DOM Sold (Zillow)",
        "Realtor For Sale Property $40k-1M",
        "Realtor For Sold Property - Recently sold on market $40K-1M",
        "For Sale/ Sold Ratio (Realtor)",
        "DOM Sold (Realtor)",
        "Land For Sale Property $40k-1M",
        "Land For Sold Property - Recently sold on market $40K-1M",
        "For Sale/ Sold Ratio (Land)"
    ]
    ws.append(headers)

    # Loop through the provided excel_ratio data and add to the sheet
    for market_data in excel_ratio:
        market_name = market_data["marketName"]
        for county_data in market_data["counties"]:
            county_name = county_data["county"]
            # Add county data to the first row
            row_data = [county_name]

            # Market-specific logic for data (Zillow, Realtor, Land)
            for market_type in ["Zillow", "Realtor", "Land"]:
                for_sale_count = county_data.get(f"{market_type.lower()}_for_sale_count", 0)
                sold_count = county_data.get(f"{market_type.lower()}_sold_count", 0)
                ratio = f"{for_sale_count / sold_count:.2f}" if sold_count > 0 else "N/A"
                dom_for_sale = "N/A"  # Placeholder for future implementation
                dom_sold = "N/A"  # Placeholder for future implementation

                row_data.extend([for_sale_count, sold_count, ratio, dom_for_sale, dom_sold])

            # Append county data to sheet
            ws.append(row_data)
    for market_data in excel_ratio:
        for county_data in market_data["counties"]:
            county_name = county_data["county"]
            # Add county data to the first row
            row_data = [county_name]

            # Append county data to sheet
            ws.append(row_data)

            # Now add zip code data under the county
            for zip_code_data in county_data["zip_codes"]:
                zip_code = zip_code_data["zip_code"]
                zip_row_data = [f"{zip_code}"]  # Add county name with zip

                # Repeat market-specific logic for zip codes
                for market_type in ["Zillow", "Realtor", "Land"]:
                    for_sale_count = zip_code_data.get(f"{market_type.lower()}_for_sale_count", 0)
                    sold_count = zip_code_data.get(f"{market_type.lower()}_sold_count", 0)
                    ratio = f"{for_sale_count / sold_count:.2f}" if sold_count > 0 else "N/A"
                    dom_for_sale = "N/A"  # Placeholder for future implementation
                    dom_sold = "N/A"  # Placeholder for future implementation

                    zip_row_data.extend([for_sale_count, sold_count, ratio, dom_for_sale, dom_sold])

                # Append zip code row to sheet
                ws.append(zip_row_data)

    # Save the workbook
    os.makedirs(base_dir, exist_ok=True)
    wb.save(file_path)

    return file_path




