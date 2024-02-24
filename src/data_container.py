from typing import List


class DataContainer:
    # Variables coming from config to be used in the pipeline
    input_file: str
    output_kg_plot_path: str

    # Variables passed to the pipeline and are updated by different steps
    document: List
    all_section_triples: List
