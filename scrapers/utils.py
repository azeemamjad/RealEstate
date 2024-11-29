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
from scrapers.redfin.redfin_scraper import fetch_data_from_redfin
from typing import List, Optional

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import PatternFill, Border, Side, Alignment
from datetime import datetime
from uuid import uuid4
import os
from itertools import cycle

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
    if "redfin" in website:
        redfin_data = fetch_data_from_redfin(
            search_term=search_term,
            for_sale=for_sale,
            price_min=price_min,
            price_max=price_max,
            lot_size_min=lot_size_min,
            lot_size_max=lot_size_max,
            days_on_market=str(days_on_market) if days_on_market != 0 else "",
        )
        total_results.extend(redfin_data)
        
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
            elif market_name.lower() == "lands":
                market_key = "Lands"
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
            elif market_name.lower() == "lands":
                market_key = "Lands"
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


def generate_properties_ratio_excel(excel_ratio, state, base_dir="static/excel"):
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid4())[:8]
    filename = f"{state}_{timestamp}_{unique_id}.xlsx"
    file_path = os.path.join(base_dir, filename)

    # Create workbook and set active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Property Data"

    # Define headers
    headers = [
        "County",
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
        "For Sale/ Sold Ratio (Land)",
    ]
    ws.append(headers)

    # Apply header styles (colors and borders)
    zillow_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")  # Red
    realtor_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow
    land_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")  # Green
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    for col_index, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_index, value=header)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if "Zillow" in header:
            cell.fill = zillow_fill
        elif "Realtor" in header:
            cell.fill = realtor_fill
        elif "Land" in header:
            cell.fill = land_fill
        cell.border = thin_border

    # Populate rows with data
    for market_data in excel_ratio:
        for county_data in market_data["counties"]:
            county_name = county_data["county"]
            row_data = [county_name]

            # Populate Zillow, Realtor, and Land data for counties
            for market_type in ["zillow", "realtor", "lands"]:
                for_sale_count = county_data.get(f"{market_type}_for_sale_count", 0)
                sold_count = county_data.get(f"{market_type}_sold_count", 0)
                ratio = float(f"{for_sale_count / sold_count:.2f}") if sold_count > 0 else 0
                dom_for_sale = county_data.get(f"{market_type}_dom_for_sale", "N/A")
                dom_sold = county_data.get(f"{market_type}_dom_sold", "N/A")
                if market_type == "zillow":
                    row_data.extend([for_sale_count, sold_count, ratio, dom_for_sale, dom_sold])
                elif market_type == "realtor":
                    row_data.extend([for_sale_count, sold_count, ratio, dom_sold])
                else:
                    row_data.extend([for_sale_count, sold_count, ratio])

            # Ensure data matches headers
            ws.append(row_data[:len(headers)])

    ws.append([])
    ws.append([])

    for market_data in excel_ratio:
        for county_data in market_data["counties"]:
            county_name = county_data["county"]
            zip_row_data_ = [county_name]
            ws.append(zip_row_data_)
            # Process ZIP code data for the county
            for zip_code_data in county_data.get("zip_codes", []):
                zip_code = zip_code_data.get("zip_code", "Unknown ZIP")
                zip_row_data = [f"  {zip_code}"]  # Indent ZIP codes for clarity

                for market_type in ["zillow", "realtor", "lands"]:
                    for_sale_count = zip_code_data.get(f"{market_type}_for_sale_count", 0)
                    sold_count = zip_code_data.get(f"{market_type}_sold_count", 0)
                    ratio = float(f"{for_sale_count / sold_count:.2f}") if sold_count > 0 else 0
                    dom_for_sale = zip_code_data.get(f"{market_type}_dom_for_sale", "N/A")
                    dom_sold = zip_code_data.get(f"{market_type}_dom_sold", "N/A")
                    if market_type == "zillow":
                        zip_row_data.extend([for_sale_count, sold_count, ratio, dom_for_sale, dom_sold])
                    elif market_type == "realtor":
                        zip_row_data.extend([for_sale_count, sold_count, ratio, dom_sold])
                    else:
                        zip_row_data.extend([for_sale_count, sold_count, ratio])

                # Ensure ZIP data matches headers
                ws.append(zip_row_data[:len(headers)])

    # Conditional formatting for ratio columns
    ratio_columns = [4, 9, 13]  # Indices for ratio columns

    # Define color fills
    fill_light_red = PatternFill(start_color="FFA07A", end_color="FFA07A", fill_type="solid")  # Light Red
    fill_green = PatternFill(start_color="008000", end_color="008000", fill_type="solid")  # Green
    fill_yellow = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow

    # Apply conditional formatting
    for col in ratio_columns:
        column_letter = chr(64 + col)  # Convert column index to letter

        ws.conditional_formatting.add(
            f"{column_letter}2:{column_letter}1048576",
            CellIsRule(operator="lessThan", formula=["0.75"], fill=fill_yellow)
        )

        # Green for values between 0.75 and 1.5
        ws.conditional_formatting.add(
            f"{column_letter}2:{column_letter}1048576",
            CellIsRule(operator="between", formula=["0.75", "1.5"], fill=fill_green)
        )

        # Light Red for values greater than 1.75
        ws.conditional_formatting.add(
            f"{column_letter}2:{column_letter}1048576",
            CellIsRule(operator="greaterThan", formula=["1.5"], fill=fill_yellow)
        )


    # Adjust column widths and enable text wrapping
    for column_cells in ws.columns:
        max_length = 10
        column = column_cells[0].column_letter  # Get column letter
        adjusted_width = max_length + 2  # Add padding
        ws.column_dimensions[column].width = adjusted_width
    ws.column_dimensions["A"].width = 25

    # Freeze panes for better readability
    ws.freeze_panes = "A2"

    # Apply alternating row colors
    row_fill_cycle = cycle([
        PatternFill(start_color="F9F9F9", end_color="F9F9F9", fill_type="solid"),  # Light gray
        PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")   # White
    ])
    for row_index, row_cells in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row), start=2):
        fill = next(row_fill_cycle)
        for cell in row_cells:
            cell.fill = fill

    # Save the workbook
    os.makedirs(base_dir, exist_ok=True)
    wb.save(file_path)

    return file_path



