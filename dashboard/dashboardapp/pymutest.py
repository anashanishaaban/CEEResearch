from pdf2image import convert_from_path
from markitdown import MarkItDown
import sys
from ExtractTable import ExtractTable
import pandas as pd


print(ExtractTable.VERSION)

api_key = "KCMqQZXjn3QZz9Gd376eK9UYlbxcEvBhxhmmZQ96"

et_sess = ExtractTable(api_key)

usage = et_sess.check_usage()

print(usage)

pdf_location = "/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/080630.pdf"  

table_data = et_sess.process_file(filepath=pdf_location, output_format="df", pages="all")

import pandas as pd

# Accumulate all tables into a single DataFrame
accumulated_data = pd.DataFrame()

for each_table in table_data:
    accumulated_data = pd.concat([accumulated_data, each_table], ignore_index=True)

# Save the accumulated data to an Excel file
output_excel_path = "/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/saved/extracted_tables.xlsx"  # Replace with the desired output path
accumulated_data.to_excel(output_excel_path, index=False)

print(f"Tables extracted and saved to {output_excel_path}")

md = MarkItDown()
result = md.convert("/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/080630.pdf")
print(result.text_content)

with open("results.txt", "a") as myfile:
    myfile.write(result.text_content)
    print("Done")

myfile.close()
