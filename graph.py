from some import *


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = {}
        self.edges = []
        self.keys = nodes
        self.N = len(nodes)
        for i in range(self.N):
            self.nodes[nodes[i]] = i
        for i in range(self.N):
            self.edges.append([])
            for node in edges[i]:
                self.edges[i].append(self.nodes[node])
        self.available = dfs(self.edges, 0)
        db = [self.keys[i] for i in range(self.N) if not self.available[i]]
        if db:
            show_set(db, "Detached blocks")
        draw(normal_edges(nodes, edges, self.available), "cfg", "Control Flow Graph")
        self.doms = [{0} for _ in range(self.N)]
        self.dom()
        self.idoms = [None] * self.N
        self.idom()
        self.preds = [set() for _ in range(self.N)]
        self.pred()
        self.dfs = [set() for _ in range(self.N)]
        self.df()
        self.dom_edges = [set() for _ in range(self.N)]
        draw(normal_edges(nodes, self.dom_tree(), self.available), "dt", "Dominator Tree")
        show_table(self.get_table())

    def dom(self):
        for taboo in range(1, self.N):
            if self.available[taboo]:
                availables = self._components(taboo)
                for i in range(self.N):
                    if not availables[i]:
                        self.doms[i].add(taboo)

    def idom(self):
        for n in range(self.N):
            if self.available[n]:
                for i in self.doms[n]:
                    flag = (i != n)
                    for m in range(self.N):
                        if m != i and m != n and (i in self.doms[m]) and (m in self.doms[n]):
                            flag = False
                    if flag:
                        self.idoms[n] = i

    def pred(self):
        for i in range(self.N):
            if self.available[i]:
                for node in self.edges[i]:
                    self.preds[node].add(i)

    def df(self):
        for i in range(self.N):
            if self.available[i]:
                if len(self.preds[i]) > 1:
                    for pred in self.preds[i]:
                        curr_pred = pred
                        while curr_pred is not None and curr_pred != self.idoms[i]:
                            self.dfs[curr_pred].add(i)
                            curr_pred = self.idoms[curr_pred]

    def _components(self, taboo):
        edges = []
        for i in range(self.N):
            edges.append([])
            if i != taboo:
                for node in self.edges[i]:
                    if node != taboo:
                        edges[i].append(node)
        return dfs(edges, 0)

    def dom_tree(self):
        for i in range(self.N):
            if self.idoms[i] is not None:
                self.dom_edges[self.idoms[i]].add(i)
        edges = []
        for i in range(self.N):
            nodes = [self.keys[node] for node in sorted(self.dom_edges[i])]
            edges.append(nodes)
        return edges

    def get_table(self):
        columns = ["node ="]
        for i in range(self.N):
            if self.available[i]:
                columns.append(self.keys[i])
        table = []
        _dict = vars(self)
        for key in ['Pred', 'Dom', 'Idom', 'DF']:
            row = [key + '(node)']
            for i in range(self.N):
                if self.available[i]:
                    if key == 'Idom':
                        if self.idoms[i] is not None:
                            row.append(f'{self.keys[self.idoms[i]]}')
                        else:
                            row.append(f'{self.idoms[i]}')
                    else:
                        nodes = [self.keys[node] for node in sorted(_dict[key.lower() + 's'][i])]
                        if len(nodes) != 0:
                            row.append(', '.join(nodes))
                        else:
                            row.append(str(None))
            table.append(row)
        return table, columns
