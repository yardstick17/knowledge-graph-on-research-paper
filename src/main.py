import logging

import click

from interface import step_factory
from data_container import DataContainer
from utils import read_config
from steps.base import Step

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@click.command()
@click.option("--config-path", "-c", help="Config path for building knowledge graph")
def main(config_path):
    config = read_config(config_path)

    data_container = DataContainer()
    data_container.steps = config.get("steps", [])
    data_container.input_file = config.get("data")["research_paper_path"]
    data_container.output_kg_plot_path = config.get("output")["output_kg_plot_path"]

    # Execute each components' step in sequence.
    for step in data_container.steps:
        logger.info(f"Executing Step: {step}")
        try:
            step_object: Step = step_factory[step]()
        except KeyError:
            logger.exception(
                f"Make sure the steps are defined in steps.interface:step_factory. Step missing: {step}"
            )
            raise
        data_container = step_object.execute(data_container=data_container)


if __name__ == "__main__":
    main()
