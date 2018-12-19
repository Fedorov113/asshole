from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

import json

from explorer.file_system.file_system_helpers import import_sample_file, delete_sample


class SampleImportView(APIView):
    def post(self, request):
        success, message = import_sample_file(json.loads(request.body))
        if success:
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        delete_sample(json.loads(request.body))
        return Response('deleted', status=status.HTTP_200_OK)
