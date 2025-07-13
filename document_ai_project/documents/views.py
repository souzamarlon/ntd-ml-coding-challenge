from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from documents.ocr import extract_text_from_image
from documents.vector_store import query_similar_document
from rest_framework import status
from documents.serializers import DocumentUploadSerializer, DocumentResultSerializer


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data['file']

        with open("temp_file", "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        text = extract_text_from_image("temp_file")
        doc_result = query_similar_document(text)
        metadata = doc_result.get("metadata", [[]])
        doc_type = (
            metadata['type']
            if metadata and 'type' in metadata
            else "unknown"
        )
        entities = (
            metadata['entities']
            if metadata and 'entities' in metadata
            else "unknown"
        )

        response_data = {
            "document_type": doc_type,
            "entities": entities
        }

        serializer = DocumentResultSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
