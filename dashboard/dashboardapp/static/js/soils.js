const soilTypeSelect = document.getElementById('soil-type');
const propertyCategoryContainer = document.getElementById('property-category-container');
const propertyCategorySelect = document.getElementById('property-category');
const tablesContainer = document.getElementById('tables-container');

// Tables
const basicTable = document.getElementById('basic-table');
const engineeringTable = document.getElementById('engineering-table');
const hydraulicTable = document.getElementById('hydraulic-table');
const settlementTable = document.getElementById('settlement-table');

// Data for table fields based on soil type and category
const tableData = {
    gravel: {
        basic: [
            { property: 'Total unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Dry unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Submerged or Buoyant unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Void ratio', cov: '', r: '', dx: '', dy: '' },
            { property: 'Relative density', cov: '', r: '', dx: '', dy: '' },
        ],
        engineering: [
            { property: 'Angle of internal friction angle', cov: '', r: '', dx: '', dy: '' },
            { property: 'Elastic Modulus', cov: '', r: '', dx: '', dy: '' },
            { property: "Poisson's ratio", cov: '', r: '', dx: '', dy: '' },
        ],
        hydraulic: [
            { property: 'Coefficient of permeability', cov: '', r: '', dx: '', dy: '' }
        ],
    },
    sand: {
        basic: [
            { property: 'Total unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Dry unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Submerged or Buoyant unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Void ratio', cov: '', r: '', dx: '', dy: '' },
            { property: 'Relative density', cov: '', r: '', dx: '', dy: '' },
            { property: 'Natural moisture content', cov: '', r: '', dx: '', dy: '' },
        ],
        engineering: [
            { property: 'Angle of internal friction angle', cov: '', r: '', dx: '', dy: '' },
            { property: 'Tangent of angle of shearing resistance', cov: '', r: '', dx: '', dy: '' },
            { property: 'Elastic Modulus', cov: '', r: '', dx: '', dy: '' },
            { property: "Poisson's ratio", cov: '', r: '', dx: '', dy: '' },
        ],
        hydraulic: [
            { property: 'Coefficient of permeability', cov: '', r: '', dx: '', dy: '' }
        ]
    },
    silt: {
        basic: [
            { property: 'Total unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Dry unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Submerged or Buoyant unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Void ratio', cov: '', r: '', dx: '', dy: '' },
            { property: 'Natural moisture content', cov: '', r: '', dx: '', dy: '' },
            { property: 'Liquid limit', cov: '', r: '', dx: '', dy: '' },
            { property: 'Plastic limit', cov: '', r: '', dx: '', dy: '' },
            { property: 'Plasticity index', cov: '', r: '', dx: '', dy: '' },
            { property: 'Liquidity index', cov: '', r: '', dx: '', dy: '' },
        ],
        engineering: [
            { property: 'Undrained cohesion', cov: '', r: '', dx: '', dy: '' },
            { property: 'Drained angle of internal friction', cov: '', r: '', dx: '', dy: '' },
            { property: 'Drained cohesion strength', cov: '', r: '', dx: '', dy: '' },
            { property: 'Undrained strength ratio', cov: '', r: '', dx: '', dy: '' },
            { property: 'Unconfined compressive strength', cov: '', r: '', dx: '', dy: '' },
        ],
        hydraulic: [
            { property: 'Coefficient of permeability', cov: '', r: '', dx: '', dy: '' }
        ],
        settlement: [
            { property: 'Coefficient of consolidation', cov: '', r: '', dx: '', dy: '' },
            { property: 'Compression index', cov: '', r: '', dx: '', dy: '' },
            { property: 'Over consolidation ratio', cov: '', r: '', dx: '', dy: '' },
        ]
    },
    clay: {
        basic: [
            { property: 'Total unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Dry unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Submerged or Buoyant unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Void ratio', cov: '', r: '', dx: '', dy: '' },
            { property: 'Natural moisture content', cov: '', r: '', dx: '', dy: '' },
            { property: 'Liquid limit', cov: '', r: '', dx: '', dy: '' },
            { property: 'Plastic limit', cov: '', r: '', dx: '', dy: '' },
            { property: 'Plasticity index', cov: '', r: '', dx: '', dy: '' },
            { property: 'Liquidity index', cov: '', r: '', dx: '', dy: '' },
        ],
        engineering: [
            { property: 'Undrained cohesion', cov: '', r: '', dx: '', dy: '' },
            { property: 'Drained angle of internal friction', cov: '', r: '', dx: '', dy: '' },
            { property: 'Drained cohesion strength', cov: '', r: '', dx: '', dy: '' },
            { property: 'Undrained strength ratio', cov: '', r: '', dx: '', dy: '' },
            { property: 'Unconfined compressive strength', cov: '', r: '', dx: '', dy: '' },
            { property: 'Residual friction angle', cov: '', r: '', dx: '', dy: '' },
        ],
        hydraulic: [
            { property: 'Coefficient of permeability', cov: '', r: '', dx: '', dy: '' }
        ],
        settlement: [
            { property: 'Coefficient of consolidation', cov: '', r: '', dx: '', dy: '' },
            { property: 'Compression index', cov: '', r: '', dx: '', dy: '' },
            { property: 'Over consolidation ratio', cov: '', r: '', dx: '', dy: '' },
        ]
    },
    general: {
        basic: [
            { property: 'Total unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Dry unit weight', cov: '', r: '', dx: '', dy: '' },
            { property: 'Submerged unit weight', cov: '', r: '', dx: '', dy: '' },
            {property: 'Natural water content', cov: '', r: '', dx: '', dy: ''  },
            {property: 'Bouyant unit weight',  cov: '', r: '', dx: '', dy: '' },
            { property: 'Void ratio', cov: '', r: '', dx: '', dy: '' },
            {property: 'Specific gravity',  cov: '', r: '', dx: '', dy: '' },
            {property: 'Angle of internal friction',  cov: '', r: '', dx: '', dy: '' },
            {property: 'Cohesion strength',cov: '', r: '', dx: '', dy: ''  },
            { property: 'Elastic Modulus', cov: '', r: '', dx: '', dy: '' },
            { property: "Poisson's ratio", cov: '', r: '', dx: '', dy: '' },
            {property: 'Relative density', cov: '', r: '', dx: '', dy: '' },
            {property: 'Coefficient of permeability', cov: '', r: '', dx: '', dy: '' },
        ]
    }
};

