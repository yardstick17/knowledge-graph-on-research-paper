import logging

from core.relationship_extraction.triple_extractor import get_triplets, get_triplets_using_transformers
from data_container import DataContainer
from steps.base import Step

logger = logging.getLogger(__name__)


class DocumentRelationExtraction(Step):
    def execute(self, data_container: DataContainer):
        all_section_triples = []
        for section in data_container.document:
            logger.info(
                f"Processing this section text: {section[:150]}... Total chars: {len(section)}"
            )
            section = section.replace("\n", " ")
            result = get_triplets_using_transformers(section)
            all_section_triples.extend(result)
        data_container.all_section_triples = all_section_triples
        return data_container
