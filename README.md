# Elasticsearch tutorial

- [About this project](#about-this-project)
    - [Getting started](#getting-started)
    - [How to](#how-to)

## About this project

This project is a tutorial to gives you the basics of Elasticsearch, as well as the Elasticsearch python lib.
You can find the official documentations for both projects here:
 - [Elasticsearch](https://www.elastic.co/guide/index.html)
 - [Python Elasticsearch client](https://elasticsearch-py.readthedocs.io/en/latest/)

### Prerequisites

- Python
- Poetry
- Elasticsearch (8.x)

> :warning: <b>This tutorial is currently based on the latest version of Elasticsearch (8.x).
> Due to bugs in the Python client matching version, the version in the dependency file is set to 7.x
> An upgrade will be committed once the issue is resolved.</b>

### Getting started

At the project's root, run:

```
$ poetry shell && poetry install
```

To download the docker image of Elasticsearch, run:

```
$ docker pull elasticsearch:latest
```

To create a docker network, run:

```
$ docker network create esnetwork
```

To create an Elasticsearch container, run:

```
$ docker run -d --name elasticsearch --net esnetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "ingest.geoip.downloader.enabled=false" -e "xpack.security.enabled=false" elasticsearch:latest
```

Elasticsearch is now available on port 9200.
Open your web browser and go to http://localhost:9200.\
You should see something like that:

```
{
  "name" : "a34d9fdb6705",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "YrBf2l1nTly8i301xwvGzg",
  "version" : {
    "number" : "8.3.3",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "801fed82df74dbe537f89b71b098ccaff88d2c56",
    "build_date" : "2022-07-23T19:30:09.227964828Z",
    "build_snapshot" : false,
    "lucene_version" : "9.2.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

### How to

The sections in the tutorials will each tackle a key concept in Elasticsearch.
In most sections, you will find a matching series of [tests](./tests).
Each test file will help illustrate some concepts and allow you to practice.

The only tutorial available for now is for [Beginners](BEGINNERS.md),
but I will make my best to deliver tutorials for more experienced developers.