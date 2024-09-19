"""
Define Scrape class for the backend logic.

File: <scraper.py>
Author: <Wenqi Cao>
Purpose: Scrape enclosure URLs from an RSS feed.
Description: This file contains the Scraper class that provides methods
             to extract enclosure URLs from the fetched content using
             the requests lib and parse HTML/XML using BeautifulSoup.
"""

import string
import requests

from bs4 import BeautifulSoup
from xml.etree import ElementTree as ETree


class ScrapingError(Exception):
    pass


class Scraper:

    def __init__(self, debug=False, debug_print=False):
        self.debug = debug
        self.print = debug_print

    @staticmethod
    def remove_punctuation(text):
        return ''.join([ch for ch in text if ch not in string.punctuation])

    def scrape_audio_url(self, rss_link, episode_name):
        try:
            page_text = self.__scrape_page(rss_link)
            # Parse the XML content
            return self.find_audio_url(page_text, episode_name)
        except ScrapingError as err:
            if self.print: print(err)
            if self.debug: raise err
            return None

    def find_audio_url(self, xml_text, episode_name):
        try:
            soup = BeautifulSoup(xml_text, 'xml')
            # Find the item that matches the given title
            item = soup.find(lambda t: t.name == 'title' and episode_name in t.text)
            if item is None:
                purify = self.remove_punctuation
                item = soup.find(lambda tag: purify(episode_name) in purify(tag.text)
                                             and tag.name == 'title')
            # Check if there is a match
            if item is None:
                if self.print: print("ScrapingError: Given title not found.")
                if self.debug: raise ScrapingError("Given title not found on the webpage!")
                return None
            link = self.__find_next_enclosure_link(item)
            # Check if audio url exists
            if link is None:
                if self.print: print("ScrapingError: No enclosure URL found.")
                if self.debug: raise ScrapingError("No enclosure URL found after the given title!")
                return None
            return link
        except ScrapingError as err:
            if self.print: print(err)
            if self.debug: raise err
            return None

    def __find_next_enclosure_link(self, tag):
        # Find the next sibling that contains an enclosure tag
        next_sibling = tag.find_next_sibling()
        while next_sibling:
            text = str(next_sibling)
            if "<enclosure" in text:
                if self.print: print("URL FOUND")
                return self.__extract_enclosure_url(text)
            next_sibling = next_sibling.find_next_sibling()
        if self.print: print("URL NOT FOUND")
        return None

    def __extract_enclosure_url(self, tag):
        enclosure_url = None
        try:
            # Parse the XML representation of the enclosure tag
            enclosure_tree = ETree.fromstring(tag)
            # Extract the URL attribute from this enclosure tag
            enclosure_url = enclosure_tree.get('url')
        except Exception as e:
            if self.print: print("Error extracting enclosure url.")
            if self.debug: raise ScrapingError("Error extracting url: ", e)
        if self.print: print(enclosure_url)
        return enclosure_url

    def __scrape_page(self, http_link):
        # Fetch the webpage content
        response = requests.get(http_link)
        # Check response status
        if response.status_code != 200:
            if self.print: print("PageRequest Error: ", response.reason)
            raise ScrapingError("Failed to scrape page: ", http_link,
                                "status code: ", response.status_code)
        return response.text