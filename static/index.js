function toggleDropdown(dropdownId, buttonElement) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle("hidden");

    // Toggle event listener based on dropdown visibility
    if (!dropdown.classList.contains("hidden")) {
        document.addEventListener("click", (event) => closeDropdownOnClickOutside(event, dropdown, buttonElement));
    }
}

function closeDropdownOnClickOutside(event, dropdown, button) {
    // Check if the click is outside of the dropdown and button
    if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        dropdown.classList.add("hidden");
        document.removeEventListener("click", closeDropdownOnClickOutside);
    }
}

function showLoader() {

    // Hide the loader
    loader.style.display = 'flex';
}
function hideLoader() {

    // Hide the loader
    loader.style.display = 'none';
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(price);
}


let forSaleResultsDiv = document.getElementById("forSaleResults");
let soldOutResultsDiv = document.getElementById("soldOutResults");
let soldRatio = document.getElementById("soldRatio");
let forSaleAverageDaysOnMarket = document.getElementById("forSaleAverageDaysOnMarket");
let soldAverageDaysOnMarket = document.getElementById("soldAverageDaysOnMarket");
let soldFile = document.getElementById("soldFile");
let detailedReport = document.getElementById("detailedReport");
let numberOfForSale = document.getElementById("numberOfForSale");
let numberOfSold = document.getElementById("numberOfSold");

let forSaleResultsBatch = 0;
let soldResultsBatch = 0;
const BATCH_SIZE = 20; // Load 20 entries at a time
let forSaleResults = [];
let soldResults = [];
let isLoading = false; // Prevent multiple triggers during scroll

function displayAddresses(results) {
    // Initialize global results for infinite scrolling
    forSaleResults = results.search_results.for_sale_results;
    soldResults = results.search_results.sold_results;
    
    forSaleAverageDaysOnMarket.innerHTML = results.forSaleAverageDaysOnMarket
    soldAverageDaysOnMarket.innerHTML = results.soldAverageDaysOnMarket
    soldFile.href = results.sold_file_path
    detailedReport.href = results.excel_ratio_file_path
    soldRatio.innerHTML = Number.parseFloat(results.soldRatio).toFixed(2)
    numberOfForSale.innerHTML = Number.parseFloat(results.numberOfForSale)
    numberOfSold.innerHTML = Number.parseFloat(results.numberOfSold)

    // Clear previous results
    forSaleResultsDiv.innerHTML = "";
    soldOutResultsDiv.innerHTML = "";

    // Load the first batch of data
    loadMoreForSaleResults();
    loadMoreSoldResults();

    // Attach infinite scroll listener
    window.addEventListener("scroll", handleScroll);
}

function loadMoreForSaleResults() {
    if (isLoading) return; // Prevent reloading
    isLoading = true;

    const keys = Object.keys(forSaleResults);
    const startIndex = forSaleResultsBatch * BATCH_SIZE;
    const endIndex = Math.min(startIndex + BATCH_SIZE, keys.length);

    forSaleResultsBatch++;
    for (let i = startIndex; i < endIndex; i++) {
        const key = keys[i];
        const listing = forSaleResults[key];

        let linkButtons = "";
        let priceRows = "";
        let sizeRows = "";
        let daysOnMarketRows = "";
        let imgSrc = "";

        listing.forEach((item) => {
            linkButtons += `
            <a href="${item.linkToList}" target="_blank" class="flex items-center justify-center bg-blue-100 text-blue-900 p-2 rounded-full m-1">
                <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6">
            </a>`;
            priceRows += `<p><span class="text-lg font-bold text-green-700 mb-2 flex justify-end">${formatPrice(item.price.toString().replace("$", "").replace(",", ""))} &nbsp;
                <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6"></span></p>`;
            sizeRows += `<p class="text-black text-sm">Acres: <span class="font-medium">${item.acres.toFixed(2)} - ${item.marketName}</span></p>`;
            daysOnMarketRows += `<p class="text-black">Days on ${item.marketName}: <span class="font-medium">${item.daysOnMarket}</span></p>`;
            imgSrc = item.imgSrc; // Assign card image source
        });

        // Ensure the URL is not modified or encoded unnecessarily
        const imageHTML = imgSrc
            ? `
            <div class="relative">
                <div class="absolute inset-0 flex justify-center items-center bg-gray-200 rounded-t-lg loader-container">
                    <div class="loader"></div>
                </div>
                <img src="${imgSrc}" alt="Google Map Image" class="w-full h-48 object-cover rounded-t-lg" loading="lazy" 
                    onload="this.previousElementSibling.style.display='none';" 
                    onerror="this.previousElementSibling.style.display='none'; this.style.display='none';">
            </div>`
            : "";

        const addressHTML = `
            <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow">
                ${imageHTML}
                <div class="p-5">
                    ${priceRows}
                    <div class="flex justify-between items-center mb-3">
                        <h5 class="text-md font-bold tracking-tight text-gray-900">${key}</h5>
                    </div>
                    ${sizeRows}
                    ${daysOnMarketRows}
                    <div class="mt-3 flex gap-1 justify-center items-center">
                        ${linkButtons}
                    </div>
                </div>
            </div>
        `;
        forSaleResultsDiv.innerHTML += addressHTML;
    }
    isLoading = false;
}

