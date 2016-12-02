from gensim.models import Word2Vec
from wiki_node_disambiguation.interface import load_entity_model, compute_wiki_node_probability
from wiki_node_disambiguation import init_logger
from JapaneseTokenizer import MecabWrapper
import logging
logger = logging.getLogger(init_logger.LOGGER_NAME)
logger.level = logging.INFO

# ------------------------------------------------------------
# PARAMETERS
path_model_file = '../bin/entity_vector/entity_vector.model.bin'
# ------------------------------------------------------------

model_object = load_entity_model(path_entity_model=path_model_file, is_use_cache=True)  # type: Word2Vec
