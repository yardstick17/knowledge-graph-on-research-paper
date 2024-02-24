import yaml

from data_container import DataContainer
from steps.base import Step


class ReadResearchPaper(Step):
    def execute(self, data_container: DataContainer):
        # Load the YAML file
        with open(data_container.input_file, 'r') as file:
            data = yaml.safe_load(file)

        data_container.document = [text for section, text in data.items()]
