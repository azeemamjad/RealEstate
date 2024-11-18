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
let numberOfForSale = document.getElementById("numberOfForSale");
let numberOfSold = document.getElementById("numberOfSold");

function displayAddresses(
    results
) {
    forSaleAverageDaysOnMarket.innerHTML = results.forSaleAverageDaysOnMarket
    soldAverageDaysOnMarket.innerHTML = results.soldAverageDaysOnMarket
    soldFile.href = results.sold_file_path
    soldRatio.innerHTML = Number.parseFloat(results.soldRatio).toFixed(2)
    numberOfForSale.innerHTML = Number.parseFloat(results.numberOfForSale)
    numberOfSold.innerHTML = Number.parseFloat(results.numberOfSold)
    // Clear previous results
    forSaleResultsDiv.innerHTML = "";
    soldOutResultsDiv.innerHTML = "";


    const forSaleResults = results.search_results.for_sale_results
    let var_7 = 0;
    for (const key in forSaleResults) {
    var_7++;
        if(var_7>100)
        {
            break;
        }
        listing = forSaleResults[key]
        let linkButtons = "";
        let priceRows = "";
        let sizeRows = "";
        let daysOnMarketRows = "";
        let imgRow = ""

        const truncatedName = key;
        listing.forEach((item) => {
            linkButtons += `
            <a href="${item.linkToList}" target="_blank" class="flex items-center justify-center bg-blue-100 text-blue-900 p-2 rounded-full m-1">
            <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6">
            </a>`;
            priceRows += `<p><span class="text-lg font-bold text-green-700 mb-2 flex justify-end">${formatPrice(item.price.toString().replace("$", "").replace(",", ""))} &nbsp;
            <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6"></span></p>`

            sizeRows += `<p class="text-black text-sm">Acres: <span class="font-medium">${item.acres.toFixed(2)} - ${item.marketName}</span></p>`

            daysOnMarketRows += `<p class="text-black">Days on ${item.marketName}: <span class="font-medium">${item.daysOnMarket}</span></p>`

        })

        const addressHTML = `
            <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow">
                <div class="p-5">
                    ${priceRows}
                    <div class="flex justify-between items-center mb-3">
                        <h5 class="text-md font-bold tracking-tight text-gray-900" style="
                            font-family: 'Arial', sans-serif;
                            color: #333;
                            overflow: hidden; 
                            white-space: nowrap;
                            text-overflow: 
                            max-width: 70%; 
                        ">${truncatedName}</h5>
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

    const soldResults = results.search_results.sold_results
    let var_8=0;
    for (const key in soldResults) {
    var_8++;
        if(var_8>100)
        {
            break;
        }
        listing = soldResults[key]
        let linkButtons = "";
        let priceRows = "";
        let sizeRows = "";
        let daysOnMarketRows = "";
        let imgRow = ""
        let soldDate = ""
        const truncatedName = key;
        listing.forEach((item) => {
            linkButtons += `
            <a href="${item.linkToList}" target="_blank" class="flex items-center justify-center bg-blue-100 text-blue-900 p-2 rounded-full m-1">
                <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6">
            </a>`;
            priceRows += `<p><span class="text-lg font-bold text-green-700 mb-2 flex justify-end">${formatPrice(item.soldPrice)}  &nbsp;
                <img src="/static/assets/${item.marketName.toLowerCase()}.png" alt="${item.marketName}" class="w-6 h-6"></span></p>`

            sizeRows += `<p class="text-black text-sm">Acres: <span class="font-medium">${item.acres.toFixed(2)} - ${item.marketName}</span></p>`

            daysOnMarketRows += `<p class="text-black">Days on ${item.marketName}: <span class="font-medium">${item.daysOnMarket}</span></p>`
            soldDate = item.soldDate
        })
        const addressHTML = `
            <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow">
                <div class="p-5">
                    ${priceRows}
                    <div class="flex justify-between items-center mb-3">
                        <h5 class="text-md font-bold tracking-tight text-gray-900" style="
                            font-family: 'Arial', sans-serif;
                            color: #333;
                            overflow: hidden; 
                            white-space: nowrap;
                            text-overflow: 
                            max-width: 70%; 
                        ">${truncatedName}</h5>
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

    // if (filteredAddresses.length === 0) {
    //     forSaleResultsDiv.innerHTML = `<p class="text-red-600 text-center mt-5 flex justify-center">No properties found based on your search criteria.</p>`;
    //     soldOutResultsDiv.innerHTML = `<p class="text-red-600 text-center mt-5 mx-auto">No properties found based on your search criteria.</p>`;
    // }
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