function loadMoreSoldResults() {
    if (isLoading) return; // Prevent reloading
    isLoading = true;

    const keys = Object.keys(soldResults);
    const startIndex = soldResultsBatch * BATCH_SIZE;
    const endIndex = Math.min(startIndex + BATCH_SIZE, keys.length);

    soldResultsBatch++;
    for (let i = startIndex; i < endIndex; i++) {
        const key = keys[i];
        const listing = soldResults[key];

        let linkButtons = "";
        let priceRows = "";
        let sizeRows = "";
        let daysOnMarketRows = "";
        let soldDate = "";
        let imgSrc = "";

        listing.forEach((item) => {
            linkButtons += `
            <a href="${item.linkToList}" target="_blank" class="flex items-center justify-center bg-blue-100 text-blue-900 p-2 rounded-full m-1">
                <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6">
            </a>`;
            priceRows += `<p><span class="text-lg font-bold text-green-700 mb-2 flex justify-end">${formatPrice(item.soldPrice)} &nbsp;
                <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6"></span></p>`;
            sizeRows += `<p class="text-black text-sm">Acres: <span class="font-medium">${item.acres.toFixed(2)} - ${item.marketName}</span></p>`;
            daysOnMarketRows += `<p class="text-black">Days on ${item.marketName}: <span class="font-medium">${item.daysOnMarket}</span></p>`;
            soldDate = item.soldDate;
            imgSrc = item.imgSrc; // Assign card image source
        });

        const imageHTML = imgSrc
            ? `
            <div class="relative">
                <div class="absolute inset-0 flex justify-center items-center bg-gray-200 rounded-t-lg loader-container">
                    <div class="loader"></div>
                </div>
                <img src="${imgSrc}" alt="Google Map Image" class="w-full h-48 object-cover rounded-t-lg" loading="lazy" 
                    onload="this.previousElementSibling.style.display='none';" 
                    onerror="this.previousElementSibling.style.display='none'; this.style.display='none';">
            </div>`
            : "";

        const addressHTML = `
            <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow">
                ${imageHTML}
                <div class="p-5">
                    ${priceRows}
                    <div class="flex justify-between items-center mb-3">
                        <h5 class="text-md font-bold tracking-tight text-gray-900">${key}</h5>
                    </div>
                    ${sizeRows}
                    <p>Sold Date: ${soldDate}</p>
                    ${daysOnMarketRows}
                    <div class="mt-3 flex gap-1 justify-center items-center">
                        ${linkButtons}
                    </div>
                </div>
            </div>
        `;
        soldOutResultsDiv.innerHTML += addressHTML;
    }
    isLoading = false;
}

function handleScroll() {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50 && !isLoading) {
        loadMoreForSaleResults();
        loadMoreSoldResults();
    }
}


function searchAddress() {
    soldRatio.innerHTML = "Not Results";
    forSaleAverageDaysOnMarket.innerHTML = "Not Results";
    soldAverageDaysOnMarket.innerHTML = "Not Results";
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    const minPrice = Number(document.getElementById("minPrice").value) || 0;
    const maxPrice = Number(document.getElementById("maxPrice").value) || 0;
    const maxDaysOnZillow = Number(document.getElementById("maxDaysOnZillow").value) || 0;
    const minLotSize = parseInt(document.getElementById('minLotSize').value, 10) || 0;
    const maxLotSize = parseInt(document.getElementById('maxLotSize').value, 10) || 0;

    if (searchTerm == "") {
        alert("Please input some address.")
        return;
    }

    const selectedWebsites = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.value)
        .join(',');

    showLoader()
    // Prepare the body for the POST request
    const requestBody = {
        "search_term": searchTerm,
        "price_min": minPrice,
        "price_max": maxPrice,
        "days_on_market": parseInt(maxDaysOnZillow),
        "lot_size_min": minLotSize,
        "lot_size_max": maxLotSize,
        "ranges": generateJSON(),
    };

    // Make the POST request
    fetch(`/search?website=${selectedWebsites}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            hideLoader()
            // Assuming data contains the results you want to display
            displayAddresses(data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
hideLoader()

soldRatio.innerHTML = "Not Results";
forSaleAverageDaysOnMarket.innerHTML = "Not Results";
soldAverageDaysOnMarket.innerHTML = "Not Results";
numberOfSold.innerHTML = "Not Results";
numberOfForSale.innerHTML = "Not Results";