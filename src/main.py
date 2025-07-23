import fire
from pipeline.processor import Processor
from logger import get_logger

logger = get_logger(__name__)

class Cli:
  def run(self):
    logger.info("Starting landscape processing")
    processor = Processor("https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml")
    processor.run()
    logger.info("Landscape processing finished")

if __name__ == '__main__':
  fire.Fire(Cli)
