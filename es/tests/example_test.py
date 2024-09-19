import unittest

from es.client import ESClient
from es.indexer import Indexer
from es.searcher import Searcher
from es.config.config import configs


class TestExample(unittest.TestCase):

    es_client = ESClient()
    es_indexer = Indexer(es_client)
    es_searcher = Searcher(es_client)

    def test_connection(self):
        print(self.es_client.es.info())
        tagline = self.es_client.es.info()["tagline"]
        self.assertEqual("You Know, for Search", tagline)

    def test_indexing(self):
        response = self.es_indexer.index_sample()
        self.assertEqual(response["_index"], configs["example_idx_name"])

    def test_search(self):
        es_results = self.es_searcher.search_sample(
            index=configs["example_idx_name"], query="Hello",
        )
        print(es_results['hits']['hits'])
        self.assertEqual(es_results['hits']['hits'][0]['_source']['title'],
                         "Hello Elasticsearch")

if __name__ == '__main__':
    unittest.main()