import requests
import json
import os

openai_api_key = ''# put yout api key here
if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in environment variables.")

url = "https://api.openai.com/v1/chat/completions"

message1 = ''
message2 = ''
message3 = ''

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-3.5-turbo",
    "response_format": {"type": "json_object"},
    "messages": [
        {
            "role": "user",
            "content": message1
        },
        {
            "role": "assistant",
            "content": message2
        },
        {
            "role": "user",
            "content": message3
        },
    ]
}

response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Response from OpenAI:", response.json())
    print('\n')
    print(response.json()['choices'][0]['message']['content'])
else:
    print("Error:", response.status_code, response.text)