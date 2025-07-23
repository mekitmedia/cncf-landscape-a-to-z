import yaml
import requests
from src.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)

def get_landscape_data(url: str):
    """
    This function gets the landscape data from a specific URL that should be in yaml
    and returns the landscape part of the data
    """
    logger.info(f"Getting landscape data from {url}")
    if url.startswith('http'):
        landscape_raw = requests.get(url)
        landscape = yaml.safe_load(landscape_raw.content)['landscape']
    else:
        with open(url, 'r') as f:
            landscape = yaml.safe_load(f)['landscape']
    logger.info("Landscape data loaded")
    return landscape
