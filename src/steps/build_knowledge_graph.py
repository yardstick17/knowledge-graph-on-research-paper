import logging

from core.knowledge_graphs.build_knowledge_graph import get_graph
from data_container import DataContainer
from steps.base import Step
import networkx as nx
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class BuildKnowledgeGraph(Step):
    def execute(self, data_container: DataContainer):
        logger.info(
            f"Executing the build graph using: {len(data_container.all_section_triples)} elements"
        )
        graph = get_graph(data_container.all_section_triples)

        links = []
        data = {"object": None, "linkType": None, "dependentObject": None, "description": ""}
        lol = set()
        for item in data_container.all_section_triples:
            data["object"] = item["head"]
            data["dependentObject"] = item["tail"]
            data["linkType"] = item["type"]
            links.append(data)
            lol.add(data["object"])
            lol.add(data["dependentObject"])

        plotting_data = {"nodes": list(lol), "links": links }

        import json
        with open('output/result.json', 'w') as fp:
            json.dump(plotting_data, fp)

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
