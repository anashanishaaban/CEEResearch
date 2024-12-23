from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PointCloudFile
from .serializers import PointCloudFileSerializer
from .utils import process_pointcloud
from django.shortcuts import render

def index(request):
    """
    Render the main page for uploading and visualizing point clouds.
    """
    return render(request, 'index.html')



class PointCloudUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PointCloudFileSerializer(data=request.data)
        if serializer.is_valid():
            # Save the uploaded file
            instance = serializer.save()

            # Process the uploaded point cloud file
            try:
                processed_file_path = process_pointcloud(instance.file.path)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)

            # Get the URL for the processed file
            processed_file_url = os.path.join(settings.MEDIA_URL, os.path.basename(processed_file_path))

            return Response({
                "message": "Uploaded and processed successfully!",
                "processed_file": processed_file_url
            }, status=201)
        return Response(serializer.errors, status=400)