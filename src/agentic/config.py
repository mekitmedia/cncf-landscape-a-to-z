import os
from pydantic_ai.models.google import GoogleModel
from src.config import load_config

def get_model(agent_name: str):
    """Get the model for a specific agent based on configuration."""
    cfg = load_config()
    
    # Priority:
    # 1. Agent-specific model in config.yaml
    # 2. Global default_model in config.yaml
    # 3. GEMINI_MODEL environment variable
    # 4. Hardcoded default
    agent_settings = cfg.agents.get(agent_name, {})
    model_name = (
        agent_settings.get('model') or 
        cfg.agents.get('default_model') or 
        os.getenv('GEMINI_MODEL') or 
        'gateway/google-vertex:gemini-2.0-flash'
    )
    
    gateway_key = os.getenv('PYDANTIC_AI_GATEWAY_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')

    if gateway_key:
        return model_name

    if google_key:
        # Strip gateway prefix for direct Google usage
        if model_name.startswith('gateway/google-vertex:'):
            model_name = model_name.replace('gateway/google-vertex:', '')
        elif model_name.startswith('gateway/'):
            raise RuntimeError(f"Direct Google usage does not support non-Google model: {model_name}")
            
        return GoogleModel(model_name)
    
    raise RuntimeError(
        f"Neither PYDANTIC_AI_GATEWAY_API_KEY nor GOOGLE_API_KEY environment variable is set. "
        f"Cannot initialize the {agent_name} agent without a configured model."
    )

def get_available_models():
    """Get a list of available models for the UI."""
    return [
        'gateway/openai:gpt-5',
        'gateway/anthropic:claude-sonnet-4-5',
        'gateway/google-vertex:gemini-2.5-flash',
        'gateway/groq:openai/gpt-oss-120b',
        'gateway/bedrock:amazon.nova-micro-v1:0',
    ]
