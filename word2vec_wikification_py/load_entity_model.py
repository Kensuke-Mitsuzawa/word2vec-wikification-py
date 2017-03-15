# -*- coding: utf-8 -*-
try:
    from gensim.models import KeyedVectors
    from gensim.models import Word2Vec
except:
    # to meet api interface of old gensim version
    from gensim.models import Word2Vec
from word2vec_wikification_py import init_logger
from word2vec_wikification_py.models import PersistentDict
from tempfile import mkdtemp
from typing import Union
import os



def load_entity_model(path_entity_model:str,
                      is_binary_file:bool=True,
                      is_use_cache:bool=False,
                      path_working_dir:str=None)->Union[KeyedVectors, Word2Vec]:
    """* What you can do
    - You load entity mode on memory.
    """
    if not os.path.exists(path_entity_model):
        raise FileExistsError('There is no model file at {}'.format(path_entity_model))
    if path_working_dir is None: path_working_dir = mkdtemp()

    try:
        if is_binary_file:
            model = Word2Vec.load_word2vec_format(path_entity_model, binary=True)
        else:
            model = Word2Vec.load_word2vec_format(path_entity_model, binary=False)
    except DeprecationWarning:
        if is_binary_file:
            model = KeyedVectors.load_word2vec_format(path_entity_model, binary=True)
        else:
            model = KeyedVectors.load_word2vec_format(path_entity_model, binary=False)


    if is_use_cache:
        cache_obj = PersistentDict(os.path.join(path_working_dir, 'entity_model'), flag='c', format='pickle')
        cache_obj = model
        return cache_obj
    else:
        return model