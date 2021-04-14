import os
import re

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
            print('Block {} ({})'.format(letter, len(block)))
            letter = chr(ord(letter) + 1)
            for line in block:
                print('({}){}\t{}'.format(line_num, ' ' if line_num < 10 else '', line))
                line_num += 1
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


def draw(edges, dir_name, title, copys=10):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for i in range(copys):
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
        plt.savefig(os.path.join(dir_name, f"{i}.png"))
        plt.close()
    print(title)
    print()
    print("| matplotlib | handmade  |\n|:---|:---|")
    print(f"| ![{dir_name.upper()}_plt](../{dir_name}/1.png) | ![CFG](../{dir_name}/diagram_{dir_name}.png) |")
    print()


def normal_edges(nodes, edges):
    n_edges = []
    for i in range(len(nodes)):
        for node in edges[i]:
            n_edges.append((nodes[i], node))
    n_edges += [('Entry', nodes[0]), (nodes[-1], 'Exit')]
    return n_edges
