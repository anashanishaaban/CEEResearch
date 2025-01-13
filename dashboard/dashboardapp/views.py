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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import AIMessage, HumanMessage


client = OpenAI()

# ExtractTable API key
EXTRACT_TABLE_API_KEY = "CfurTKm6aPtbLe1V4lpji2ztipruquOuuNNIxvAK"
et_sess = ExtractTable(EXTRACT_TABLE_API_KEY)
print(et_sess.check_usage())

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

            # Store the original excel_data in the session
            request.session["original_excel_data"] = excel_data
            request.session["extracted_text"] = extracted_text

            # Updated prompt to include averages
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant that processes geotechnical data. Output only valid JSON."},
                    {
                        "role": "user",
                        "content": f"""Analyze this data and return a JSON object with three parts:
                        1. header_data: containing Borehole Unique ID, Ground Elevation, Depth of exploration, ground water depth, and year of exploration.
                        2. soil_layers: containing an array of soil layers, water, and barge, with depth ranges and classifications. The depth range starts from 0, and the first classification is from 0 - whatever depth.
                        3. averages: including Average SPT (N60), Average Moisture Content (%), Average Cohesion (psf), and Average Bulk Unit Weight (pcf).

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
                            ],
                            "averages": {{
                                "average_spt_n60": number,
                                "average_moisture_content": number,
                                "average_cohesion": string,
                                "average_bulk_unit_weight": string
                            }}
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
                if not all(key in processed_data for key in ['header_data', 'soil_layers', 'averages']):
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

    uploaded_file_names = request.session.get("uploaded_file_names", [])
    return render(request, "fileupload.html", {"uploaded_file_names": uploaded_file_names})

@csrf_exempt
def update_table(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        processed_data = request.session.get("processed_data", {})
        original_excel_data = request.session.get("original_excel_data", {})
        extracted_text = request.session.get("extracted_text", "")
        
        # Get the history stack from session, or initialize if it doesn't exist
        data_history = request.session.get("data_history", [])

        if not processed_data:
            return JsonResponse({"error": "No processed data found. Please upload a file first."}, status=400)

        try:
            # Check if the user wants to undo
            if "undo" in user_input.lower():
                if data_history:
                    # Pop the last state from history
                    previous_state = data_history.pop()
                    # Update the current processed data
                    processed_data = previous_state
                    # Save the updated history and current state
                    request.session["data_history"] = data_history
                    request.session["processed_data"] = processed_data
                    return JsonResponse({
                        "success": True,
                        "updated_data": processed_data,
                        "message": "Successfully undid last change"
                    })
                else:
                    return JsonResponse({
                        "error": "No previous state to revert to"
                    }, status=400)

            # If not undoing, proceed with normal update
            # Save current state to history before making changes
            data_history.append(processed_data.copy())
            # Limit history size to prevent session from growing too large
            if len(data_history) > 10:  # Keep last 10 states
                data_history.pop(0)
            request.session["data_history"] = data_history

            # Create a prompt for GPT-4 to modify the data based on user input
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant that modifies geotechnical data based on user input and original Excel data. Output only valid JSON in the exact same format as the input data."},
                    {
                        "role": "user",
                        "content": f"""
                        Original Excel Data: {json.dumps(original_excel_data)}
                        Original Text Content: {extracted_text}
                        Current Summary Data: {json.dumps(processed_data)}
                        
                        User request: {user_input}
                        
                        Using both the original Excel data and the current summary, modify the data according to the user's request.
                        Return the modified JSON maintaining this exact structure:
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
                            ],
                            "averages": {{
                                "average_spt_n60": number,
                                "average_moisture_content": number,
                                "average_cohesion": string,
                                "average_bulk_unit_weight": string
                            }}
                        }}
                        """
                    }
                ],
                temperature=0
            )

            # Parse the modified data
            response_content = completion.choices[0].message.content
            updated_data = json.loads(response_content)

            # Validate the structure of the updated data
            if not all(key in updated_data for key in ['header_data', 'soil_layers', 'averages']):
                raise ValueError("Modified data is missing required fields")

            # Update session data with the modified version
            request.session["processed_data"] = updated_data

            return JsonResponse({
                "success": True,
                "updated_data": updated_data,
                "message": "Successfully updated data"
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the response"}, status=500)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

def boreholesummary(request):
    processed_data = request.session.get("processed_data", {})
    return render(request, "boreholesummary.html", {"processed_data": processed_data})

# def process_references(request):
#     """
#     Extract tables from PDFs in the references directory and classify them using OpenAI.
#     """
#     references_dir = "/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/references"
#     extracted_data = []

#     try:
#         # Loop through all PDF files in the directory
#         for filename in os.listdir(references_dir):
#             if filename.endswith(".pdf"):
#                 pdf_path = os.path.join(references_dir, filename)
#                 table_data = et_sess.process_file(filepath=pdf_path, output_format="df", pages="all")
                
#                 # Combine all extracted tables
#                 combined_data = pd.DataFrame()
#                 for each_table in table_data:
#                     combined_data = pd.concat([combined_data, each_table], ignore_index=True)

#                 # Convert to dictionary format for OpenAI
#                 table_dict = combined_data.to_dict(orient="records")
#                 extracted_data.append({"filename": filename, "tables": table_dict})

#         # Use OpenAI to classify the data into categories
#         completion = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an assistant that processes geotechnical data. "
#                         "Classify the extracted table data into categories: Basic Properties, "
#                         "Engineering Properties, Hydraulic Properties, and Settlement Parameters "
#                         "based on the soil type. Output valid JSON grouped into these categories."
#                     ),
#                 },
#                 {"role": "user", "content": json.dumps(extracted_data)}
#             ],
#             temperature=0,
#         )

#         # Parse OpenAI response
#         response_content = completion.choices[0].message.content
#         classified_data = json.loads(response_content)

#         # Return the classified data to the frontend
#         return JsonResponse({"success": True, "classified_data": classified_data})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)