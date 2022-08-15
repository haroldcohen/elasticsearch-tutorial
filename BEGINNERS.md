# Tutorial for beginners

## Introduction

### What is Elasticsearch ?

Elasticsearch is a search engine based on the Lucene library, that provides a full-text search engine with HTTP web
interfaces.

### How is it different from PostgreSQL ?

Unlike relational databases like PostgreSQL or MySQL, Elasticsearch does not store data in forms of columns located in
multiple tables.

> ES is a NoSQL distributed document store that uses JSON as exchange format.

Since Elasticsearch is a distributed system, it can handle incredibly large volumes of data without facing performance
issues.
Below are some key differences.

|                        | PostgreSQL | Elasticsearch |
|------------------------|------------|---------------|
| Type                   | RDBMS      | NoSQL         |
| Transaction support    | Yes        | No            |
| User authentication    | Yes        | No            |
| Consistency            | Yes        | No            |
| Availability           | Yes        | Yes           |
| Partition              | No         | Yes           |
| Near real time search  | No         | Yes           |

### What are indices and documents ?

> An index is a collection of documents, and each document is a collection of fields.
ES has the ability to be schema-less, meaning you don't need to how to handle the field of a document.

In short, Elasticsearch stores JSON documents in indices, whereas PostgreSQL stores data in rows and columns across
tables in databases.

### Elasticsearch features and REST API

Elasticsearch provides with a REST API that can be called directly to access ES features.
You will find a complete API
documentation [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)

## Using Elasticsearch

### Working with documents

#### Index a new document

Let's imagine a car rental system where I want to store a car in an index named "vehicles".\
To do so, I can send the following request to Elasticsearch (available on port 9200 of your localhost).

Note that I don't need to create the index prior to creating a new car. Elasticsearch will automatically create the
index if it does not exist.

```
POST /vehicles/_doc
{
    "type": "car",
    "model": "prius",
    "license_plate": "STARLORD",
    "color": "white",
    "brand": "Toyota"
}
```

The answer should look something like that:

```json
{
  "_index": "vehicles",
  "_id": "9-eUnYIBzqjOGIvCpnMF",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 7,
  "_primary_term": 1
}
```

We can verify that the car was added by sending the following request.

```
POST /vehicles/_search
{
    "query": {
        "match_all": {}
    }
}
```

The answer should look something like that:

```json
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "vehicules",
        "_id": "-eeVnYIBzqjOGIvCpHOt",
        "_score": 1.0,
        "_source": {
          "type": "car",
          "model": "prius",
          "license_plate": "STARLORD",
          "color": "white",
          "brand": "Toyota"
        }
      }
    ]
  }
}
```

Of course, sending request like we just would be extremely tedious in a real life project.\
Thankfully there are libraries available that will make it easier for a developer.\
For Python, we can use the library elasticsearch available on PyPi (installed by Poetry at the beginning of the
tutorial).

We first need an instance of an Elasticsearch client:

```python
import elasticsearch as es

# Remember that this is a tutorial only and that an actual project
# would require ssl certification among other things.
es_client = es.Elasticsearch(
    hosts=[
        {
            "host": "localhost",
            "port": 9200,
        }
    ],
    connection_class=es.RequestsHttpConnection,
    timeout=60,
    max_retries=10,
    retry_on_timeout=True,
    ca_certs=False, verify_certs=False
)
es_client.index(
    index="vehicles",
    body={
        "type": "car",
        "model": "mustang",
        "license_plate": "IRONMAN",
        "color": "white",
        "brand": "Ford"
    }
)
```

> If retrieve the indexed document right after indexing, you will notice that Elasticsearch returns an empty result.

```python
# noinspection PyUnresolvedReferences
es_client.search(
    index="vehicles",
    body={
        "query": {"match": {"license_plate": "IRONMAN"}}
    }
)
```

```json
{
  "_shards": {
    "failed": 0,
    "skipped": 0,
    "successful": 1,
    "total": 1
  },
  "hits": {
    "hits": [],
    "max_score": null,
    "total": {
      "relation": "eq",
      "value": 0
    }
  },
  "timed_out": null,
  "took": 0
}
```

> The reason for this is that although indexing is near real time, indices are refreshed by default every 1 second.

You can force a refresh to update the index at the time of the request:

```python
# noinspection PyUnresolvedReferences
es_client.index(
    index="vehicles",
    body={
        "type": "car",
        "model": "mustang",
        "license_plate": "IRONMAN",
        "color": "white",
        "brand": "Ford"
    },
    refresh=True,
)
```

You will also notice that Elasticsearch has automatically created an ID for the said document. Although convenient, it might
be an issue when we want to update the document.
That's why providing an ID when indexing a new document is preferable.

```python
# noinspection PyUnresolvedReferences
es_client.index(
    index="vehicles",
    id=1,
    body={
        "type": "car",
        "model": "mustang",
        "license_plate": "IRONMAN",
        "color": "white",
        "brand": "Ford"
    }
)
```

You can exercise on adding documents [here](tests/test_index.py)

#### Updating a document

As mentioned above, updating a document will require an ID

```
POST /vehicles/_doc/1
{
    "color": "red",
}
```

The answer should look something like that:

```json
{
  "_index": "vehicles",
  "_id": "1",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 3,
  "_primary_term": 1
}
```

Using the Python Elasticsearch update() method will look like this:

```python
# noinspection PyUnresolvedReferences
es_client.update(
    index="vehicles",
    id="1",
    body={
        "doc": {"color": "red"}
    },
)
```

#### Deleting a document

To delete a document using the Elasticsearch API, I can send the following request.

```
DELETE /vehicles/_doc/1
```

The answer should look something like that:

```json
{
  "_index": "vehicles",
  "_id": "1",
  "_version": 2,
  "result": "deleted",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```

### Searching documents