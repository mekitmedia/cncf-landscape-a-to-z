from enum import Enum
import os
from typing import Optional, List
from pydantic import BaseModel, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_ai.models.google import GoogleModel
from src.config import load_config


class ProviderType(str, Enum):
    """Enumeration of supported AI model providers."""
    GATEWAY = "gateway"
    GOOGLE_DIRECT = "google_direct"
    NONE = "none"


class AgentSettings(BaseSettings):
    """Pydantic BaseSettings model for safe, validated configuration loading with SecretStr."""
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: Optional[SecretStr] = Field(
        default=None,
        validation_alias="GOOGLE_API_KEY",
        description="Google AI Studio API key (protected via SecretStr)",
    )
    pydantic_ai_gateway_api_key: Optional[SecretStr] = Field(
        default=None,
        validation_alias="PYDANTIC_AI_GATEWAY_API_KEY",
        description="Pydantic AI Gateway API key (protected via SecretStr)",
    )
    gemini_model: Optional[str] = Field(
        default=None,
        validation_alias="GEMINI_MODEL",
        description="Gemini model name override",
    )

    @property
    def active_provider(self) -> ProviderType:
        """Determine active provider based on configured API keys."""
        if self.pydantic_ai_gateway_api_key:
            return ProviderType.GATEWAY
        elif self.google_api_key:
            return ProviderType.GOOGLE_DIRECT
        return ProviderType.NONE

    @property
    def is_1password_ref(self) -> bool:
        """Check if google_api_key is an unresolved 1Password reference string."""
        if self.google_api_key:
            return self.google_api_key.get_secret_value().startswith("op://")
        return False

    @property
    def raw_google_key(self) -> Optional[str]:
        """Safely extract raw string value for GOOGLE_API_KEY if present."""
        return self.google_api_key.get_secret_value() if self.google_api_key else None

    @property
    def raw_gateway_key(self) -> Optional[str]:
        """Safely extract raw string value for PYDANTIC_AI_GATEWAY_API_KEY if present."""
        return self.pydantic_ai_gateway_api_key.get_secret_value() if self.pydantic_ai_gateway_api_key else None


class KeyConfigStatus(BaseModel):
    """Pydantic model representing active key configuration and provider status."""
    provider: ProviderType
    secret_key: Optional[SecretStr] = None
    is_1password_ref: bool = False

    @property
    def safe_display_key(self) -> str:
        """Pydantic SecretStr manages sensitive string protection natively."""
        if not self.secret_key:
            return "None"
        val = self.secret_key.get_secret_value()
        if self.is_1password_ref:
            return f"{val[:15]}..."
        # Pydantic native SecretStr string representation (e.g. '**********')
        return str(self.secret_key)


def get_agent_settings() -> AgentSettings:
    """Instantiate and return the validated AgentSettings instance."""
    return AgentSettings()


def get_model(agent_name: str):
    """Get the model for a specific agent based on configuration."""
    cfg = load_config()
    settings = get_agent_settings()
    
    agent_settings = cfg.agents.get(agent_name, {})
    model_name = (
        agent_settings.get('model') or 
        cfg.agents.get('default_model') or 
        settings.gemini_model or 
        'gemini-2.5-flash'
    )
    
    gateway_key = settings.raw_gateway_key
    google_key = settings.raw_google_key

    env_hint = "op run --env-file=../.env -- just workflow" if os.path.exists("../.env") else "op run -- just workflow"

    if gateway_key:
        if gateway_key.startswith('op://'):
            raise RuntimeError(
                f"PYDANTIC_AI_GATEWAY_API_KEY contains an unexpanded 1Password reference ('op://...').\n"
                f"Please run using 1Password CLI: `{env_hint}`"
            )
        return model_name

    if google_key:
        if google_key.startswith('op://'):
            raise RuntimeError(
                f"GOOGLE_API_KEY contains an unexpanded 1Password reference ('op://...').\n"
                f"Please run using 1Password CLI: `{env_hint}`"
            )
        # Strip gateway prefix for direct Google usage
        if model_name.startswith('gateway/google-vertex:'):
            model_name = model_name.replace('gateway/google-vertex:', '')
        elif model_name.startswith('gateway/'):
            raise RuntimeError(f"Direct Google usage does not support non-Google model: {model_name}")
            
        return GoogleModel(model_name)
    
    raise RuntimeError(
        f"Neither PYDANTIC_AI_GATEWAY_API_KEY nor GOOGLE_API_KEY environment variable is set.\n"
        f"If your secrets are stored in 1Password, execute using 1Password CLI:\n"
        f"  {env_hint}\n"
        f"  (or simply: just workflow)"
    )


def fetch_live_google_models(google_key: Optional[str]):
    """Fetch live models from Google Generative AI API via modern google.genai SDK."""
    if not google_key or google_key.startswith('op://'):
        return None
    try:
        from google import genai
        client = genai.Client(api_key=google_key)
        live_models = []
        for model in client.models.list():
            name = model.name.replace('models/', '') if hasattr(model, 'name') else str(model)
            supported = getattr(model, 'supported_actions', []) or getattr(model, 'supported_generation_methods', []) or []
            if 'generateContent' in supported or not supported:
                if name.startswith('gemini'):
                    live_models.append(name)
        if live_models:
            return live_models
    except Exception:
        pass
    return None

def get_available_models():
    """Get a list of available models based on active key type (Google AI Studio vs Gateway)."""
    settings = get_agent_settings()
    gateway_key = settings.raw_gateway_key
    google_key = settings.raw_google_key

    if gateway_key:
        return [
            'gateway/openai:gpt-5',
            'gateway/anthropic:claude-sonnet-4-5',
            'gateway/google-vertex:gemini-2.5-flash',
            'gateway/google-vertex:gemini-2.5-flash-lite',
            'gateway/groq:openai/gpt-oss-120b',
            'gateway/bedrock:amazon.nova-micro-v1:0',
        ]
    elif google_key:
        live = fetch_live_google_models(google_key)
        if live:
            return live
        return [
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
        ]
    else:
        return [
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gateway/google-vertex:gemini-2.5-flash',
        ]
