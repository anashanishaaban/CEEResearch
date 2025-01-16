from aryn_sdk.partition import partition_file, table_elem_to_dataframe, draw_with_boxes
from aryn_sdk.config import ArynConfig
import json

with open("/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/references/1_Duncan-2000-Factors-of-safety-and-reliability-in-geotechnical-engineering.pdf", "rb") as f:
   data = partition_file(f, extract_table_structure=True, use_ocr=True, extract_images=True, threshold=0.35, aryn_api_key="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsiZW1sIjoiYW5vb3NoYW5pQHlhaG9vLmNvbSIsImFjdCI6IjM4NjQ5MzM0NDkzNyJ9LCJpYXQiOjE3MzY5NTU1MzV9.W6i3zMyUrCJEoZLht82YFeTdhkQR9yZ-BAO0RFCy31wyHJt_aP29YCcoICEp87TOMj-I_E1xeoUpiLwyiGDdCQ")

# Produce a pandas DataFrame representing one of the extracted tables
table_elements = [elt for elt in data['elements'] if elt['type'] == 'table']
dataframe = table_elem_to_dataframe(table_elements[0])

with open("/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/saved/sample.json", "w") as outfile:
    i = 0
    for elemennt in table_elements:
        dataframe = table_elem_to_dataframe(table_elements[i])
        dataframe_json = dataframe.to_dict()
        json.dump(dataframe_json, outfile)
        i = i+1

