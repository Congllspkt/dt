from app.shared.exception.ai_model_not_defined_exception import AIModelNotDefinedException
from app.agent.model.ollama_llama_model import OllamaLlamaModel
from app.agent.model.ai_agent_model import AIAgentModel
from app.agent.model.gemnini_model import GerminiModel
from app.agent.model.ollama_deepseek_r1_model import OllamaDeekseakR1Model
from app.agent.model.chat_gpt_model import ChatGPTModel

class AIAgentModelFactory:

    def get(model_name):
        
        if model_name == AIAgentModel.Default:
            return GerminiModel()
        
        if model_name == AIAgentModel.Gemini1p5Flash:
            return GerminiModel()
        
        if model_name == AIAgentModel.GPT3p5Turbo:
            return ChatGPTModel()
        
        if model_name == AIAgentModel.OllamaDeepSeekR1c8b:
            return OllamaDeekseakR1Model()
        
        if model_name == AIAgentModel.OllamaLlama3p1c8b:
            return OllamaLlamaModel()
        
        raise AIModelNotDefinedException()