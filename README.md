# DockieDb
A simple in-memory document database.

## Installation

Install using `pip install tq-dockie-db`.

## Document Database Primer
Looking at the tests in the `test` folder will give you a good idea on how to use DockieDb. Nevertheless,
this section offers some guidance.

In general, document database objects have the following hierarchy:

`Database ---> Container (1 or more) --->Document (1 or more)`

At the root, there is a Database. A database consists of one or more Containers. A
Container holds one or more Documents. 

If you're coming from a relational background then you can
think of the Database as the schema, a Container as the table, and a Document as a row in the table.

Whereas the rows in the table conform to the same schema, Documents in a Container
are schemaless. In other words you can store Documents of different shapes in the same container.

[This tutorial](https://docs.microsoft.com/en-us/learn/paths/implement-modeling-partitioning-azure-cosmos-db-sql-api/) is a great read for those new to document databases. It does
a better job explaining it than I ever could in this readme.

## Creating Database Objects

### Create a Database
```python
from dockie.core.database import Database

db = Database()
```

### Create a Container
```python
container = db.add_container("items")
```

### Add a Document to the Container
```python
from dockie.core.document import Document

document = Document("item1", {"name": "basketball", "price": 29.99})
container.add_document(document)
```
<mark>A document id must be a string or integer.</mark>

## Retrieving Documents
There are two ways to retrieve a document:

- By its id.
- By querying against one or more non-id attributes.

### Retrieving a Document by ID
```python
from dockie.query.query import DocumentIdQuery

query = DocumentIdQuery()
document = query.execute(container, document_id="item1")
```
### Retrieving a Document by a Non-ID Attribute
Querying by non-ID attributes is accomplished with the [dictquery library](https://pypi.org/project/dictquery/).
```python
from dockie.query.query import DocumentAttributeQuery

query = DocumentAttributeQuery()
document = query.execute(container, query='name=="basketball"')
```

Refer to the tests in this repository for more query examples. Refer to the dictquery
homepage for details on dictquery syntax.

## Persisting the Database
Although DockieDb is an in-memory database, it can be saved and loaded to/from a file.

### Save the Database to File
```python
from dockie.core.persistence import persist_to_file

persist_to_file(db, "db.bak")
```

### Load the Database from File
```python
from dockie.core.persistence import load_from_file

db = load_from_file("db.bak)
```

## Miscellania
### Running Tests
From the project root folder, run `pytest` without any arguments.