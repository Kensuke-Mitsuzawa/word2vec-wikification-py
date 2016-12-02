from typing import List, Any, Dict
from pymysql import Connection, cursors
from typing import Tuple

def __generate_window_size(target_token:List[str])->List[int]:
    return [i for i in range(1, len(target_token)+1)]


def __generate_index_range(list_index:List[int], window_size:int)->List[List[int]]:
    """generate set of list, which describes range-index of candidate tokens
    """
    search_index = []
    for start_i in range(0, len(list_index)):
        end_i = start_i + window_size
        if end_i <= len(list_index):
            search_index.append(list(range(start_i, end_i)))
    return search_index


def search_function_from_wikipedia_database(token: str,
                                            wikipedia_db_connector: Connection,
                                            page_table_name: str = 'page',
                                            page_table_redirect: str = 'redirect') -> List[str]:
    """*
    部分文字検索をするときに使う
    """
    def decode_string(string):
        try:
            unicode_string = string.decode('utf-8')
            return unicode_string
        except:
            return None

    cursor = wikipedia_db_connector.cursor()  # type: cursors
    redirect_page_query = """SELECT rd_from, rd_title FROM {} WHERE rd_title = %s AND rd_namespace = 0""".format(page_table_redirect)
    cursor.execute(redirect_page_query, (token,))
    redirect_results = [(page_id_title[0], page_id_title[1]) for page_id_title in cursor.fetchall()]
    cursor.close()
    # TODO 曖昧さ回避の処理が必要
    # カテゴリテーブルを検索して、曖昧さカテゴリの下にないことを確認する


    # 結果が0でなければ、tokenはwikipedia記事名である。
    if len(redirect_results) != 0: return [token]

    cursor = wikipedia_db_connector.cursor()  # type: cursors
    page_query = """SELECT page_id, page_title FROM {} WHERE page_title = %s AND page_namespace = 0""".format(page_table_name)
    cursor.execute(page_query, (token, ))
    page_results = [page_id_title[0] for page_id_title in cursor.fetchall()]
    cursor.close()
    if len(page_results)==0: return []

    cursor = wikipedia_db_connector.cursor()  # type: cursors
    select_query = """SELECT rd_title FROM {} WHERE rd_from IN %s""".format(page_table_redirect)
    cursor.execute(select_query, (page_results,))
    redirect_names = [decode_string(page_id_title[0]) for page_id_title in cursor.fetchall()
                      if not decode_string(page_id_title[0]) is None]
    cursor.close()

    return redirect_names


def search_from_dictionary(target_tokens:List[str],
                           string_normalization_function,
                           partially_param_given_function)->Dict[str,Any]:
    """*
    """
    list_window_size = __generate_window_size(target_tokens)
    found_index = [] # type: List[int]
    found_token_tuple_object = {}

    all_index = [i for i in range(0, len(target_tokens))]

    for w_size in list_window_size[::-1]:
        list_index = list(range(0, len(target_tokens)))
        candidate_index_list = __generate_index_range(list_index, window_size=w_size)
        for candidate_indices in candidate_index_list:
            if len(set(candidate_indices).intersection(set(found_index)))>=1: continue

            start_index = candidate_indices[0]
            end_index = candidate_indices[-1] + 1
            # candidate token
            search_token = ''.join(target_tokens[start_index:end_index])
            normalized_search_token = string_normalization_function(search_token)
            # search token from ontology
            search_result = partially_param_given_function(normalized_search_token)
            # search result check
            # if length is more than 0, this is true
            if len(search_result)>0:
                # 見つかったオブジェクトを追加する
                found_token_tuple_object.update({normalized_search_token: search_result})
                if all_index[-1] in candidate_indices:
                    found_index += candidate_indices
                else:
                    if len(candidate_indices)==1:
                        found_index += candidate_indices
                    else:
                        found_index += candidate_indices
        # end condition
        if set(found_index) == set(all_index): break

    return found_token_tuple_object


def complete_search():
    pass