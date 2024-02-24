import logging

from core.knowledge_graphs.build_knowledge_graph import get_graph
from data_container import DataContainer
from steps.base import Step
import networkx as nx
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class BuildKnowledgeGraph(Step):
    def execute(self, data_container: DataContainer):
        graph = get_graph(data_container.all_section_triples)
        nx.draw(
            graph,
            with_labels=True,
            font_weight="bold",
            node_color="skyblue",
            node_size=1500,
            edge_color="gray",
        )
        plt.savefig(data_container.output_kg_plot_path, dpi=300, bbox_inches="tight")
        logger.info(
            f"Knowledge graph plot saved at: {data_container.output_kg_plot_path }"
        )
        return data_container
