import os
import requests
import json

from app.core.config import settings

class GerminiModel():
    def sendMessage(self, prompt):  # Added self and renamed to snake_case
        try:
            url = settings.URL_GEMINI + "/ask"  # Replace with the actual API endpoint

            headers = {
                "Content-Type": "application/json"  # Important for sending JSON data
            }
            data = {
                        "contents": [
                            {"role": "user", "parts": [{"text": prompt}]}
                        ]
                    }
            response = requests.post(url, headers=headers, data=json.dumps(data))  # Use json.dumps() to convert the dictionary to a JSON string

            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Process the response
            print("Status Code:", response.status_code)
            response_json = response.json();
            content_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

            print("Response Body:", content_text)  # If the response is also in JSON format
            # time.sleep(1)
            return content_text

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
