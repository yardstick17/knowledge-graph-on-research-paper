from core.relationship_extraction.triple_extractor import get_triplets
from data_container import DataContainer
from steps.base import Step


class DocumentRelationExtraction(Step):
    def execute(self, data_container: DataContainer):
        all_section_triples = []
        for section in data_container.document:
            result = get_triplets(section)
            all_section_triples.extend(result)
        data_container.all_section_triples = all_section_triples
        return data_container
