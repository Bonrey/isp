import copy

from some import *


class Phi:
    def __init__(self, code_blocks, nodes, graph, is_ascii):
        self.nodes = nodes
        self.graph = graph
        self.phi_char = "phi"
        self.is_ascii = is_ascii
        if not self.is_ascii:
            self.phi_char = 'φ'
        self.code_blocks = copy.deepcopy(code_blocks)
        for i in range(len(nodes)):
            if not graph.available[i]:
                self.code_blocks[i] = ["pass"]
        self.globs = set()
        self.blocks = {}
        show_table(self.globals_blocks())
        # show_set(self.globs, "Global variables")
        self.phi_args = [set() for _ in range(self.graph.N)]
        self.locate()
        show_table(self.table_new_phi())
        self.phis = [{var: [0, []] for var in sorted(self.phi_args[block])} for block in range(self.graph.N)]
        # print(self.phis)
        self.counter = {var: 0 for var in self.globs}
        self.stack = {var: [] for var in self.globs}
        self.tab_str = " " * 4
        print("```")
        self.rename(0)
        print("```")
        print()
        self.add_phi()
        show_blocks(self.code_blocks)

    def new_name(self, var):
        idx = self.counter[var]
        self.counter[var] += 1
        self.stack[var].append(idx)
        # print('```')
        # show_table(self.stack_table())
        # print('```')
        return idx

    def globals_blocks(self):
        print('```')
        for node in range(len(self.nodes)):
            if self.graph.available[node]:
                print(f'{self.nodes[node]}-block:')
                def_block = set()
                show_set(def_block, f"\tdef_{self.nodes[node]}", True)
                for line in self.code_blocks[node]:
                    print(f'\t{line}')
                    used, changed, _ = parse_vars(line)
                    for var in used.union(changed).difference(self.blocks.keys()):
                        if var not in self.blocks:
                            self.blocks[var] = set()
                    for var in used:
                        if var not in def_block:
                            self.globs.add(var)
                            show_set(self.globs, f"\t\tGlobals", True)
                    for var in changed:
                        def_block.add(var)
                        show_set(def_block, f"\t\tdef_{self.nodes[node]}", True)
                        self.blocks[var].add(node)
                        show_set([self.nodes[block] for block in self.blocks[var]], f"\t\tBlocks({var})", True)
        print('```')
        print()
        columns = ["var ="] + sorted(self.blocks)
        table = []
        row = ["Blocks(var)"]
        for var in columns[1:]:
            if self.blocks[var]:
                row.append(', '.join(sorted([self.graph.keys[block] for block in self.blocks[var]])))
            else:
                row.append('None')
        table.append(row)
        row = ["is Global"]
        for var in columns[1:]:
            row.append(var in self.globs)
        table.append(row)
        return table, columns

    def locate(self):
        print('```')
        for var in self.globs:
            print(f'variable {var}:')
            work_list = list(self.blocks[var])
            show_set([self.nodes[block] for block in work_list], "\tWorkList", True)
            item = 0
            n = len(work_list)
            while item < n:
                for df in self.graph.dfs[work_list[item]]:
                    if var not in self.phi_args[df]:
                        print(f"\tinsert {self.phi_char}(*{var}) in {self.nodes[df]}-block")
                        self.phi_args[df].add(var)
                    if df not in work_list:
                        work_list.append(df)
                        show_set([self.nodes[block] for block in work_list], "\tWorkList", True)
                        n += 1
                item += 1
        print('```')
        print()

    def rename_phi(self, block, tabs):
        if not self.phis[block]:
            print((tabs + 1) * self.tab_str + f'no {self.phi_char}-functions')
        else:
            print((tabs + 1) * self.tab_str + f'rename {self.phi_char}-functions:')
            for phi in self.phis[block]:
                self.phis[block][phi][0] = self.new_name(phi)
                print((tabs + 2) * self.tab_str + show_phi(self.phis[block][phi], phi, self.phi_char, self.is_ascii))

    def rename_instructions(self, block, tabs):
        new_block = []
        has_instructions = False
        for line in self.code_blocks[block]:
            used, changed, new_line = parse_vars(line)
            if used.union(changed).intersection(self.globs):
                if not has_instructions:
                    has_instructions = True
                    print((tabs + 1) * self.tab_str + 'rename instructions:')
                for i in range(len(new_line)):
                    if type(new_line[i]) is list and not new_line[i][0]:
                        var = list(used)[new_line[i][1]]
                        if var in self.globs:
                            if not self.stack[var]:
                                idx = self.new_name(var)
                            else:
                                idx = self.stack[var][-1]
                            var = var + sub(idx, self.is_ascii)
                        if new_line[i][-1]:
                            var += ','
                        new_line[i] = var
                for i in range(len(new_line)):
                    if type(new_line[i]) is list and new_line[i][0]:
                        var = list(changed)[new_line[i][1]]
                        if var in self.globs:
                            idx = self.new_name(var)
                            var = var + sub(idx, self.is_ascii)
                        if new_line[i][-1]:
                            var += ','
                        new_line[i] = var
                print((tabs + 2) * self.tab_str + ' '.join(new_line))
            for i in range(len(new_line)):
                if type(new_line[i]) is list:
                    var = list(used)[new_line[i][1]]
                    if new_line[i][-1]:
                        var += ','
                    new_line[i] = var
            new_block.append(' '.join(new_line))
        if not has_instructions:
            print((tabs + 1) * self.tab_str + 'no instructions')
        return new_block

    def fill(self, successor, tabs):
        print((tabs + 1) * self.tab_str + f'fill({self.nodes[successor]}):')
        if not self.phis[successor]:
            print((tabs + 2) * self.tab_str + f'no {self.phi_char}-functions')
        else:
            # print((tabs + 1) * tab_str + 'rename phi-functions')
            for phi in self.phis[successor]:
                if not self.stack[phi]:
                    self.new_name(phi)
                self.phis[successor][phi][1].append(self.stack[phi][-1])
                print(
                    (tabs + 2) * self.tab_str + show_phi(self.phis[successor][phi], phi, self.phi_char, self.is_ascii))

    def rename(self, block, tabs=0):
        new_block = []
        print(tabs * self.tab_str + f'Rename({self.nodes[block]}):')
        self.rename_phi(block, tabs)
        new_block += self.rename_instructions(block, tabs)
        for successor in self.graph.edges[block]:
            self.fill(successor, tabs)
        for successor in self.graph.dom_edges[block]:
            self.rename(successor, tabs + 1)
            print((tabs + 2) * self.tab_str + f'return to {self.nodes[block]};')
        # print('```')
        # show_table(self.stack_table())
        # print('```')
        self.clean(block, tabs)
        # print('```')
        # show_table(self.stack_table())
        # print('```')
        self.code_blocks[block] = new_block

    def add_phi(self):
        for block in range(self.graph.N):
            if self.phis[block]:
                new_block = []
                for phi in self.phis[block]:
                    new_block.append(show_phi(self.phis[block][phi], phi, self.phi_char, self.is_ascii))
                if self.code_blocks[block] and self.code_blocks[block][0][0] == 'L':
                    first_line = self.code_blocks[block][0].split(': ')
                    new_block[0] = first_line[0] + ': ' + new_block[0]
                    self.code_blocks[block][0] = ': '.join(first_line[1:])
                self.code_blocks[block] = new_block + self.code_blocks[block]

    def table_new_phi(self):
        columns = ["block ="] + self.nodes
        table = []
        for var in sorted(self.blocks):
            row = [var]
            for i in range(len(self.nodes)):
                if var in self.phi_args[i]:
                    row.append(' + ')
                else:
                    row.append(' - ')
            table.append(row)
        return table, columns, f"Needs a {self.phi_char}-function:"

    def clean(self, block, tabs):
        print((tabs + 1) * self.tab_str + 'clean();')
        for phi in self.phis[block]:
            self.stack[phi].pop()
        has_instructions = False
        for line in self.code_blocks[block]:
            used, changed, new_line = parse_vars(line)
            if used or changed:
                if not has_instructions:
                    has_instructions = True
                for var in changed.intersection(self.globs):
                    self.stack[var].pop()

    def stack_table(self):
        columns = ["vars ="] + list(self.globs)
        table = []
        row = ["counter"]
        max_stack = 0
        for var in self.counter:
            row.append(self.counter[var])
            if max_stack < len(self.stack[var]):
                max_stack = len(self.stack[var])
        for i in range(max_stack):
            row = [i]
            for var in self.globs:
                if i < len(self.stack[var]):
                    row.append(f'{var}{sub(self.stack[var][i], self.is_ascii)}')
                else:
                    row.append(' - ')
            table.append(row)
        return table, columns
