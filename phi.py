import copy

from some import *


class Phi:
    def __init__(self, code_blocks, nodes, graph):
        self.nodes = nodes
        self.graph = graph
        self.code_blocks = copy.deepcopy(code_blocks)
        self.globs = set()
        self.blocks = {}
        show_table(self.globals_blocks())
        show_set(self.globs, "Global variables")
        self.phis = [set() for _ in range(self.graph.N)]
        self.locate()
        # print(self.phis)
        self.counter = {var: 0 for var in self.globs}
        self.stack = {var: [] for var in self.globs}
        print("```")
        self.rename(0)
        print("```")

    def new_name(self, var):
        idx = self.counter[var]
        self.counter[var] += 1
        self.stack[var].append(idx)
        return idx

    def globals_blocks(self):
        for node in tqdm.tqdm(range(len(self.nodes)), desc="Globals & Blocks", ncols=100, colour='green'):
            if self.graph.available[node]:
                def_block = set()
                for line in self.code_blocks[node]:
                    used, changed, _ = parse_vars(line)
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

    def rename(self, block, tabs=0):
        new_block = []
        tab_str = " " * 4
        print(tabs * tab_str + f'Rename({self.nodes[block]})')
        if not self.phis[block]:
            print((tabs + 1) * tab_str + 'no phi-functions')
        else:
            print((tabs + 1) * tab_str + 'rename phi-functions')
            for phi in self.phis[block]:
                var = self.new_name(phi)
                ...
        has_instructions = False
        for line in self.code_blocks[block]:
            used, changed, new_line = parse_vars(line)
            if used.union(changed).intersection(self.globs):
                if not has_instructions:
                    has_instructions = True
                    print((tabs + 1) * tab_str + 'rename instructions')
                for i in range(len(new_line)):
                    if type(new_line[i]) is list and not new_line[i][0]:
                        var = list(used)[new_line[i][1]]
                        if var in self.globs:
                            if not self.stack[var]:
                                idx = self.new_name(var)
                            else:
                                idx = self.stack[var][-1]
                            var = var + sub(idx)
                        if new_line[i][-1]:
                            var += ','
                        new_line[i] = var
                for i in range(len(new_line)):
                    if type(new_line[i]) is list and new_line[i][0]:
                        var = list(changed)[new_line[i][1]]
                        if var in self.globs:
                            idx = self.new_name(var)
                            var = var + sub(idx)
                        if new_line[i][-1]:
                            var += ','
                        new_line[i] = var
                print((tabs + 2) * tab_str + ' '.join(new_line))
            new_block.append(''.join(new_line))
        if not has_instructions:
            print((tabs + 1) * tab_str + 'no instructions')
        for successor in self.graph.edges[block]:
            print((tabs + 1) * tab_str + f'fill({self.nodes[successor]})')
            ...
        for successor in self.graph.dom_edges[block]:
            self.rename(successor, tabs + 1)
        if not self.phis[block]:
            print((tabs + 1) * tab_str + 'no phi-functions')
        else:
            print((tabs + 1) * tab_str + 'pop for each phi-functions')
            for phi in self.phis[block]:
                self.stack[phi].pop()
        has_instructions = False
        for line in self.code_blocks[block]:
            used, changed, new_line = parse_vars(line)
            if used or changed:
                if not has_instructions:
                    has_instructions = True
                    print((tabs + 1) * tab_str + 'pop for each instructions')
                for var in changed:
                    self.stack[var].pop()