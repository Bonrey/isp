import sys

from graph import Graph
from some import *

if __name__ == '__main__':
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
    with open("input.txt", 'r') as code:
        blocks = parse(code.read())
        show_blocks(blocks)
        nodes += ['Entry'] + [chr(ord('A') + i) for i in range(len(blocks) - 2)] + ['Exit']
        edges += parse_edges(blocks)
        with open(os.path.join(out_dir, "graph.txt"), "w") as fout:
            fout.write(str(nodes) + '\n\n')
            for n in edges:
                fout.write(str(n) + '\n')

    draw(normal_edges(nodes, edges), "cfg", "### Control Flow Graph")
    graph = Graph(nodes, edges)
    sys.stdout = orig_stdout
    f.close()
