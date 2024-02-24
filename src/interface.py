# This step factory implements the core logic in the `execute` method.
# These Step update the `DataContainer` attributes as it is passed through different steps.
from steps.build_knowledge_graph import BuildKnowledgeGraph
from steps.document_relation_extraction import DocumentRelationExtraction
from steps.read_pdf_research_paper import ReadPDFResearchPaper
from steps.read_research_paper import ReadResearchPaper

step_factory = {
    "read-research-paper": ReadResearchPaper,
    "read-pdf-research-paper": ReadPDFResearchPaper,
    "document-relation-extraction": DocumentRelationExtraction,
    "build-knowledge-graph": BuildKnowledgeGraph,
    # "evaluate": Evaluation,
}
