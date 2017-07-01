# -*- coding: utf-8 -*-
import sys
import pandas as pd


# DataFrameの作成
def make_df(file):
    df = pd.read_csv(file)
    df = df.sort_values("id").reset_index(drop=True)
    return df


#ユニークな要素を抽出
def makeDataFrameNode(df):
    uniq_df = df.item.unique()
    # print uniq_df
    list_node = []
    list_size = []
    for i in uniq_df:
        size = df[df['item'] == i].item.count()
        list_node.append(i)
        list_size.append(size)
    node = pd.DataFrame(columns=['node', 'size'])
    node = pd.DataFrame({'node': list_node, 'size': list_size})
    return node


def printNodeXEXF(df):
    header = '''
<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.1draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">
<graph>
<nodes>
'''
    footer = '''
</nodes>
</graph>
</gexf>
'''
    print header
    print footer
#    for item in df.node:
#        print '<node id="a" label="' + item + '">'
#        print '<viz:size value="' + size + '"/>'
    print df
    for i in df.iterrows():
        node = df.node.ix[i]
        print node


# idにマッチするitemを表示
def search_data(df, uniqids):
    for i in uniqids:
        str = ""
        count = 0
        for d in df.item[(df.id == i)]:
            count += 1
            if count > 1:
                str += ","
            str += "\"" + d + "\""
        print str


# main
def main():
    df = make_df(argvs[1])
    df_node = makeDataFrameNode(df)
    printNodeXEXF(df_node)


if __name__ == '__main__':
    # arguments
    argvs = sys.argv
    # check
    if len(argvs) != 2:
        print "Usage: python main.py [hoge.csv]"
        exit()
    main()
