# graph

トランザクションデータから、gephi用gexfファイルを生成するコード。

トランザクションデータが日本語を含む場合は、networkxのwrite_gexfの仕様で文字化けしてしまうので、一度出力したファイルを読み込んで置換しています。

作成された temp.gexfファイルは消してしまってかまいません。
(後で削除するようにしよう。。)

### require
- python2.7
- module
  - sys
  - itertools
  - pandas
  - networkx(stable)
  - Counter

networkx/pandas はpipでインストールしてください。

### command

python convert2gexf.py <トランザクションデータファイル> > fuga.gexf

### トランザクションデータファイルの形式
以下の形式で保存してください。

    id,item
    1,hoge
    2,fuga
    3,hoge
