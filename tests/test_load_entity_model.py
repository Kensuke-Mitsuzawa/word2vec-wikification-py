from word2vec_wikification_py import load_entity_model
import unittest
import os

class TestLoadEntityModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # procedures before tests are started. This code block is executed only once
        cls.path_model_file = '../bin/entity_vector/entity_vector.model.bin'
        if not os.path.exists(cls.path_model_file):
            cls.path_model_file = cls.path_model_file.replace('../', '')


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

    def test_load_entity_model(self):
        model_object = load_entity_model.load_entity_model(path_entity_model=self.path_model_file,
                                                           is_use_cache=True)
        print(model_object.most_similar('[エン・ジャパン]'))

if __name__ == '__main__':
    unittest.main()