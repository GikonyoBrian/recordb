# Recordb

Recordb library provides a fast and easy-to-use embedded database
for Python.

## Installation
If pip is installed run the command;
```
pip install recordb
```

## Quick start
A simple script using recordb module;

````
>>> import recordb
>>> 
>>> rdb = recordb.Recordb() # Initialize the database object
>>> rdb.createdb("people") # Create a new database
>>> rdb.opendb("people") # Open the database
>>> # Create a old doc in people database with "husband" and "wife" keys
>>> rdb.createdoc("old", ["husband", "wife"]) 
>>> rdb.insert_to_doc("old", [{"husband": "George Foreman", "wife": "Elsie Wise"}])# insert a list of key-value pairs to database
>>> rdb.insert_to_doc("old", [{"husband": "Clark Kent", "wife": "Lois Lane"}])
>>> result = rdb.search_from_doc("old", {"wife": "Lois Lane"})
>>> print result # list of all records in old doc containing the key "wife" whose value is "Lois Lane"
>>> # update the value of "husband" key of the record which has the "wife" key's value as "Lois Lane"
>>> rdb.update_in_doc("old", {"wife": "Lois Lane"}, {"husband": "Superman"}) 
>>> # Delete record where value of "husband" key is "George Foreman" 
>>> rdb.delete_from_doc("old", {"husband": "George Foreman"}) 
>>> rdb.dropdoc("old") # Drop/delete the old doc
>>> rdb.closedb() # Close the database
>>> rdb.dropdb() # Delete the database
````
Docs here are conceptually similar to tables in SQL whereas keys in a doc are similar
to columns.

You can view the databases in your system before opening one as follows;

````
 >>> rbd = recordb.Recordb()
 >>> dbs = rbd.get_databases()
 >>> print dbs
````

You  can view the docs in a database once you've connected to it as follows;

````
 >>> rbd.createdb("people")
 >>> rbd.opendb("people")
 >>> rbd.createdoc("old", ["husband", "wife"])
 >>> docs = rbd.get_docs()
 >>> print docs
 ````

 You can get the keys of a doc in a database as follows:
````
 >>> rbd.opendb("people") 
 >>> keys = rbd.get_doc_keys("old")
 >>> print keys
````
You can insert multiple records at the same time as follows;
````
>>> rbd.createdoc("numbers", ["number"])
>>> insert_list = list()
>>> for x in xrange(1000000):
>>> 	d = {"number": x}
>>> 	insert_list.append(d)
>>> 
>>> rbd.insert_to_doc("numbers", insert_list)
````
You can also query conditionally;
````
>>> rbd.search_from_doc("numbers", {"number": 5000}, condition_statement="greater-than"})
````
The statement above returns all the records whose "number" value is greater than 5000.
````
>>> rbd.search_from_doc("numbers", {"number": 5000}, condition_statement="less-than"})
````
The statement above returns all the records whose "number" value is less than 5000.
````
>>> rbd.search_from_doc("numbers", {"number": 5000}, condition_statement="greater-than-or-equal-to"})
````
The statement above returns all the records whose "number" value is greater than or equal to 5000.
````
>>> rbd.search_from_doc("numbers", {"number": 5000}, condition_statement="less-than-or-equal-to"})
````
The statement above returns all the records whose "number" value is less than or equal to 5000.
```
>>> rbd.update_in_doc("numbers", {"number": 5000}, {"number": 6789}, condition_statement="greater-than"})
````
The statement above updates all the records whose "number" value is greater than 5000 to 6789.
````
>>> rbd.update_in_doc("numbers", {"number": 5000}, {"number": 6789},condition_statement="less-than"})
````
The statement above updates all the records whose "number" value is less than 5000 to 6789.
````
>>> rbd.update_in_doc("numbers", {"number": 5000}, {"number": 6789},  condition_statement="greater-than-or-equal-to"})
````
The statement above updates all the records whose "number" value is greater than or equal to 5000 to 6789.
````
>>> rbd.update_in_doc("numbers", {"number": 5000}, {"number": 6789}, condition_statement="less-than-or-equal-to"})
````
The statement above updates all the records whose "number" value is less than or equal to 5000 to 6789.
````
>>> rbd.delete_from_doc("numbers", {"number": 5000}, condition_statement="greater-than"})
````
The statement above deletes all the records whose "number" value is greater than 5000.
````
>>> rbd.delete_from_doc("numbers", {"number": 5000}, condition_statement="less-than"})
````
The statement above deletes all the records whose "number" value is less than 5000.
````
>>> rbd.delete_from_doc("numbers", {"number": 5000}, condition_statement="greater-than-or-equal-to"})
````
The statement above deletes all the records whose "number" value is greater than or equal to 5000.
````
>>> rbd.delete_from_doc("numbers", {"number": 5000}, condition_statement="less-than-or-equal-to"})
````
The statement above deletes all the records whose "number" value is less than or equal to 5000.
