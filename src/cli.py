import fire
from src.legacy_main import Cli as LegacyCli
from src.logger import get_logger

logger = get_logger(__name__)

class RunGroup:
    def etl(self, input_path="https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml", output_dir="data"):
        """Runs the legacy ETL pipeline."""
        logger.info("Running ETL pipeline via src/cli.py")
        LegacyCli().run(input_path, output_dir)

    def workflow(self):
        logger.info("Running workflow (placeholder)")

    def agent(self):
        logger.info("Running agent (placeholder)")

class Cli:
    def __init__(self):
        self.run = RunGroup()

if __name__ == '__main__':
    fire.Fire(Cli)
