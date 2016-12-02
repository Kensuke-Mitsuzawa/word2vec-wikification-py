from gensim.models import Word2Vec
from word2vec_wikification_py.interface import load_entity_model, predict_japanese_wiki_names_with_wikidump
from word2vec_wikification_py.initialize_mysql_connector import initialize_pymysql_connector
from word2vec_wikification_py import init_logger
# You're supposed to install "JapaneseTokenizer" pakcage beforehand
from JapaneseTokenizer import MecabWrapper
import logging
logger = logging.getLogger(init_logger.LOGGER_NAME)
logger.level = logging.INFO

"""In this example, you see how to get wikipedia-liked information from Japanese sentence
"""

# ------------------------------------------------------------
# PARAMETERS
path_model_file = '../bin/entity_vector/entity_vector.model.bin'
dict_type = 'neologd'
path_mecab_config = '/usr/local/bin/'
pos_condition = [('名詞', )]
mysql_username = ''
mysql_hostname = 'localhost'
mysql_password = ''
mysql_db_name = 'wikipedia'
# ------------------------------------------------------------
entity_linking_model = load_entity_model(path_model_file)
mecab_tokenizer = MecabWrapper(dict_type, path_mecab_config=path_mecab_config)
model_object = load_entity_model(path_entity_model=path_model_file, is_use_cache=True)  # type: Word2Vec
mysql_connector = initialize_pymysql_connector(hostname=mysql_hostname,
                                               user_name=mysql_username,
                                               password=mysql_password,
                                               dbname=mysql_db_name)

input_sentence = "かつてはイルモア、WCMといったプライベーターがオリジナルマシンで参戦していたほか、カワサキがワークス・チームを送り込んでいたが、2016年現在出場しているのはヤマハ、ホンダ、スズキ、ドゥカティ、アプリリアの5メーカーと、ワークスマシンの貸与等を受けられるサテライトチームとなっている。"
filtered_nouns = mecab_tokenizer.filter(
    parsed_sentence=mecab_tokenizer.tokenize(sentence=input_sentence,return_list=False),
    pos_condition=pos_condition).convert_list_object()

sequence_score_ojects = predict_japanese_wiki_names_with_wikidump(input_tokens=filtered_nouns,
                                                                  wikipedia_db_connector=mysql_connector,
                                                                  entity_vector_model=entity_linking_model,
                                                                  is_use_cache=True,
                                                                  is_sort_object=True)
for rank, sequence_obj in enumerate(sequence_score_ojects):
    print('Rank-{} with score={}'.format(rank, sequence_obj.sequence_score))
    print(sequence_obj.get_tokens())
    print('-'*30)