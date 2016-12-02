from wiki_node_disambiguation import load_entity_model, make_lattice, interface
from wiki_node_disambiguation.models import WikipediaArticleObject, LatticeObject, IndexDictionaryObject
import unittest
import os

class TestInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # procedures before tests are started. This code block is executed only once
        cls.path_model_file = '../bin/entity_vector/entity_vector.model.bin'
        if not os.path.exists(cls.path_model_file):
            cls.path_model_file = cls.path_model_file.replace('../', '')
        cls.model_object = load_entity_model.load_entity_model(path_entity_model=cls.path_model_file, is_use_cache=True)

        cls.seq_wikipedia_article_object = [
            WikipediaArticleObject(page_title='ヤマハ', candidate_article_name=['[ヤマハ]', '[ヤマハ発動機]']),
            WikipediaArticleObject(page_title='スズキ', candidate_article_name=['[スズキ_(企業)]', '[スズキ_(魚)]']),
            WikipediaArticleObject(page_title='ドゥカティ', candidate_article_name=['[ドゥカティ]']),
        ]

    @classmethod
    def tearDownClass(cls):
        # procedures after tests are finished. This code block is executed only once
        pass

    def setUp(self):
        # procedures before every tests are started. This code block is executed every time
        pass

    def tearDown(self):
        # procedures after every tests are finished. This code block is executed every time
        pass

    def test_compute_wiki_node_probability(self):
        sequence_score_objects = interface.compute_wiki_node_probability(
            seq_wiki_article_name=self.seq_wikipedia_article_object,
            entity_vector_model=self.model_object,
            is_use_cache=True
        )
        print([seq_obj.__dict__() for seq_obj in sequence_score_objects])


if __name__ == '__main__':
    unittest.main()