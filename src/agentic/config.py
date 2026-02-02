import os
from pydantic_ai.models.google import GoogleModel
from src.config import load_config

def get_model(agent_name: str):
    """Get the model for a specific agent based on configuration."""
    cfg = load_config()
    
    # Try to get agent-specific model from config, fallback to default_model, then env, then hardcoded default
    agent_settings = cfg.agents.get(agent_name, {}) if hasattr(cfg, 'agents') else {}
    default_model = cfg.agents.get('default_model', 'gemini-3-flash') if hasattr(cfg, 'agents') else 'gemini-3-flash'
    
    model_name = agent_settings.get('model') or os.getenv('GEMINI_MODEL') or default_model
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError(
            f"GOOGLE_API_KEY environment variable is not set. "
            f"Cannot initialize the {agent_name} agent without a configured Gemini model."
        )
    
    return GoogleModel(model_name)

def get_available_models():
    """Get a list of available models for the UI."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return []
    
    # Models available in the environment as per the provided screenshot
    model_names = [
        'gemini-3-flash',
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemma-3-27b',
        'gemma-3-12b',
        'gemma-3-4b',
        'gemma-3-2b',
        'gemma-3-1b',
    ]
    return [GoogleModel(name) for name in model_names]
