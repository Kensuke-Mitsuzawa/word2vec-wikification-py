from numpy import ndarray
from gensim.models import Word2Vec
from word2vec_wikification_py import init_logger
from word2vec_wikification_py.models import WikipediaArticleObject, PersistentDict, LatticeObject, IndexDictionaryObject, EdgeObject
from typing import List, Tuple, Union, Any, Dict
from tempfile import mkdtemp
from scipy.sparse import csr_matrix
import os
import logging
logger = logging.getLogger(name=init_logger.LOGGER_NAME)


class TransitionEdgeObject(object):
    __slots__ = ['row_index', 'column_index', 'transition_score']

    def __init__(self,
                 row_index:int,
                 column_index:int,
                 transition_score:float):
        self.row_index = row_index
        self.column_index = column_index
        self.transition_score = transition_score


def __update_index_dictionary(key:Tuple[int,str], index_dictionary:Dict[Tuple[int,str],int])->Dict[Tuple[int,str],int]:
    """
    """
    if key in index_dictionary:
        raise Exception('The key is already existing in index_dictionary. key={}'.format(key))
    else:
        if len(index_dictionary)==0:
            index_dictionary[key] = 0
        else:
            latest_index_number = max(index_dictionary.values())
            index_dictionary[key] = latest_index_number + 1

        return index_dictionary


def make_state_transition_edge(state_t_word_tuple:Tuple[int,str],
                               state_t_plus_word_tuple:Tuple[int,str],
                               state2index_obj:IndexDictionaryObject,
                               entity_vector:Word2Vec)->Tuple[TransitionEdgeObject, IndexDictionaryObject]:
    """* What you can do
    - tの単語xからt+1の単語x'への遷移スコアを計算する

    * Output
    - tuple object whose element is (transition_element, row2index, column2index)
    - transition_element is (row_index, column_index, transition_score)
    """
    if not state_t_word_tuple[1] in entity_vector.vocab:
        raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_word_tuple))
    if not state_t_plus_word_tuple[1] in entity_vector.vocab:
        raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_plus_word_tuple))

    transition_score = entity_vector.similarity(state_t_word_tuple[1], state_t_plus_word_tuple[1])  # type: float

    if state_t_word_tuple in state2index_obj.state2index['row2index']:
        row_index = state2index_obj.state2index['row2index'][state_t_word_tuple]  # type: int
    else:
        state2index_obj.state2index['row2index'] = __update_index_dictionary(state_t_word_tuple, state2index_obj.state2index['row2index'])
        row_index = state2index_obj.state2index['row2index'][state_t_word_tuple]  # type: int

    if state_t_plus_word_tuple in state2index_obj.state2index['column2index']:
        column_index = state2index_obj.state2index['column2index'][state_t_plus_word_tuple]  # type: int
    else:
        state2index_obj.state2index['column2index'] = __update_index_dictionary(state_t_plus_word_tuple, state2index_obj.state2index['column2index'])
        column_index = state2index_obj.state2index['column2index'][state_t_plus_word_tuple]  # type: int

    transition_edge_obj = TransitionEdgeObject(row_index=row_index,
                                               column_index=column_index,
                                               transition_score=transition_score)

    return (transition_edge_obj, state2index_obj)


def make_state_transition(index:int,
                          seq_wiki_article_name:List[WikipediaArticleObject],
                          state2index_obj:IndexDictionaryObject,
                          entity_vector_model:Word2Vec)->Tuple[List[EdgeObject], List[TransitionEdgeObject]]:
    """* What you can do
    - You make all state-information between state_index and state_index_plus_1
    """
    edge_group = []  # type: List[EdgeObject]
    seq_transition_element = []  # type: List[TransitionEdgeObject]

    for candidate_wikipedia_article_name in seq_wiki_article_name[index].candidate_article_name:
        for candiate_wikipedia_article_name_state_plus in seq_wiki_article_name[index + 1].candidate_article_name:
            state_t_word_tuple = (index, candidate_wikipedia_article_name)
            state_t_plus_word_tuple = (index + 1, candiate_wikipedia_article_name_state_plus)
            transition_element, state2index_obj = make_state_transition_edge(
                state_t_word_tuple=state_t_word_tuple,
                state_t_plus_word_tuple=state_t_plus_word_tuple,
                state2index_obj=state2index_obj,
                entity_vector=entity_vector_model
            )
            seq_transition_element.append(transition_element)
            edge_group.append( EdgeObject(state2index_obj.state2index['row2index'][state_t_word_tuple],
                                          state2index_obj.state2index['column2index'][state_t_plus_word_tuple])
                               )

    return (edge_group, seq_transition_element)


