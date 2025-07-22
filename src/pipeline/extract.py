import yaml
import requests
from src.logger import get_logger

logger = get_logger(__name__)

def get_landscape_data(url: str):
    """
    This function gets the landscape data from a specific URL that should be in yaml
    and returns the landscape part of the data
    """
    logger.info(f"Getting landscape data from {url}")
    landscape_raw = requests.get(url)
    landscape = yaml.safe_load(landscape_raw.content)['landscape']
    logger.info("Landscape data loaded")
    return landscape
