import os
import glob
from pdp_lib import preprocess
from pdp_lib import draw


#filename='pdp_instances/LiLim/pdp_100/lrc207.txt'

nodes=preprocess.read_node(filename)
draw.draw_original_nodes(nodes, filename)

