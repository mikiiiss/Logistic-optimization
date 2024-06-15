import pandas as pd
import warnings
from causalnex.structure import StructureModel
import numpy as np

warnings.filterwarnings("ignore")  # silence warnings

data = pd.read_csv('final.csv')

struct_data = data.copy()
non_numeric_columns = list(struct_data.select_dtypes(exclude=[np.number]).columns)
print(non_numeric_columns)

for col in struct_data.columns:
    if struct_data[col].isnull().any():
        mean_value = struct_data[col].mean()
        struct_data[col].fillna(mean_value, inplace=True)

from causalnex.structure.notears import from_pandas
sm = from_pandas(struct_data)

import matplotlib.pyplot as plt
from causalnex.plots import plot_structure, NODE_STYLE, EDGE_STYLE
viz = plot_structure(
    sm,
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK
)

viz.toggle_physics(False)
viz.show("03_fully_connected.html")

sm.remove_edges_below_threshold(0.8)
viz.show("support01_thresholded.html")

viz.show("03_fully_connected.html")

sm = from_pandas(struct_data, tabu_edges=[("weekday","displacement")], w_threshold=0.8)
#sm = sm.get_largest_subgraph()
viz = plot_structure(
    sm,
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK
)

viz.show("03_largest_subgraph.html")