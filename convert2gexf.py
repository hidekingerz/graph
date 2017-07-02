# -*- coding: utf-8 -*-
import sys
import itertools
import pandas as pd
import networkx as nx
from collections import Counter


# DataFrameの作成
def makeDataFrame(file):
    df = pd.read_csv(file)
    df = df.sort_values("id").reset_index(drop=True)
    return df


# gfをいれて、ノードのラベルに合致するidを返す
def convertNodeLabelToID(gf, nodelabel):
    gf_nodelist = gf.nodes(data=True)
    for node in gf_nodelist:
        if nodelabel == node[1]['label']:
            return node[0]


# gfをいれて、ノードのIDに合致するラベルを返す
def convertNodeIDToLabel(gf, nodeid):
    gf_nodelist = gf.nodes(data=True)
    for node in gf_nodelist:
        if nodeid == node[0]:
            return node[1]['label']


# dfをいれて、ノードIDを作成する
def makeNodeIDLists(df, gf, list_node):
    list_id = []
    for label in list_node:
        list_id.append(convertNodeLabelToID(gf, label))
    return list_id


# dfをいれて、ノードのリストを作成する
def makeNodeLists(df):
    list_node = []
    for i in df.item.unique():
        list_node.append(i)
    return list_node


# dfをいれて、ノードのサイズを作成する
def makeNodeSizeLists(df):
    list_size = []
    for i in df.item.unique():
        size = df[df['item'] == i].item.count()
        list_size.append(size)
    return list_size


# DFからユニーク要素を抽出して、networkxのノード情報を作成
def makeNodes(df):
    list_node = makeNodeLists(df)
    list_size = makeNodeSizeLists(df)
    df_node = pd.DataFrame(columns=['node', 'size'])
    df_node = pd.DataFrame({'node': list_node, 'size': list_size})
    gf = nx.Graph()
    for index, row in df_node.iterrows():
        gf.add_node(index, label=row['node'])
        gf.node[index]['viz'] = {'size': row['size']}
    return gf


# DF からエッジ情報を抽出して、networkxのエッジ情報を作成
def makeEdges(df, gf):
    list_edges = []
    for i in df.id.unique():
        list_trans = []
        if df[df['id'] == i].item.count() > 1:
            for index, row in df[df['id'] == i].iterrows():
                list_trans.append(row['item'])
            # 順列を要素2までで作成
            list_permutations = list(itertools.permutations(list_trans, 2))
            for permutation in list_permutations:
                list_edges.append(permutation)
    counter = Counter(list_edges)
    for edge, cnt in counter.most_common():
        id_src = convertNodeLabelToID(gf, edge[0])
        id_dst = convertNodeLabelToID(gf, edge[1])
        gf.add_edge(id_src, id_dst, weight=cnt)
    return gf


def outputGEXF(df, gf):
    nx.write_gexf(gf, 'temp.gexf', encoding='utf-8')
    list_id = makeNodeIDLists(df, gf, makeNodeLists(df))
    with open('temp.gexf') as lines:
        for line in lines:
            text = line.rstrip('\r\n')
            for i in list_id:
                elem = '      <node id="' + str(i) + '"'
                if elem in text:
                    label = convertNodeIDToLabel(gf, i)
                    replace_elem = elem + ' label="' + str(label) + '">'
                    text = replace_elem
                    break
            print text


# main
def main():
    df = makeDataFrame(argvs[1])
    gf_node = makeNodes(df)
    gf = makeEdges(df, gf_node)
    outputGEXF(df, gf)


if __name__ == '__main__':
    # arguments
    argvs = sys.argv
    # check
    if len(argvs) != 2:
        print "Usage: python main.py [hoge.csv]"
        exit()
    main()
