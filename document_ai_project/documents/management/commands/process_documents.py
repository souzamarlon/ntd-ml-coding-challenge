from django.core.management.base import BaseCommand
import os
from documents.ocr import extract_text_from_image
from documents.extractor import extract_entities
from documents.vector_store import upsert_document
import json


class Command(BaseCommand):
    help = "Process documents in a folder"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to folder with documents')

    def handle(self, *args, **options):
        path = options['path']
        for root, _, files in os.walk(path):
            for filename in files:
                if not filename.strip().lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    continue
                file_path = os.path.join(root, filename)
                self.stdout.write(f"Processing {file_path}")
                try:
                    text = extract_text_from_image(file_path)
                    entities = extract_entities(text)
                    safe_metadata = {
                        "type": entities.get("document_type", None),
                        "entities": json.dumps(entities) 
                    }

                    upsert_document(filename, text, safe_metadata)
                except Exception as e:
                    import traceback
                    self.stderr.write(f"Failed to process {filename}: {str(e)}")
                    traceback.print_exc()