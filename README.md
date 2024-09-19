# D2477-Podcast-Search

## Overview

Welcome to KTH DD2477 Podcast Search Project!

The Podcast Search project is a Flask-based web application that provides users with an efficient way to find relevant segments of podcasts based on their search queries. 
Leveraging Elasticsearch, the project indexes podcast data, including transcriptions and time markers, to enable efficient search functionality. 
Users can easily search for specific topics or keywords, retrieve relevant segments of audio content, and explore search results seamlessly. 
The interface is intuitive and user-friendly, allowing users to specify the duration of podcast segments and navigate through search results effortlessly.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe) and above installed on your system (Python 3.6 and above)
- [Docker](https://www.docker.com/products/docker-desktop/) installed on your system (Docker 20.0 and above)
- [Git](https://git-scm.com/) installed on your system (if cloning the repository)

### Datasets

- Download the dataset from [**spotify-podcasts-2020**](https://podcastsdataset.byspotify.com/)

- Unzip the `podcasts-transcripts` to the path defined by `podcasts_transcripts_path` in `elasticsearch.yml`

- Unzip the `metadata.tsv` to the path defined by `metadata_tsv_path` in `elasticsearch.yml`


### Installation

To install and run this project locally, follow these steps:

1.  Clone the repository:

    ```shell
    git clone git@github.com:IsakNordg/DD2477-Podcast-search.git
    ```

2.  Install dependencies:

    ```shell
    cd ./DD2477-Podcast-search
    pip install -r es/requirements.txt
    pip install -r backend/requirements.txt
    ```

3.  Set up Elasticsearch (using Docker is recommended):

    Ensure that Elasticsearch is installed and running locally or on a remote server.
    Docker example:
    
    ```shell
    docker network create elastic
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```
    
    Configure Elasticsearch connection settings in `es/config/elasticsearch.yml`.
    > Change the IP and port of `hosts` if you run elasticsearch remotely.

    Replace the password and certificate in `es/config/.env` and `es/config/http_ca.crt` with your credentials to Elasticsearch.
    > The default path to `http_ca.crt` in docker is `/usr/share/elasticsearch/config/certs/http_ca.crt`.
    
4.  Run the Flask application:
    ```shell
    python meow.py
    ```
    
    > The repo also provides the Docker-Compose file for you to run applications in a docker container.

### Command Line Options

The program supports the following command-line options:

1. `reindex`: Set to `true` to force re-indexing of all podcasts (default is `false`).
2. `append`: Set to `false` to disable indexing new podcasts (default is `true`).
3. `debug`: Set to `true` to enable debug mode for Flask application (default is `false`).
4. `limit`: Specify the maximum number of podcasts to index (default is 105360).
5. `hosts`: Specify the host IP address to run the Flask application (default is "0.0.0.0").


### Usage & App Features

Once the application is running, you can open the web browser and search on `http://localhost:5000/:

- `Clip duration`: Define the max duration of podcast clip to search.
- `Search method`: Select the searching method.

Demo Pictures:

[![search-page-image](https://i.postimg.cc/L8NY3wPG/search-page-image.webp)](https://postimg.cc/75JZxBmN)

[![result-page-image](https://i.postimg.cc/7hBHv8N2/result-page-image.webp)](https://postimg.cc/MfQ2RLN6)

## Contributing

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the [Apache 2.0 License]().

## Acknowledgments

Special thanks to the contributors and maintainers of Flask, Elasticsearch, and other open-source libraries used in this project.