// Hide all tables
function hideAllTables() {
    basicTable.style.display = 'none';
    engineeringTable.style.display = 'none';
    hydraulicTable.style.display = 'none';
    settlementTable.style.display = 'none';
}

// Clear all table contents
function clearAllTableContents() {
    const tables = [basicTable, engineeringTable, hydraulicTable, settlementTable];
    tables.forEach(table => {
        const tbody = table.querySelector('tbody');
        if (tbody) {
            tbody.innerHTML = ''; // Clear all rows
        }
    });
}

// Populate table rows dynamically
function populateTable(table, rows) {
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = ''; // Clear previous rows

    rows.forEach(row => {
        const tr = document.createElement('tr');
        Object.values(row).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// Function to update property category dropdown
function updatePropertyCategories(soilType) {
    propertyCategorySelect.innerHTML = ''; // Reset dropdown

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = '--Select--';
    propertyCategorySelect.appendChild(defaultOption);

    const categories = [
        { value: 'basic', label: 'Basic Properties' },
        { value: 'engineering', label: 'Engineering Properties' },
        { value: 'hydraulic', label: 'Hydraulic Properties' },
    ];

    if (soilType === 'clay' || soilType === 'silt') {
        categories.push({ value: 'settlement', label: 'Settlement Parameters' });
    }

    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.value;
        option.textContent = category.label;
        propertyCategorySelect.appendChild(option);
    });
}

// When soil type changes
soilTypeSelect.addEventListener('change', function () {
    const soilType = soilTypeSelect.value;

    if (soilType) {
        if (soilType === 'general') {
            // Display General Soil table directly
            hideAllTables();
            clearAllTableContents();
            tablesContainer.style.display = 'block';
            populateTable(basicTable, tableData.general.basic);
            basicTable.style.display = 'table';
            propertyCategoryContainer.style.display = 'none'; // Hide category dropdown
        } else {
            propertyCategoryContainer.style.display = 'block';
            updatePropertyCategories(soilType);
            propertyCategorySelect.value = '';
            tablesContainer.style.display = 'none';
            hideAllTables();
            clearAllTableContents();
        }
    } else {
        propertyCategoryContainer.style.display = 'none';
        tablesContainer.style.display = 'none';
        hideAllTables();
        clearAllTableContents();
    }
});

// When property category changes
propertyCategorySelect.addEventListener('change', function () {
    const soilType = soilTypeSelect.value;
    const category = propertyCategorySelect.value;

    hideAllTables();
    clearAllTableContents();

    if (category && tableData[soilType] && tableData[soilType][category]) {
        const rows = tableData[soilType][category];
        tablesContainer.style.display = 'block';

        switch (category) {
            case 'basic':
                populateTable(basicTable, rows);
                basicTable.style.display = 'table';
                break;
            case 'engineering':
                populateTable(engineeringTable, rows);
                engineeringTable.style.display = 'table';
                break;
            case 'hydraulic':
                populateTable(hydraulicTable, rows);
                hydraulicTable.style.display = 'table';
                break;
            case 'settlement':
                populateTable(settlementTable, rows);
                settlementTable.style.display = 'table';
                break;
        }
    } else {
        tablesContainer.style.display = 'none';
    }
});
