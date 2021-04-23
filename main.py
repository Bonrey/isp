import sys

from graph import Graph
from phi import Phi
from some import *

if __name__ == '__main__':
    input_file = "input/input_2.txt"
    is_ascii = False
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "-ascii":
        is_ascii = True
    out_dir = "output"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    orig_stdout = sys.stdout
    f = open(os.path.join(out_dir, 'ans.md'), 'w')
    sys.stdout = f
    # nodes = ['Entry', 'A', 'B', 'C', 'D', 'E', 'Exit']
    # edges = [['A'], ['B', 'C'], ['D'], ['D', 'E'], ['E'], ['A', 'Exit'], []]
    nodes = []
    edges = []
    with open(input_file, 'r') as code:
        code_blocks = parse(code.read())
        show_blocks(code_blocks)
        nodes += ['Entry'] + [chr(ord('A') + i) for i in range(len(code_blocks) - 2)] + ['Exit']
        edges += parse_edges(code_blocks)
    graph = Graph(nodes, edges)
    phi = Phi(code_blocks, nodes, graph, is_ascii)

    sys.stdout = orig_stdout
    f.close()
