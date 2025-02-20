from app.agent.model.ai_agent_model_factory import AIAgentModelFactory

class AIAgent:

    def get_model(self, model_name):
        return AIAgentModelFactory.get(model_name)

    def sendMessage(self, model_name, prompt):
        ai_model = self.get_model(model_name)
        return ai_model.sendMessage(prompt=prompt)
    
ai_agent = AIAgent()