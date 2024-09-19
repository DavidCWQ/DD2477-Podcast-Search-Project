"""
Define Flask routes for the application.

File: <routes.py>
Author: <Wenqi Cao>
Purpose: Define Flask routes
Description: This file defines Flask routes for handling HTTP requests.
             Each route corresponds to a URL endpoint and calls a view
             function to generate an HTTP response.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .views import search_example, search_podcast, configs

session = dict()

isTest = configs["is_test"]
api = Blueprint('api', __name__)

@api.route('/')
def home():
    """
    Render the home page (optional).

    Returns:
        str: Rendered HTML content for the home page.
    """
    return render_template("home.html")

@api.route('/search', methods=['GET', 'POST'])
def search():
    """
    Endpoint to perform search in Elasticsearch.

    Returns:
        Rendered HTML content for the search or results page.
    """
    if request.method == 'POST':
        # Get the search query from the request body
        size = request.json.get('size')
        query = request.json.get('query')
        method = request.json.get('method')
        seconds = request.json.get('second')
        if not query or not method:
            return jsonify({"Error": "Query parameter is missing."}), 400
        else:
            size = 10 if size == '' else int(size)
            seconds = configs["default_clip_sec"] if seconds == '' else int(seconds)
            return search_query(query, method, seconds, size)

    if request.method == 'GET':
        # Get the search query from the request URL
        size = request.args.get('size', type=int)
        query = request.args.get('query', type=str)
        method = request.args.get('method', type=int)
        seconds = request.args.get('second', type=int)
        if not query or not method:
            return render_template("search.html")
        else:
            return search_query(query, method, seconds, size)

@api.route('/results', methods=['GET', 'POST'])
def results():
    es_results = session.get('results')
    if es_results is None:
        return redirect(url_for('api.home'))
    return render_template("results.html", results=es_results)

@api.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors (optional).

    Args:
        e (Exception): The exception object.

    Returns:
        tuple: A tuple containing the error message and status code.
    """
    return 'Page not found', 404

def search_query(query, method, second, size):
    # Avoid searching for the same consecutive query and method
    query_obj = {"query": query, "method": method, "second": second, "size": size}
    if session.get('query_obj') and session['query_obj'] == query_obj:
        return redirect(url_for('api.results'))
    else:
        session['query_obj'] = query_obj
    # Process the search query and get search results
    if isTest is True:
        session['results'] = search_example(query, method)
    else:
        session['results'] = search_podcast(query, method, second, size)
    # Redirect the user to the results page
    return redirect(url_for('api.results'))