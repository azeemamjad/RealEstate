import math
import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openpyxl import Workbook
from pydantic import BaseModel
from fastapi import FastAPI, Query

from openpyxl.styles import PatternFill

import scrapers.utils
from scrapers.utils import get_data

class SearchData(BaseModel):
    """
    Represents the structure of the input data required by the API.
    """
    search_term: str
    price_max: float = 0
    price_min: float = 0
    lot_size_min: float = 0
    lot_size_max: float = 0
    days_on_market: int = 365
    ranges: list = []

# Initialize the FastAPI app
app = FastAPI(
    title="Real Estate Search API",
    description="An API that mimics the behavior of a real estate search system using the `get_data` function.",
    version="1.0.0"
)


# Mount the 'static' directory to serve static files like CSS, JS, images, etc.

# Create and mount static files directory
UPLOAD_DIR = Path("static/excel")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.curdir, "static")), name="static")

# Set up Jinja2 templates. The templates will be located in the 'templates' directory.
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    This route renders the 'index.html' template from the 'templates' directory.
    """
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home Page"})

@app.post("/search", response_model=dict)
async def search_real_estate(payload: SearchData, website: str = Query('zillow')):
    """
    Real Estate Search Endpoint.
    This endpoint accepts a JSON payload with search criteria for real estate properties
    and processes it using the `get_data` function.
    """

    # try:
        # Convert payload to dictionary
    print(payload)
    input_dict = payload.dict()
    input_dict["for_sale"] = True
    
    # Fetch for sale results
    for_sale_results, for_sale_file_path = get_data(
        search_term=input_dict.get("search_term"),
        for_sale=input_dict.get("for_sale"),
        price_min=input_dict.get("price_min"),
        price_max=input_dict.get("price_max"),
        lot_size_min=input_dict.get("lot_size_min"),
        lot_size_max=input_dict.get("lot_size_max"),
        days_on_market=input_dict.get("days_on_market"),
        ranges=input_dict.get("ranges"),
        website=website.split(","),
    )

    for_sale_day_on_market = [int(result.get("daysOnMarket")) for result in for_sale_results]
    forSaleAverageDaysOnMarket = 0
    if not (len(for_sale_day_on_market)==sum(for_sale_day_on_market)==0):
        forSaleAverageDaysOnMarket = math.ceil(sum(for_sale_day_on_market) / len(for_sale_day_on_market))
    
    # Update for sale flag for sold results
    input_dict["for_sale"] = False
    
    # Fetch sold results
    sold_results, sold_file_path = get_data(
        search_term=input_dict.get("search_term"),
        for_sale=input_dict.get("for_sale"),
        price_min=input_dict.get("price_min"),
        price_max=input_dict.get("price_max"),
        lot_size_min=input_dict.get("lot_size_min"),
        lot_size_max=input_dict.get("lot_size_max"),
        days_on_market=input_dict.get("days_on_market"),
        ranges=input_dict.get("ranges"),
        website=website.split(","),
    )

    sold_day_on_market = [int(result.get("daysOnMarket")) for result in sold_results]

    soldAverageDaysOnMarket = 0
    if not (len(sold_day_on_market)==sum(sold_day_on_market)==0):
        soldAverageDaysOnMarket = math.ceil(sum(sold_day_on_market) / len(sold_day_on_market))


    

    # Combine results
    combined_results = {
        "for_sale_results": {},
        "sold_results": {},
    }
    
    # Process for sale results
    for result in for_sale_results:
        address = result['address']
        if address not in combined_results["for_sale_results"]:
            combined_results["for_sale_results"][address] = []
        combined_results["for_sale_results"][address].append(result)
        
    # Process sold results
    for result in sold_results:
        address = result['address']
        if address not in combined_results["sold_results"]:
            combined_results["sold_results"][address] = []
        combined_results["sold_results"][address].append(result)
        
    # Return the formatted response
    return {
        "status": "success",
        "search_results": combined_results,
        "soldRatio": len(for_sale_results)/len(sold_results) if not (len(sold_day_on_market)==sum(sold_day_on_market)==0) else 0,
        "forSaleAverageDaysOnMarket": forSaleAverageDaysOnMarket,
        "soldAverageDaysOnMarket": soldAverageDaysOnMarket,
        "numberOfForSale": len(for_sale_results),
        "numberOfSold": len(sold_results),
        "for_sale_file_path": for_sale_file_path,
        "sold_file_path": sold_file_path,
        'excel_ratio': scrapers.utils.get_data_for_excel_ratio(combined_results),
        'excel_ratio_file_path': scrapers.utils.generate_properties_ratio_excel(scrapers.utils.get_data_for_excel_ratio(combined_results)),
    }
