from typing import List, Tuple, Any, Union, Dict
from numpy.core import ndarray
import pickle, json, csv, os, shutil

# this class is from https://code.activestate.com/recipes/576642/
class PersistentDict(dict):
    ''' Persistent dictionary with an API compatible with shelve and anydbm.
    The dict is kept in memory, so the dictionary operations run as fast as
    a regular dictionary.
    Write to disk is delayed until close or sync (similar to gdbm's fast mode).
    Input file format is automatically discovered.
    Output file format is selectable between pickle, json, and csv.
    All three serialization formats are backed by fast C implementations.
    '''

    def __init__(self, filename, flag='c', mode=None, format='pickle', *args, **kwds):
        self.flag = flag                    # r=readonly, c=create, or n=new
        self.mode = mode                    # None or an octal triple like 0644
        self.format = format                # 'csv', 'json', or 'pickle'
        self.filename = filename
        if flag != 'n' and os.access(filename, os.R_OK):
            fileobj = open(filename, 'rb' if format=='pickle' else 'r')
            with fileobj:
                self.load(fileobj)
        dict.__init__(self, *args, **kwds)

    def sync(self):
        'Write dict to disk'
        if self.flag == 'r':
            return
        filename = self.filename
        tempname = filename + '.tmp'
        fileobj = open(tempname, 'wb' if self.format=='pickle' else 'w')
        try:
            self.dump(fileobj)
        except Exception:
            os.remove(tempname)
            raise
        finally:
            fileobj.close()
        shutil.move(tempname, self.filename)    # atomic commit
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, fileobj):
        if self.format == 'csv':
            csv.writer(fileobj).writerows(self.items())
        elif self.format == 'json':
            json.dump(self, fileobj, separators=(',', ':'))
        elif self.format == 'pickle':
            pickle.dump(dict(self), fileobj, 2)
        else:
            raise NotImplementedError('Unknown format: ' + repr(self.format))

    def load(self, fileobj):
        # try formats from most restrictive to least restrictive
        for loader in (pickle.load, json.load, csv.reader):
            fileobj.seek(0)
            try:
                return self.update(loader(fileobj))
            except Exception:
                pass



class WikipediaArticleObject(object):
    """Wikipediaの記事情報を記述するためのクラス
    """
    __slots__ = ['page_title', 'candidate_article_name', 'article_name']

    def __init__(self,
                 page_title:str,
                 candidate_article_name:List[str],
                 article_name:str=None):
        self.page_title = page_title
        self.candidate_article_name = candidate_article_name
        self.article_name = article_name

    def __str__(self)->str:
        return self.page_title

    def __dict__(self)->Dict[str,Any]:
        return {
            'page_title': self.page_title,
            'candidate_article_name': self.candidate_article_name,
            'article_name': self.article_name
        }

    @classmethod
    def from_dict(cls, dict_object:Dict[str,Any]):
        if 'article_name' in dict_object:
            article_name = dict_object['article_name']
        else:
            article_name = None

        return WikipediaArticleObject(
            page_title=dict_object['page_title'],
            candidate_article_name=dict_object['candidate_article_name'],
            article_name=article_name
        )


class SequenceScore(object):
    """計算された記事系列のスコアを保持するオブジェクト

    """
    def __init__(self,
                 seq_words:Union[WikipediaArticleObject, List[str]],
                 seq_transition_score:ndarray,
                 sequence_score:float):
        self.seq_words = seq_words
        self.seq_transition_score = seq_transition_score
        self.sequence_score = sequence_score

    def __dict__(self):
        return {
            'seq_words': self.seq_words,
            'seq_transition_score': self.seq_transition_score,
            'sequence_score': self.sequence_score
        }

    @classmethod
    def from_dict(cls, dict_object:Dict[str,Any]):
        return SequenceScore(
            seq_words=dict_object['seq_words'],
            seq_transition_score=dict_object['seq_transition_score'],
            sequence_score=dict_object['sequence_score']
        )


class LatticeObject(object):
    def __init__(self,
                 transition_matrix:ndarray,
                 index2column:Dict[int,Tuple[int,str]],
                 index2row:Dict[int,Tuple[int,str]]):
        self.transition_matrix = transition_matrix
        self.index2column = index2column
        self.index2row = index2row