#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add project root to sys.path
repo_root = Path(__file__).resolve().parents[1]
sys.path.append(str(repo_root))

from src.agentic.config import get_available_models
from pydantic_ai.models.google import GoogleModel

def list_models():
    gateway_key = os.getenv('PYDANTIC_AI_GATEWAY_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')

    print("=" * 50)
    print("AI Model Configuration")
    print("=" * 50)
    
    if gateway_key:
        print(f"Status: Using Pydantic AI Gateway (KEY: {gateway_key[:5]}...{gateway_key[-4:]})")
    elif google_key:
        print(f"Status: Using Google AI directly (KEY: {google_key[:5]}...{google_key[-4:]})")
    else:
        print("Status: WARNING - No API keys found (Neither PYDANTIC_AI_GATEWAY_API_KEY nor GOOGLE_API_KEY)")
    
    print("-" * 50)
    print("Available Models:")
    
    try:
        models = get_available_models()
        if not models:
            print("  No models available. Ensure API keys are set correctly.")
        else:
            for m in models:
                if isinstance(m, str):
                    print(f"  - {m} (Gateway)")
                elif isinstance(m, GoogleModel):
                    print(f"  - {m.model_name} (GoogleDirect)")
                else:
                    print(f"  - {m}")
    except Exception as e:
        print(f"  Error retrieving models: {e}")

    print("=" * 50)
    
    # Try to simulate getting the model for a generic agent to see what the final resolved model would be
    try:
        from src.config import load_config
        cfg = load_config()
        # Same priority as src/agentic/config.py
        resolved_name = (
            cfg.agents.get('default_model') or 
            os.getenv('GEMINI_MODEL') or 
            'gateway/google-vertex:gemini-2.0-flash'
        )
        print(f"Default model (Config/GEMINI_MODEL): {resolved_name}")
    except Exception:
        current_model = os.getenv('GEMINI_MODEL') or "gateway/google-vertex:gemini-2.0-flash (default)"
        print(f"Default model (env): {current_model}")
        
    print("=" * 50)

if __name__ == "__main__":
    list_models()
