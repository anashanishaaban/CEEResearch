from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import redirect, render
from django.http import HttpResponse
import os
from openai import OpenAI
import pandas as pd
import json
from pdf2image import convert_from_path
from markitdown import MarkItDown
from ExtractTable import ExtractTable

client = OpenAI()

# ExtractTable API key
EXTRACT_TABLE_API_KEY = "KCMqQZXjn3QZz9Gd376eK9UYlbxcEvBhxhmmZQ96"
et_sess = ExtractTable(EXTRACT_TABLE_API_KEY)

def index(request):
    """
    Render the main page for uploading and visualizing point clouds.
    """
    return render(request, 'index.html')

def soils(request):
    return render(request, 'soils.html')

def upload_file(request):
    if request.method == "POST" and request.FILES.getlist("files"):
        uploaded_files = request.FILES.getlist("files")

        pdf_file = None
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".pdf"):
                pdf_file = uploaded_file

        if not pdf_file:
            return HttpResponse("You must upload a PDF file.", status=400)

        try:
            # Save the uploaded PDF file locally (in-memory)
            pdf_file_path = f"/tmp/{pdf_file.name}"
            with open(pdf_file_path, "wb") as f:
                f.write(pdf_file.read())

            # Extract tables from the PDF using ExtractTable
            table_data = et_sess.process_file(filepath=pdf_file_path, output_format="df", pages="all")
            accumulated_data = pd.DataFrame()

            for each_table in table_data:
                accumulated_data = pd.concat([accumulated_data, each_table], ignore_index=True)

            # Extract text from the PDF using MarkItDown
            md = MarkItDown()
            result = md.convert(pdf_file_path)
            extracted_text = result.text_content

            # Combine extracted data
            excel_data = accumulated_data.to_dict(orient="records")
            combined_input = f"Excel Data: {excel_data}\n\nText File Content: {extracted_text}"

            # Send data to OpenAI
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant that processes geotechnical data. Output only valid JSON."},
                    {
                        "role": "user",
                        "content": f"""Analyze this data and return a JSON object with two parts:
                        1. header_data: containing Borehole Unique ID, Ground Elevation, Depth of exploration, ground water depth, and year of exploration
                        2. soil_layers: containing an array of soil layers with depth ranges and classifications

                        **Important:** Only use values from the 'Depth/Elev.' column for depth calculations, not the 'Depth' column on the far left.

                        Format the response as:
                        {{
                            "header_data": {{
                                "borehole_id": string,
                                "ground_elevation": number,
                                "depth_of_exploration": number,
                                "groundwater_depth": string,
                                "year_of_exploration": number
                            }},
                            "soil_layers": [
                                {{
                                    "depth_start": number,
                                    "depth_end": number,
                                    "soil_type": string
                                }}
                            ]
                        }}

                        Data to analyze: {combined_input}"""
                    }
                ],
                temperature=0
            )

            # Parse the response content as JSON
            response_content = completion.choices[0].message.content
            try:
                processed_data = json.loads(response_content)
                if not all(key in processed_data for key in ['header_data', 'soil_layers']):
                    raise ValueError("Missing required data fields in response")
            except json.JSONDecodeError:
                return HttpResponse("Error: Invalid JSON response from AI", status=500)
            except ValueError as e:
                return HttpResponse(f"Error: {str(e)}", status=500)

            # Save processed data and file names in the session
            request.session["uploaded_file_names"] = [pdf_file.name]
            request.session["processed_data"] = processed_data

            return redirect("boreholesummary")

        except Exception as e:
            return HttpResponse(f"An error occurred while processing the files: {str(e)}", status=500)

    # Retrieve file names from the session to display them on the upload page
    uploaded_file_names = request.session.get("uploaded_file_names", [])
    return render(request, "fileupload.html", {"uploaded_file_names": uploaded_file_names})

def boreholesummary(request):
    processed_data = request.session.get("processed_data", {})
    return render(request, "boreholesummary.html", {"processed_data": processed_data})
