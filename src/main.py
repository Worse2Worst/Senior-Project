from pdp_lib import draw

from pdp_lib import preprocess

filename='pdp_instances/LiLim/pdp_100/lrc207.txt'
#os.chdir("C:/Users/Worse2Worst/Desktop/Senior-Project")
    #for file in glob.glob("*.txt"):
nodes= preprocess.read_node(filename)
draw.draw_original_nodes(nodes, filename)
