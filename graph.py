import pandas as pd

from some import *


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
        self.doms = [{0} for _ in range(self._N)]
        self.dom()
        self.idoms = [None] * self._N
        self.idom()
        self.preds = [set() for _ in range(self._N)]
        self.pred()
        self.dfs = [set() for _ in range(self._N)]
        self.df()
        self.dom_edges = [set() for _ in range(self._N)]
        draw(normal_edges(nodes, self.dom_tree()), "dt", "Dominator Tree")
        print(self.get_table().to_markdown(index=False))

    def dom(self):
        for taboo in tqdm.tqdm(range(1, self._N), desc="Dom", ncols=100, colour='green'):
            availables = self._components(taboo)
            for i in range(self._N):
                if not availables[i]:
                    self.doms[i].add(taboo)

    def idom(self):
        for n in tqdm.tqdm(range(self._N), desc="IDom", ncols=100, colour='green'):
            for i in self.doms[n]:
                flag = (i != n)
                for m in range(self._N):
                    if m != i and m != n and (i in self.doms[m]) and (m in self.doms[n]):
                        flag = False
                if flag:
                    self.idoms[n] = i

    def pred(self):
        for i in tqdm.tqdm(range(self._N), desc="Pred", ncols=100, colour='green'):
            for node in self.edges[i]:
                self.preds[node].add(i)

    def df(self):
        for i in tqdm.tqdm(range(self._N), desc="Dominance Frontier", ncols=100, colour='green'):
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
        for i in tqdm.tqdm(range(self._N), desc="Dom Tree", ncols=100, colour='green'):
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
        for key in tqdm.tqdm(['Pred', 'Dom', 'Idom', 'DF'], desc="Table", ncols=100, colour='green'):
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
