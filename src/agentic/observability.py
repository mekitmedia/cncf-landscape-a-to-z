import os
import logging
import logfire

logger = logging.getLogger(__name__)

def setup_observability():
    """
    Configure Logfire for observability.
    Should be called once at the start of the application.
    """
    # Configure Logfire if token is present
    if os.getenv('LOGFIRE_TOKEN'):
        try:
            logfire.configure()
            # Auto-instrument Pydantic and Pydantic AI
            logfire.instrument_pydantic()
            if hasattr(logfire, 'instrument_pydantic_ai'):
                logfire.instrument_pydantic_ai()
            logger.info("Logfire configured successfully.")
        except Exception as e:
            logger.error(f"Failed to configure Logfire: {e}")
    else:
        logger.debug("LOGFIRE_TOKEN not set, skipping Logfire configuration.")
