# development.py
# A sample file for development (modified from initial main.py)

from es.client import ESClient
from es.indexer import Indexer
from es.searcher import Searcher
from es.config.config import configs

# Create an instance of the Elasticsearch client.
client = ESClient()

# Create an instance of the Indexer class with the Elasticsearch client.
indexer = Indexer(client)

# Index podcast data into the "podcast" index.
# Set "force_indexing" to True to force reindexing.
indexer.index_podcasts(idx_name=configs['idx_name'], limit=10, reindexing=False, append=True)

# Create an instance of the Searcher class with the Elasticsearch client.
searcher = Searcher(client)

# Define the duration (in seconds) for the segments to search for.
seconds = 35

# Search for segments containing the query "hi" within the specified duration.
# The third argument is a dictionary with additional search parameters, in this case, the duration.
segments = searcher.search_podcasts("podcast", "hi", seconds=seconds)

# If relevant segments are found, print information about each segment.
searcher.print_es_results(segments, seconds)