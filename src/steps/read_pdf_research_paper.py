import yaml

from data_container import DataContainer
from steps.base import Step


class ReadPDFResearchPaper(Step):
    def execute(self, data_container: DataContainer):
        raise NotImplementedError
