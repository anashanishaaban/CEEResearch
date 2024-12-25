console.log("Hi")

const soilTypeSelect = document.getElementById('soil-type');
const propertyCategoryContainer = document.getElementById('property-category-container');
const propertyCategorySelect = document.getElementById('property-category');
const tablesContainer = document.getElementById('tables-container');

// Tables
const basicTable = document.getElementById('basic-table');
const engineeringTable = document.getElementById('engineering-table');
const hydraulicTable = document.getElementById('hydraulic-table');
const settlementTable = document.getElementById('settlement-table');

// Hide all tables
function hideAllTables() {
    basicTable.style.display = 'none';
    engineeringTable.style.display = 'none';
    hydraulicTable.style.display = 'none';
    settlementTable.style.display = 'none';
}

// When soil type changes
soilTypeSelect.addEventListener('change', function () {
    const soilType = soilTypeSelect.value;
    if (soilType) {
        // Show property category dropdown
        propertyCategoryContainer.style.display = 'block';
        // Reset property category and hide tables
        propertyCategorySelect.value = '';
        tablesContainer.style.display = 'none';
        hideAllTables();
    } else {
        // Hide property category and tables if no soil selected
        propertyCategoryContainer.style.display = 'none';
        tablesContainer.style.display = 'none';
        hideAllTables();
    }
});

// When property category changes
propertyCategorySelect.addEventListener('change', function () {
    const category = propertyCategorySelect.value;
    hideAllTables();
    if (category) {
        // Show tables container
        tablesContainer.style.display = 'block';
        
        // Show the corresponding table
        switch (category) {
            case 'basic':
                basicTable.style.display = 'table';
                break;
            case 'engineering':
                engineeringTable.style.display = 'table';
                break;
            case 'hydraulic':
                hydraulicTable.style.display = 'table';
                break;
            case 'settlement':
                settlementTable.style.display = 'table';
                break;
        }
    } else {
        // No category selected, hide tables
        tablesContainer.style.display = 'none';
    }
});
