import os
from pdp_lib import draw
from pdp_lib import preprocess
from pdp_lib import save_pics

'''
filename='pdp_instances/LiLim/pdp_100/lrc207.txt'
nodes= preprocess.read_node(filename)
draw.draw_original_nodes(nodes)
'''
save_pics.save_all_pics()