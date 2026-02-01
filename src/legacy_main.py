"""Legacy CLI wrapper (deprecated)."""

import fire
from src.pipeline.runner import run_etl


class Cli:
    def run(
        self,
        input_path="https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml",
        output_dir="data",
    ):
        run_etl(input_path=input_path, output_dir=output_dir)


if __name__ == '__main__':
    fire.Fire(Cli)
