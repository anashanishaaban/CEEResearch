// Fetch and dynamically populate tables with backend-provided data
function loadClassifiedData() {
    fetch("/process-references")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateTables(data.classified_data);
            } else {
                console.error(data.error);
            }
        })
        .catch(error => console.error("Error fetching classified data:", error));
}

// Populate tables with classified data
function populateTables(classifiedData) {
    const soilTypeSelect = document.getElementById("soil-type");
    const propertyCategorySelect = document.getElementById("property-category");

    // Update dropdown based on classified data
    soilTypeSelect.addEventListener("change", function () {
        const selectedSoilType = soilTypeSelect.value;
        if (selectedSoilType) {
            const categories = Object.keys(classifiedData[selectedSoilType]);
            updatePropertyDropdown(categories);
        }
    });

    propertyCategorySelect.addEventListener("change", function () {
        const selectedSoilType = soilTypeSelect.value;
        const selectedCategory = propertyCategorySelect.value;

        if (selectedCategory && classifiedData[selectedSoilType][selectedCategory]) {
            const rows = classifiedData[selectedSoilType][selectedCategory];
            displayTableRows(selectedCategory, rows);
        }
    });
}

// Update property dropdown
function updatePropertyDropdown(categories) {
    const propertyCategorySelect = document.getElementById("property-category");
    propertyCategorySelect.innerHTML = "<option value=''>--Select--</option>";

    categories.forEach(category => {
        const option = document.createElement("option");
        option.value = category;
        option.textContent = category;
        propertyCategorySelect.appendChild(option);
    });
}

// Display rows in the appropriate table
function displayTableRows(category, rows) {
    const tableMap = {
        basic: document.getElementById("basic-table"),
        engineering: document.getElementById("engineering-table"),
        hydraulic: document.getElementById("hydraulic-table"),
        settlement: document.getElementById("settlement-table"),
    };

    // Clear and populate the selected table
    const table = tableMap[category];
    const tbody = table.querySelector("tbody");
    tbody.innerHTML = ""; // Clear previous rows

    rows.forEach(row => {
        const tr = document.createElement("tr");
        Object.values(row).forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    // Display the table
    table.style.display = "table";
}
