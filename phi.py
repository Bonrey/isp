from some import *


class Phi:
    def __init__(self, code_blocks, nodes, graph):
        self.nodes = nodes
        self.graph = graph
        self.code_blocks = code_blocks
        self.globs = set()
        self.blocks = {}
        show_table(self.globals_blocks())
        show_set(self.globs, "Global variables")
        self.phis = [set() for _ in range(self.graph.N)]
        self.locate()
        print(self.phis)

    def globals_blocks(self):
        for node in tqdm.tqdm(range(len(self.nodes)), desc="Globals & Blocks", ncols=100, colour='green'):
            if self.graph.available[node]:
                def_block = set()
                for line in self.code_blocks[node]:
                    used, changed = parse_vars(line)
                    for var in used.union(changed).difference(self.blocks.keys()):
                        if var not in self.blocks:
                            self.blocks[var] = set()
                    for var in used:
                        if var not in def_block:
                            self.globs.add(var)
                    for var in changed:
                        def_block.add(var)
                        self.blocks[var].add(node)
        columns = ["var ="] + sorted(self.blocks)
        table = []
        row = ["Blocks(var)"]
        for var in columns[1:]:
            if self.blocks[var]:
                row.append(', '.join(sorted([self.graph.keys[block] for block in self.blocks[var]])))
            else:
                row.append('None')
        table.append(row)
        return table, columns

    def locate(self):
        for var in tqdm.tqdm(self.globs, desc="Locate phi functions", ncols=100, colour='green'):
            work_list = list(self.blocks[var])
            item = 0
            n = len(work_list)
            while item < n:
                for df in self.graph.dfs[work_list[item]]:
                    self.phis[df].add(var)
                    if df not in work_list:
                        work_list.append(df)
                        n += 1
                item += 1

    def ssa(self):
        ...
