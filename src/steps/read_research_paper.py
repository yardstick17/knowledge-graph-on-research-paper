import logging

import yaml

from data_container import DataContainer
from steps.base import Step

logger = logging.getLogger(__name__)


class ReadResearchPaper(Step):
    def execute(self, data_container: DataContainer):
        # Load the YAML file
        with open(data_container.input_file, "r") as file:
            data = yaml.safe_load(file)
            data_container.document = [
                self.clean_string(text) for section, text in data.items()
            ]
            logger.info(f"Got total documents: {len(data_container.document)}")
        return data_container

    def clean_string(self, s):
        # Remove leading and trailing whitespace
        s = s.strip()

        # Remove line breaks
        s = s.replace("\n", " ").replace("\r", "")
        return s
