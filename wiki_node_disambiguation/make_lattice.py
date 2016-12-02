from numpy import ndarray
from gensim.models import Word2Vec
from wiki_node_disambiguation.models import WikipediaArticleObject, PersistentDict, LatticeObject
from typing import List, Tuple, Union, Any, Dict
from tempfile import mkdtemp
from scipy.sparse import csr_matrix
import os


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
                               column2index:Union[Dict, PersistentDict],
                               row2index:Union[Dict, PersistentDict],
                               entity_vector:Word2Vec)->Tuple[Tuple[int,int,float], Dict, Dict]:
    """tの単語xからt+1の単語x'への遷移スコアを計算する
    * Output
    - tuple object whose element is (transition_element, row2index, column2index)
    - transition_element is (row_index, column_index, transition_score)
    """
    if not state_t_word_tuple[1] in entity_vector.vocab:
        raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_word_tuple))
    if not state_t_plus_word_tuple[1] in entity_vector.vocab:
        raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_plus_word_tuple))

    transition_score = entity_vector.similarity(state_t_word_tuple[1], state_t_plus_word_tuple[1])  # type: float
    if state_t_word_tuple in row2index:
        row_index = row2index[state_t_word_tuple]
    else:
        row2index = __update_index_dictionary(state_t_word_tuple, row2index)
        row_index = row2index[state_t_word_tuple]


    if state_t_plus_word_tuple in column2index:
        column_index = column2index[state_t_plus_word_tuple]
    else:
        column2index = __update_index_dictionary(state_t_plus_word_tuple, column2index)
        column_index = column2index[state_t_plus_word_tuple]

    return (
        (
            row_index,
            column_index,
            transition_score
        ), row2index, column2index)


def make_state_transition_sequence(seq_wiki_article_name:List[WikipediaArticleObject],
                                   entity_vector_model:Word2Vec,
                                   column2index: Union[Dict, PersistentDict],
                                   row2index: Union[Dict, PersistentDict])->Tuple[Dict[Tuple[int,str],int],
                                                                                  Dict[Tuple[int,str],int],
                                                                                  ndarray]:
    """系列での遷移行列を作成する
    """
    # TODO 関数ごとcython化を検討
    seq_transition_element = []
    for index in range(0, len(seq_wiki_article_name)-1):
        for candidate_wikipedia_article_name in seq_wiki_article_name[index].candidate_article_name:
            for candiate_wikipedia_article_name_state_plus in seq_wiki_article_name[index+1].candidate_article_name:
                state_t_word_tuple = (index, candidate_wikipedia_article_name)
                state_t_plus_word_tuple = (index+1, candiate_wikipedia_article_name_state_plus)
                transition_element, row2index, column2index = make_state_transition_edge(
                    state_t_word_tuple=state_t_word_tuple,
                    state_t_plus_word_tuple=state_t_plus_word_tuple,
                    column2index=column2index,
                    row2index=row2index,
                    entity_vector=entity_vector_model
                )
                seq_transition_element.append(transition_element)

    # TODO cythonの場合は、numpyのまま処理してしまう
    data = [transition_tuple[2] for transition_tuple in seq_transition_element]
    row = [transition_tuple[0] for transition_tuple in seq_transition_element]
    column = [transition_tuple[1] for transition_tuple in seq_transition_element]

    transition_matrix = csr_matrix(
        (data, (row, column)),
        shape=(len(row2index), len(column2index))
    )
    return (row2index, column2index, transition_matrix)



def make_lattice_object(seq_wiki_article_name:List[WikipediaArticleObject],
                        entity_vector_model:Word2Vec,
                        path_wordking_dir:str=None,
                        is_use_cache:bool=True)->LatticeObject:
    """* What you can do

    """
    if path_wordking_dir is None: path_wordking_dir = mkdtemp()
    persistent_column2index = PersistentDict(os.path.join(path_wordking_dir, 'column2index.json'), flag='c', format='json')
    persistent_row2index = PersistentDict(os.path.join(path_wordking_dir, 'row2index.json'), flag='c', format='json')

    # TODO vocaburaryに存在しない単語の排除

    row2index, column2index, transition_matrix = make_state_transition_sequence(
        seq_wiki_article_name=seq_wiki_article_name,
        entity_vector_model=entity_vector_model,
        column2index=persistent_column2index,
        row2index=persistent_row2index
    )

    if is_use_cache:
        """If is_use_cache is True, use disk-drive for keeping object
        """
        index2row = PersistentDict(os.path.join(path_wordking_dir, 'index2row.json'), flag='c', format='json')
        index2column = PersistentDict(os.path.join(path_wordking_dir, 'index2column.json'), flag='c', format='json')

        index2row = {value: key for key,value in row2index.items()}
        index2column = {value: key for key,value in column2index.items()}
    else:
        index2row = {value: key for key,value in row2index.items()}
        index2column =  {value: key for key,value in column2index.items()}

    return LatticeObject(
        transition_matrix=transition_matrix,
        index2column=index2column,
        index2row=index2row
    )