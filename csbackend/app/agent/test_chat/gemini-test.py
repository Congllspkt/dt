key = '' # your api key

import google.generativeai as genai
import os

genai.configure(api_key=key)

model = genai.GenerativeModel('gemini-1.5-flash')
contents = [
    {"role": "user", "parts":[ { "text": "Hello" }, { "text": "\nI'm Peter" } ]},
    {"role": "model", "parts":[{ "text": "Great to meet you. What would you like to know?" }]},
    {"role": "user", "parts":[{ "text": "What is" }]},
]
response = model.generate_content(contents,
                                  generation_config=genai.GenerationConfig(response_mime_type="application/json"))
print(response)