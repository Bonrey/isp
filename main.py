import re
import sys

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = {}
        self.edges = []
        self._keys = nodes
        self._N = len(nodes)
        for i in range(self._N):
            self.nodes[nodes[i]] = i
        for i in range(self._N):
            self.edges.append([])
            for node in edges[i]:
                self.edges[i].append(self.nodes[node])

    def dom(self):
        self.doms = [{0} for _ in range(self._N)]
        for taboo in range(1, self._N):
            availables = self._components(taboo)
            for i in range(self._N):
                if not availables[i]:
                    self.doms[i].add(taboo)

    def idom(self):
        self.idoms = [None] * self._N
        for n in range(self._N):
            for i in self.doms[n]:
                flag = (i != n)
                for m in range(self._N):
                    if m != i and m != n and (i in self.doms[m]) and (m in self.doms[n]):
                        flag = False
                if flag:
                    self.idoms[n] = i

    def pred(self):
        self.preds = [set() for _ in range(self._N)]
        for i in range(self._N):
            for node in self.edges[i]:
                self.preds[node].add(i)

    def df(self):
        self.dfs = [set() for _ in range(self._N)]
        for i in range(self._N):
            if len(self.preds[i]) > 1:
                for pred in self.preds[i]:
                    curr_pred = pred
                    while curr_pred is not None and curr_pred != self.idoms[i]:
                        self.dfs[curr_pred].add(i)
                        curr_pred = self.idoms[curr_pred]

    def _components(self, taboo):
        edges = []
        for i in range(self._N):
            edges.append([])
            if i != taboo:
                for node in self.edges[i]:
                    if node != taboo:
                        edges[i].append(node)
        return dfs(edges, 0)

    def dom_tree(self):
        self.dom_edges = [set() for _ in range(self._N)]
        for i in range(self._N):
            if self.idoms[i] is not None:
                self.dom_edges[self.idoms[i]].add(i)
        edges = []
        for i in range(self._N):
            nodes = [self._keys[node] for node in sorted(self.dom_edges[i])]
            edges.append(nodes)
        return edges

    def get_table(self):
        columns = ["node="] + self._keys
        table = []
        dict = vars(self)
        for key in ['Pred', 'Dom', 'Idom', 'DF']:
            row = [key + '(node)']
            if key == 'Idom':
                for i in range(self._N):
                    if self.idoms[i] is not None:
                        row.append(f'{self._keys[self.idoms[i]]}')
                    else:
                        row.append(f'{self.idoms[i]}')
            else:
                for i in range(self._N):
                    nodes = [self._keys[node] for node in sorted(dict[key.lower() + 's'][i])]
                    if len(nodes) != 0:
                        row.append(', '.join(nodes))
                    else:
                        row.append(str(None))
            table.append(row)
        return pd.DataFrame(table, columns=columns)


def dfs(edges, start, visited=None):
    if visited is None:
        visited = [False] * len(edges)
    visited[start] = True
    for next in edges[start]:
        if not visited[next]:
            dfs(edges, next, visited)
    return visited


def draw(edges, dir_name):
    for i in range(100):
        G = nx.DiGraph()
        G.add_edges_from(edges)
        options = {
            'node_color': 'pink',
            'node_size': 1000,
            'width': 3,
            'arrowstyle': '->',
            'arrowsize': 12,
        }
        nx.draw_networkx(G, arrows=True, **options)
        plt.savefig(f'{dir_name}/{i}.png')
        plt.close()


def normal_edges(nodes, edges):
    n_edges = []
    for i in range(len(nodes)):
        for node in edges[i]:
            n_edges.append((nodes[i], node))
    n_edges += [('Entry', nodes[0]), (nodes[-1], 'Exit')]
    return n_edges


def parse(code):
    blocks = []
    block = []
    for line in code.split('\n'):
        if not line:
            continue
        if ':' in line:
            if block:
                blocks.append(block)
                block = []
        block.append(line)
        if 'goto' in line or 'if' in line:
            blocks.append(block)
            block = []
    if block:
        blocks.append(block)
    return blocks


def show_blocks(blocks):
    print("```")
    letter = 'A'
    linenum = 1
    print('Entry\n')
    for block in blocks:
        print('Block {} ({})'.format(letter, len(block)))
        letter = chr(ord(letter) + 1)
        for line in block:
            print('({}){}\t{}'.format(linenum, ' ' if linenum < 10 else '', line))
            linenum += 1
        print()
    print('Exit')
    print("```")
    print()


#def parse_edges():
#    n = len(blocks)
#    lables = {}
#    for i in range(n):
#        line = blocks[i][0]
#        if line[0] == 'L':
#            lables[line[1]] = chr(ord('A') + i)
#    edges = [[] for _ in range(len(blocks))]
#    for i in range(n):
#        line = blocks[i][-1]
#        if 'goto' in line:
#            edges[i].append(lables[re.findall(r'goto\s*L\d', line)[-1][-1]])
#        if 'if' in line or 'goto' not in line:
#            if i < n - 1:
#                edges[i].append(chr(ord('A') + i + 1))
#    return edges


if __name__ == '__main__':
    orig_stdout = sys.stdout
    f = open('ans.md', 'w')
    sys.stdout = f
    # data1
    nodes = ['Entry', 'A', 'B', 'C', 'D', 'E', 'Exit']
    edges = [['A'], ['B', 'C'], ['D'], ['D', 'E'], ['E'], ['A', 'Exit'], []]
    # nodes = []
    # edges = []
    # with open("input.txt", 'r') as code:
    #    blocks = parse(code.read())
    #    show_blocks(blocks)
    #    nodes += [chr(ord('A') + i) for i in range(len(blocks))]
    #    edges += parse_edges()
    #    with open("graph.txt", "w") as fout:
    #        fout.write(str(nodes) + '\n\n')
    #        for n in edges:
    #            fout.write(str(n) + '\n')

    draw(normal_edges(nodes, edges), "cfg")
    print("### Control Flow Graph")
    print()
    table = "| matplotlib | handmade  |\n|:---|:---|"
    print(table)
    print("| ![CFG_plt](cfg/1.png) | ![CFG](cfg/diagram_dt.png) |")
    print()
    graph = Graph(nodes, edges)
    graph.dom()
    graph.idom()
    graph.pred()
    draw(normal_edges(nodes, graph.dom_tree()), "dt")
    print("### Dominator Tree")
    print()
    print(table)
    print("| ![DT_plt](dt/1.png) | ![DT](dt/diagram_dt.png) |")
    print()
    graph.df()
    print(graph.get_table().to_markdown(index=False))
    sys.stdout = orig_stdout
    f.close()
