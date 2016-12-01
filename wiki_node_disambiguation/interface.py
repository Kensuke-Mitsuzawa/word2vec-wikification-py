# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from wiki_node_disambiguation.load_entity_model import load_entity_model
from typing import List, Tuple


def inter_plausible_sequence():
    """入力系列を形態素分割して、wiki nodeを特定して、ほんでもっともらしいwiki系列を求める
    """
    # TODO 形態素分割 tokenizerは関数objectとして引数にすること
    # TODO mysqlへのconnectorを用意すること
    # computer_wiki_node_probability()を呼び出しする
    pass


def computer_wiki_node_probability(seq_wiki_article_name:List[str],
                                   entity_vector_model:Word2Vec):
    """
    入力を入れたら、もっとも確率的によさげな系列を出力する関数
    入力はwiki記事名の系列
    """
    pass