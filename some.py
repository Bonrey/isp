import os
import re

import pandas as pd
import tqdm

import networkx as nx
import matplotlib.pyplot as plt


def show_blocks(blocks):
    print("```")
    letter = 'A'
    line_num = 1
    borders = ['Entry', 'Exit']
    iscode = -1
    for block in blocks:
        if not block:
            print(borders[iscode + 1])
            iscode += 1
        else:
            print('Block {} [{}]'.format(letter, len(block)))
            letter = chr(ord(letter) + 1)
            for line in block:
                print('({}){}\t{}'.format(line_num, ' ' if line_num < 10 else '', line))
                line_num += 1
        if iscode < 1:
            print()
    print("```")
    print()


def parse_edges(blocks):
    n = len(blocks)
    lables = {}
    for i in range(n):
        line = "not a code line"
        if blocks[i]:
            line = blocks[i][0]
        if line[0] == 'L':
            lables[line[1]] = chr(ord('A') + i - 1)
    edges = [[] for _ in range(len(blocks))]
    for i in range(n):
        line = "not a code line"
        if blocks[i]:
            line = blocks[i][-1]
        if 'goto' in line:
            edges[i].append(lables[re.findall(r'goto\s*L\d', line)[-1][-1]])
        if 'if' in line or 'goto' not in line:
            if i < n - 2:
                edges[i].append(chr(ord('A') + i))
            if i == n - 2:
                edges[i].append("Exit")
    return edges


def parse(code):
    blocks = [[]]
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
    blocks.append([])
    return blocks


def draw(edges, dir_name, title, default='planar', is_table=False):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    styles = [nx.draw_networkx, nx.draw_circular, nx.draw_kamada_kawai, nx.draw_random, nx.draw_spectral,
              nx.draw_spring, nx.draw_shell, nx.draw_planar]
    for style in tqdm.tqdm(styles, desc=title, ncols=100, colour='green'):
        G = nx.DiGraph()
        G.add_edges_from(edges)
        options = {
            'node_color': 'pink',
            'node_size': 1000,
            'width': 3,
            'arrowstyle': '->',
            'arrowsize': 12,
            'with_labels': True,
            'arrows': True
        }
        style(G, **options)
        plt.savefig(os.path.join(dir_name, f"{str(style).split()[1]}.png"))
        plt.close()
    print("###", title)
    print()
    if is_table:
        print("| matplotlib | handmade  |\n|:---|:---|")
        print(f"| ![{dir_name.upper()}_plt](../{dir_name}/draw_{default}.png) "
              f"| ![{dir_name.upper()}](../{dir_name}/diagram_{dir_name}.png) |")
    else:
        print(f"![{dir_name.upper()}_plt](../{dir_name}/draw_{default}.png)")
    print()


def normal_edges(nodes, edges, available=None):
    n_edges = []
    for i in range(len(nodes)):
        if not available or available[i]:
            for node in edges[i]:
                n_edges.append((nodes[i], node))
    return n_edges


def dfs(edges, start, visited=None):
    if visited is None:
        visited = [False] * len(edges)
    visited[start] = True
    for next in edges[start]:
        if not visited[next]:
            dfs(edges, next, visited)
    return visited


def globals_blocks(nodes, code_blocks, available):
    globs = set()
    blocks = {}
    for node in tqdm.tqdm(range(len(nodes)), desc="Globals & Blocks", ncols=100, colour='green'):
        if available[node]:
            def_block = set()
            for line in code_blocks[node]:
                commands = line.split()
                i = 0
                changed = set()
                used = set()
                is_changed = True
                while i < len(commands):
                    if commands[i][0] == 'L' or \
                            ((commands[i] == 'goto' or commands[i] == 'param') and i + 1 < len(commands)):
                        pass
                    elif len(commands[i]) >= len('ifTrue') and commands[i][:2] == 'if' and i + 2 < len(commands):
                        is_changed = False
                    elif (commands[i] == '<--' or commands[i] == 'return') and i + 1 < len(commands):
                        is_changed = False
                    elif commands[i][0].islower():
                        var = commands[i]
                        if var[-1] == ',':
                            var = var[:-1]
                        if var not in blocks:
                            blocks[var] = set()
                        if is_changed:
                            changed.add(var)
                        else:
                            used.add(var)
                    else:
                        pass
                    i += 1
                for var in used:
                    if var not in def_block:
                        globs.add(var)
                for var in changed:
                    def_block.add(var)
                    blocks[var].add(nodes[node])
    print("Global variables : ```{" + ', '.join(sorted(globs)) + "}```")
    print()
    columns = ["var ="] + sorted(blocks)
    table = []
    row = ["Blocks(var)"]
    for var in columns[1:]:
        if blocks[var]:
            row.append(', '.join(sorted(blocks[var])))
        else:
            row.append('None')
    table.append(row)
    print(pd.DataFrame(table, columns=columns).to_markdown(index=False))
    print()
    return globs, blocks
