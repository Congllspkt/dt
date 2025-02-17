class AIAgent:
    def sendMessage(prompt):
        import ollama
        client = ollama.Client()
        model = 'llama3.2:latest'
        response = client.generate(model=model, prompt=prompt)
        return response.response