def make_state_transition_sequence(seq_wiki_article_name:List[WikipediaArticleObject],
                                   entity_vector_model:Word2Vec,
                                   state2index_obj: IndexDictionaryObject)->Tuple[IndexDictionaryObject,
                                                                                  List[List[EdgeObject]],
                                                                                  csr_matrix]:
    """系列での遷移行列を作成する
    """
    # TODO 関数ごとcython化を検討
    # TODO sequence系列も作成する
    seq_transition_element = []  # type: List[TransitionEdgeObject]
    seq_edge_group = []
    for index in range(0, len(seq_wiki_article_name)-1):
        edge_group, seq_transition_edge_object = make_state_transition(
            index=index,
            seq_wiki_article_name=seq_wiki_article_name,
            state2index_obj=state2index_obj,
            entity_vector_model=entity_vector_model)
        seq_edge_group.append(edge_group)
        seq_transition_element += seq_transition_edge_object

    # TODO cythonの場合は、numpyのまま処理してしまう
    data = [transition_tuple.transition_score for transition_tuple in seq_transition_element]
    row = [transition_tuple.row_index for transition_tuple in seq_transition_element]
    column = [transition_tuple.column_index for transition_tuple in seq_transition_element]

    transition_matrix = csr_matrix(
        (data, (row, column)),
        shape=(len(state2index_obj.state2index['row2index']), len(state2index_obj.state2index['column2index']))
    )
    return (state2index_obj, seq_edge_group, transition_matrix)


def filter_out_of_vocabulary_word(wikipedia_article_obj: WikipediaArticleObject, vocabulary_words:set)->Union[bool, WikipediaArticleObject]:
    """* What you can do
    - You remove out-of-vocabulary word from wikipedia_article_obj.candidate_article_name
    """
    filtered_article_name = []
    for article_name in wikipedia_article_obj.candidate_article_name:
        if article_name in vocabulary_words:
            filtered_article_name.append(article_name)
        else:
            logger.warning(msg='Out of vocabulary word. It removes. word = {}'.format(article_name))

    if len(filtered_article_name)==0:
        return False
    else:
        wikipedia_article_obj.candidate_article_name = filtered_article_name
        return wikipedia_article_obj


def make_lattice_object(seq_wiki_article_name:List[WikipediaArticleObject],
                        entity_vector_model:Word2Vec,
                        path_wordking_dir:str=None,
                        is_use_cache:bool=True)->LatticeObject:
    """* What you can do

    """
    if path_wordking_dir is None: path_wordking_dir = mkdtemp()
    if is_use_cache:
        persistent_state2index = PersistentDict(os.path.join(path_wordking_dir, 'column2index.json'), flag='c', format='json')
        persistent_state2index['row2index'] = {}
        persistent_state2index['column2index'] = {}
    else:
        persistent_state2index = {}
        persistent_state2index['row2index'] = {}
        persistent_state2index['column2index'] = {}

    state2dict_obj = IndexDictionaryObject(
        state2index=persistent_state2index,
        index2state={})

    vocabulary_words = set(entity_vector_model.vocab.keys())
    seq_wiki_article_name = [
        wiki_article_name
        for wiki_article_name in seq_wiki_article_name
        if not filter_out_of_vocabulary_word(wiki_article_name, vocabulary_words) is False]

    updated_state2dict_obj, seq_edge_group, transition_matrix = make_state_transition_sequence(
        seq_wiki_article_name=seq_wiki_article_name,
        entity_vector_model=entity_vector_model,
        state2index_obj=state2dict_obj
    )

    if is_use_cache:
        """If is_use_cache is True, use disk-drive for keeping object
        """
        index2state = PersistentDict(os.path.join(path_wordking_dir, 'index2row.json'), flag='c', format='json')
        updated_state2dict_obj.index2state = index2state
    else:
        updated_state2dict_obj.index2state = {}

    updated_state2dict_obj.index2state['index2row'] = {value: key for key, value in updated_state2dict_obj.state2index['row2index'].items()}
    updated_state2dict_obj.index2state['index2column'] = {value: key for key, value in updated_state2dict_obj.state2index['column2index'].items()}

    return LatticeObject(
        transition_matrix=transition_matrix,
        index_dictionary_obj=updated_state2dict_obj,
        seq_edge_groups=seq_edge_group,
        seq_wiki_article_name=seq_wiki_article_name
    )