#!/usr/bin/env python3
"""CLI utility to inspect active AI model configuration and available models using typed Pydantic models."""

import sys
from pathlib import Path

# Ensure project root is in sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from pydantic_ai.models.google import GoogleModel
from src.agentic.config import (
    AgentSettings,
    KeyConfigStatus,
    ProviderType,
    get_agent_settings,
    get_available_models,
)
from src.config import load_config


def inspect_key_status(settings: AgentSettings) -> KeyConfigStatus:
    """Return a typed Pydantic KeyConfigStatus model from settings."""
    provider = settings.active_provider
    if provider == ProviderType.GATEWAY:
        return KeyConfigStatus(
            provider=provider,
            secret_key=settings.pydantic_ai_gateway_api_key,
            is_1password_ref=False,
        )
    elif provider == ProviderType.GOOGLE_DIRECT:
        return KeyConfigStatus(
            provider=provider,
            secret_key=settings.google_api_key,
            is_1password_ref=settings.is_1password_ref,
        )
    return KeyConfigStatus(provider=ProviderType.NONE)


def print_status_header(status: KeyConfigStatus) -> None:
    """Print the formatted status header based on Pydantic KeyConfigStatus."""
    print("=" * 50)
    print("AI Model Configuration")
    print("=" * 50)

    if status.provider == ProviderType.GATEWAY:
        print(f"Status: Using Pydantic AI Gateway (KEY: {status.safe_display_key})")
    elif status.provider == ProviderType.GOOGLE_DIRECT:
        if status.is_1password_ref:
            print(f"Status: 1Password Reference Detected ({status.safe_display_key})")
            print("Note:   Run with `op run --env-file=../.env -- just list-models` to resolve and query live Google API.")
        else:
            print(f"Status: Using Google AI directly (KEY: {status.safe_display_key}) [Live Google GenAI API]")
    else:
        print("Status: WARNING - No API keys found (Neither PYDANTIC_AI_GATEWAY_API_KEY nor GOOGLE_API_KEY)")


def print_available_models(status: KeyConfigStatus) -> None:
    """Retrieve and display available AI models for the active configuration."""
    print("-" * 50)
    print("Available Models:")

    try:
        models = get_available_models()
        if not models:
            print("  No models available. Ensure API keys are set correctly.")
            return

        if status.provider == ProviderType.GATEWAY:
            provider_label = "Gateway"
        elif status.provider == ProviderType.GOOGLE_DIRECT:
            provider_label = "Google AI Studio"
        else:
            provider_label = "Supported"

        for m in models:
            if isinstance(m, str):
                print(f"  - {m} ({provider_label})")
            elif isinstance(m, GoogleModel):
                print(f"  - {m.model_name} (Google AI Studio)")
            else:
                print(f"  - {m}")
    except Exception as e:
        print(f"  Error retrieving models: {e}")


def get_resolved_default_model(settings: AgentSettings) -> str:
    """Resolve default model from config.yaml or Pydantic AgentSettings."""
    try:
        cfg = load_config()
        return (
            cfg.agents.get("default_model")
            or settings.gemini_model
            or "gemini-2.5-flash"
        )
    except Exception:
        return settings.gemini_model or "gemini-2.5-flash (default)"


def print_default_model_info(settings: AgentSettings) -> None:
    """Print configured default model information."""
    print("=" * 50)
    default_model = get_resolved_default_model(settings)
    print(f"Default model (Config/GEMINI_MODEL): {default_model}")
    print("=" * 50)


def list_models() -> None:
    """Main entrypoint to list AI model status and available models."""
    settings = get_agent_settings()
    status = inspect_key_status(settings)
    print_status_header(status)
    print_available_models(status)
    print_default_model_info(settings)


if __name__ == "__main__":
    list_models()
