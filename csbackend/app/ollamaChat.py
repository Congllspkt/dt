import ollama

client = ollama.Client()

model = 'llama3.2:latest'
prompt = "Viet 1 kich ban vui nhon"

response = client.generate(model=model, prompt=prompt)

print("response: ")
print(response.response)
