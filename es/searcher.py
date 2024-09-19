"""
Define functions for searching data in Elasticsearch.

File: <searcher.py>
Author: <NAME>
Purpose: Search data in Elasticsearch
Description: This file contains functions to search for data in Elasticsearch,
             such as querying documents based on specific criteria.
"""

from es.client import ESClient
from es.config.config import configs

class Searcher:

    def __init__(self, client=ESClient()):
        self.es = client.es
        pass

    @staticmethod
    def print_es_results(segments, seconds):
        if segments:
            print(f"Found {len(segments)} relevant {seconds}-second segments:")
            for segment in segments:
                print(f"Document ID: {segment['doc_id']}")
                print(f"Path: {segment['path']}")
                print(f"Transcript: {segment['transcript']}")
                print(f"Start Time: {segment['startTime']}, End Time: {segment['endTime']}")
                print("=" * 50)
        else:
            print("No relevant segments found for the query.")

    def search_sample(self, index, query):
        es_query = {
            "query": {
                "match": {
                    "title": query,
                }
            }
        }
        return self.es.search(index=index, body=es_query)

    def search_podcasts(self, index, query, **kwargs):
        """
        Search for podcasts in the specified index based on the given query.

        Args:
            index (str): The name of the Elasticsearch index to search in.
            query (str): The search query string (NOT the body of search).
            kwargs: Other parameters or options for the search (optional).
                'seconds' (int): The number of seconds to search for podcasts.
                'method' (int): The method ID to search for podcasts.
                'size' (int): The maximum number of podcasts to return.

        Returns:
            dict: The search results returned by Elasticsearch.
        """
        # TODO(Isak): Implementation of searching logic

        # Extract seconds and method from kwargs if provided
        seconds = kwargs.get('seconds', configs["default_clip_sec"])  # Default value is 120 if not provided
        method_id = kwargs.get('method', 0)  # Default value is id=0 if not provided
        size = kwargs.get('size', 10)  # Default value is top 10 if not provided

        # Begin a try block to handle potential exceptions during execution
        try:
            # Define an Elasticsearch query
            es_query = {
                "query": {
                    "match": {
                        "transcript": query
                    }
                }
            }

            # Execute the Elasticsearch with defined query
            response = self.es.search(index=index, body=es_query, size=size)

            # Initialize an empty list to store relevant segments
            segments = []

            # Iterate through the hits returned by the Elasticsearch
            for hit in response['hits']['hits']:
                # For each hit, create a dictionary representing a segment
                segment = {
                    "doc_id": hit['_id'],
                    "path": hit['_source']['path'],
                    "transcript": hit['_source']['transcript'],
                    "startTime": hit['_source']['startTime'],
                    "endTime": hit['_source']['endTime'],
                    "score": hit['_score'],
                    # Update metadata (v2.0)
                    "episode_name": hit['_source']['episode_name'],
                    "rss_link": hit['_source']['rss_link'],
                    "title": hit['_source']['title'],
                }
                # Append the segment to the list of segments
                segments.append(segment)

            # Sort the segments based on their scores in descending order
            segments = sorted(segments, key=lambda x: x['score'], reverse=True)

            # Return the filtered segments based on the specified duration
            return self.filter_segments(segments, seconds)

        except Exception as e:
            # Catch any exceptions that occur during execution
            print(f"Error searching for segments: {e}")
            # If an exception occurs, return an empty list
            return []
        
    def filter_segments(self, segments, seconds):
        """
        Filter segments based on the desired duration (in seconds).

        Args:
            segments (list): List of segments to be filtered.
            seconds (int): Desired duration in seconds.

        Returns:
            list: Filtered segments.
        """
        filtered_segments = []
        for segment in segments:
            start_seconds = segment['startTime']
            end_seconds = segment['endTime']
            duration_seconds = end_seconds - start_seconds
            if duration_seconds <= seconds:
                filtered_segments.append(segment)

        # Check if the segments can be extended to reach the desired duration
        for segment in filtered_segments:
            start_seconds = segment['startTime']
            end_seconds = segment['endTime']
            duration_seconds = end_seconds - start_seconds

            # Get following segments that are within the desired duration
            es_query = {
                "query": {
                    "match": {
                        "path": segment['path'],
                    }
                },
                "size": 1000,   # FIXME This is just a high number. Maybe it should be bigger if some files are large,
                                #       or more reasonable if all are smaller
            }

            response = self.es.search(index=configs['idx_name'], body=es_query)
            for hit in response['hits']['hits']:
                hit_transcript = hit['_source']['transcript']
                hit_start_seconds = hit['_source']['startTime']
                hit_end_seconds = hit['_source']['endTime']
                hit_duration_seconds = hit_end_seconds - hit_start_seconds

                if hit_start_seconds >= end_seconds: # if hit is after segment
                    if duration_seconds + hit_duration_seconds <= seconds:  # if adding hit to segment is within desired duration
                        # Add score to segment if another segment also had query from previous search.
                        for seg in segments:
                            if seg['transcript'] == hit_transcript:
                                segment['score'] += seg['score']

                        segment['endTime'] = hit['_source']['endTime']
                        duration_seconds += hit_duration_seconds
                        segment['transcript'] += " " + hit['_source']['transcript']
                    else:
                        break

        # Sort filtered segments based on their scores in descending order
        filtered_segments = sorted(filtered_segments, key=lambda x: x['score'], reverse=True)
        return filtered_segments
