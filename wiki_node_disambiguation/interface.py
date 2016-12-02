# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from wiki_node_disambiguation.models import WikipediaArticleObject, LatticeObject, SequenceScore
from wiki_node_disambiguation.make_lattice import make_lattice_object
from wiki_node_disambiguation.load_entity_model import load_entity_model
from typing import List, Tuple


def inter_plausible_sequence():
    """入力系列を形態素分割して、wiki nodeを特定して、ほんでもっともらしいwiki系列を求める
    """
    # TODO 形態素分割 tokenizerは関数objectとして引数にすること
    # computer_wiki_node_probability()を呼び出しする
    pass


def compute_wiki_node_probability(seq_wiki_article_name: List[WikipediaArticleObject],
                                  entity_vector_model: Word2Vec,
                                  is_use_cache: bool = True,
                                  is_sort_object: bool = True) -> List[SequenceScore]:
    """* What you can do
    - You can get sequence of wikipedia-article-names with its sequence-score

    入力を入れたら、もっとも確率的によさげな系列を出力する関数
    入力はwiki記事名の系列。入力の時点ですでに「記事名の展開」が完了していなくてはならない。なぜなら、word2vecモデルではredirect <-> 記事名の対応をつくることができないから
    """
    # step1 it constructs array of transition-matrix(from state-t until state-t+1)
    lattice_object = make_lattice_object(
        seq_wiki_article_name=seq_wiki_article_name,
        entity_vector_model=entity_vector_model,
        is_use_cache=is_use_cache
    )
    # step2 Lattice
    sequence_score_objects = lattice_object.get_score_routes()
    if is_sort_object: sequence_score_objects.sort(key=lambda obj: obj.sequence_score, reverse=True)

    return sequence_score_objects