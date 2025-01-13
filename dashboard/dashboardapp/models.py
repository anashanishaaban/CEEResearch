import pdfplumber
import json
import csv


# Path to your PDF file
pdf_path = "/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/references/1_Duncan-2000-Factors-of-safety-and-reliability-in-geotechnical-engineering.pdf"
output_csv_path = "/Users/anasshaaban/ResearchProject/final.csv"

# Open the PDF
with pdfplumber.open(pdf_path) as pdf:
    # Extract the desired page (change the index as needed)
    page = pdf.pages[1]
    
    # Extract the table
    table = page.extract_table()

    # Save the table as a CSV file
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write rows to the CSV
        for row in table:
            csv_writer.writerow(row)

print(f"Table extracted and saved as CSV to {output_csv_path}")
