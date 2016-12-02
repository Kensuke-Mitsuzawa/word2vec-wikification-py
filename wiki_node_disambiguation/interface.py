# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from wiki_node_disambiguation.models import WikipediaArticleObject
from wiki_node_disambiguation.load_entity_model import load_entity_model
from typing import List, Tuple


def inter_plausible_sequence():
    """入力系列を形態素分割して、wiki nodeを特定して、ほんでもっともらしいwiki系列を求める
    """
    # TODO 形態素分割 tokenizerは関数objectとして引数にすること
    # TODO mysqlへのconnectorを用意すること
    # computer_wiki_node_probability()を呼び出しする
    pass


def computer_wiki_node_probability(seq_wiki_article_name:List[WikipediaArticleObject],
                                   entity_vector_model:Word2Vec):
    """
    入力を入れたら、もっとも確率的によさげな系列を出力する関数
    入力はwiki記事名の系列。入力の時点ですでに「記事名の展開」が完了していなくてはならない。なぜなら、word2vecモデルではredirect <-> 記事名の対応をつくることができないから
    """
    pass
    # step1 it constructs array of transition-matrix(from state-t until state-t+1)

    # step2 系列とstate間のスコアを保持するオブジェクトを生成する

