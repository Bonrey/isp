import os
import re

import pandas as pd

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
    if not os.path.exists(os.path.join("output", dir_name)):
        os.makedirs(os.path.join("output", dir_name))
    styles = [nx.draw_networkx, nx.draw_circular, nx.draw_kamada_kawai, nx.draw_random, nx.draw_spectral,
              nx.draw_spring, nx.draw_shell, nx.draw_planar]
    for style in styles:
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
        plt.savefig(os.path.join("output", dir_name, f"{str(style).split()[1]}.png"))
        plt.close()
    print("###", title)
    print()
    if is_table:
        print("| matplotlib | handmade  |\n|:---|:---|")
        print(f"| ![{dir_name.upper()}_plt]({dir_name}/draw_{default}.png) "
              f"| ![{dir_name.upper()}]({dir_name}/diagram_{dir_name}.png) |")
    else:
        print(f"![{dir_name.upper()}_plt]({dir_name}/draw_{default}.png)")
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


def parse_vars(code_line):
    commands = code_line.split()
    i = 0
    changed = set()
    used = set()
    is_changed = True
    new_line = []
    while i < len(commands):
        if commands[i][0] == 'L' or (commands[i] == 'goto' and i + 1 < len(commands)):
            new_line.append(commands[i])
        elif len(commands[i]) >= len('ifTrue') and commands[i][:2] == 'if' and i + 2 < len(commands):
            is_changed = False
            new_line.append(commands[i])
        elif (commands[i] == '<--' or commands[i] == 'return' or commands[i] == 'param') and i + 1 < len(commands):
            is_changed = False
            new_line.append(commands[i])
        elif commands[i][0].islower():
            var = commands[i]
            command = [is_changed, -1, False]
            if var[-1] == ',':
                var = var[:-1]
                command[-1] = True
            if is_changed:
                changed.add(var)
                command[1] = list(changed).index(var)
            else:
                used.add(var)
                command[1] = list(used).index(var)
            new_line.append(command)
        else:
            new_line.append(commands[i])
        i += 1
    return used, changed, new_line


def show_set(st, title, incode=False):
    if incode:
        print(title, ": {" + ', '.join(sorted(st)) + "}")
    else:
        print(title, ": ```{" + ', '.join(sorted(st)) + "}```")
        print()


def show_table(table):
    if len(table) > 2:
        print("###", table[2])
        print()
    print(pd.DataFrame(table[0], columns=table[1]).to_markdown(index=False))
    print()


def sub(num, is_ascii):
    if is_ascii:
        return f'_{num}'
    sub_chars = "₀₁₂₃₄₅₆₇₈₉"
    return ''.join([sub_chars[int(i)] for i in str(num)])


def show_phi(args, phi, phi_char, is_ascii):
    var = phi + sub(args[0], is_ascii)
    params = [phi + sub(idx, is_ascii) for idx in args[1]]
    return f"{var} <-- {phi_char}({', '.join(params)})"
