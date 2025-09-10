import yaml
import requests
from src.logger import get_logger
import os

logger = get_logger(__name__)

def get_landscape_data(path: str):
    """
    This function gets the landscape data from a specific URL or local path that should be in yaml
    and returns the landscape part of the data
    """
    logger.info(f"Getting landscape data from {path}")
    if path.startswith('http'):
        landscape_raw = requests.get(path)
        landscape = yaml.safe_load(landscape_raw.content)['landscape']
    else:
        with open(path, 'r') as f:
            landscape = yaml.safe_load(f)['landscape']
    logger.info("Landscape data loaded")
    return landscape
