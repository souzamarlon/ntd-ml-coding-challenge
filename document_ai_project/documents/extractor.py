from openai import OpenAI
import json
from django.conf import settings

openai_api_key = settings.OPENAI_API_KEY

client = OpenAI(api_key=openai_api_key)


def extract_entities(text: str) -> dict:

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a reliable assistant that extracts structured data from unstructured text. Always respond with a JSON object containing relevant metadata."
            },
            {
                "role": "user",
                "content": f"""
                    Please analyze the text below and do the following:
                    1. Determine the document type (e.g., invoice, form, assignment, letter, etc.)
                    2. Extract relevant entities including:
                        - Sender and recipient names (if available)
                        - Dates
                        - Addresses
                        - Invoice amount or payment total (if applicable)
                        - Any other meaningful metadata

                    Return your answer as a JSON object with at least the following fields:
                    {{
                        "document_type": string,
                        "sender": string or null,
                        "recipient": string or null,
                        "dates": list of strings,
                        "addresses": list of strings,
                        "amount": string or null,
                        "other_metadata": dict or null
                    }}

                    Do not include any explanation or commentary. Only return the JSON.

                    Text:
                    {text}
                """
            }
        ]
    )
    
    try:
        parsed_entities = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        parsed_entities = {"error": "Invalid JSON in model response"}

    return parsed_entities