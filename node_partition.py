from pdp_lib import preprocess
from pdp_lib import draw
nodes=preprocess.read_node('pdp_instances/LiLim/pdp_100/lrc207.txt')
draw.draw_nodes(nodes)