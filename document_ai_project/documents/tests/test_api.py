from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from unittest.mock import patch


class DocumentUploadViewTest(APITestCase):
    @patch('documents.ocr.extract_text_from_image')
    def test_upload_document(self, mock_ocr):
        mock_ocr.return_value = "Sample text extracted from image"

        image = Image.new('RGB', (1, 1), color='white')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        uploaded_file = SimpleUploadedFile("test.jpg", img_byte_arr.read(), content_type="image/jpeg")
        response = self.client.post("/api/upload/", {'file': uploaded_file}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertIn('document_type', response.data)
        self.assertIn('entities', response.data)
