import os
import time
import ujson
import fcntl
import shutil


class Recordb:
	def __init__(self):
		self.database = ""

	def check_for_key_value_pairs_in_dict(self, key_value_dict, dictionary):
		key_value_dict_length = len(key_value_dict.keys())
		key_values_in_both_dicts = list()
		decoded_key_value_dict_keys = [key.decode('utf8', 'strict') for key in key_value_dict.keys()]
		if all(key in dictionary.keys() for key in decoded_key_value_dict_keys):
			for key, value in zip(key_value_dict.keys(), key_value_dict.values()):
				if dictionary[key.decode('utf8', 'strict')] == value.decode('utf8', 'strict'):
					key_values_in_both_dicts.append(key)
			if len(key_values_in_both_dicts) == key_value_dict_length:
				return True
			else:
				return False
		else:
			return False

	def check_for_keys_in_dict(self, keys_list, dictionary):
			decoded_keys_list = [key.decode('utf8', 'strict') for key in keys_list]
			if all(key in dictionary.keys() for key in decoded_keys_list):
				return True
			else:
				return False

	
	def createdb(self, database_name):
		database_path = ".data" + "/" + database_name
		assert (not os.path.exists(database_path)),"Database " + database_name + " exists."
		os.makedirs(database_path)

	def opendb(self, database_name):
		database_path = ".data" + "/" + database_name
		assert (os.path.exists(database_path)),"Database " + database_name + " not created."
		self.database = database_path

	def createdoc(self, doc_name, keys):
		doc_data = {'timestamp': time.asctime(), 'records': list(), 'keys': keys}
		doc_path = self.database + "/" + doc_name + ".gik"
		assert (not os.path.exists(doc_path)),"Database not created/opened or specified doc already exists."
		with open(doc_path, "wb") as doc:
			ujson.dump(doc_data, doc)
			doc.close()
		
	def insert_to_doc(self, doc_name, insert_values_list):
		if isinstance(insert_values_list, list):
			doc_path = self.database + "/" + doc_name + ".gik"
			with open(doc_path, 'r+b') as doc:
				fcntl.flock(doc, fcntl.LOCK_EX)
				doc_data = ujson.load(doc)
				doc.seek(0)
				for insert_values in insert_values_list:
					if isinstance(insert_values, dict):
						keys = [key.decode('utf8', 'strict') for key in insert_values.keys()]
						if keys.sort() == doc_data["keys"].sort():
							doc_data["records"].append(insert_values)
						else:
							fcntl.flock(doc, fcntl.LOCK_UN)
							doc.close()
							raise KeyError("Keys for data provided do not match those in the doc.")
					else:
						raise TypeError("Insert data is not a dictionary.")
				doc_data["timestamp"] = time.asctime()
				ujson.dump(doc_data, doc)
				fcntl.flock(doc, fcntl.LOCK_UN)
				doc.close()
		else:
			raise TypeError("Insert parameter is not a list of dictionaries.")


	def delete_from_doc(self, doc_name, conditions_dictionary):
		if isinstance(conditions_dictionary, dict):
			doc_path = self.database + "/" + doc_name + ".gik"
			with open(doc_path, 'rb+') as doc:
				fcntl.flock(doc, fcntl.LOCK_EX)
				doc_data = ujson.load(doc)
				doc.seek(0)
				doc.truncate(0)
				for record in doc_data["records"]:
					if self.check_for_key_value_pairs_in_dict(conditions_dictionary, record):
						doc_data["records"].remove(record)
					else:
						continue
				doc_data["timestamp"] = time.asctime()
				ujson.dump(doc_data, doc)
				fcntl.flock(doc, fcntl.LOCK_UN)
				doc.close()
		else:
			raise TypeError("Condition data is not a dictionary.")

	def update_in_doc(self, doc_name, conditions_dictionary, new_key_value_dict):
		if isinstance(conditions_dictionary, dict) and isinstance(new_key_value_dict, dict):
			doc_path = self.database + "/" + doc_name + ".gik"
			with open(doc_path, 'rb+') as doc:
				fcntl.flock(doc, fcntl.LOCK_EX)
				doc_data = ujson.load(doc)
				doc.seek(0)
				doc.truncate(0)
				for record in doc_data["records"]:
					if self.check_for_keys_in_dict(new_key_value_dict, record) and self.check_for_key_value_pairs_in_dict(conditions_dictionary, record):
						for key in new_key_value_dict.keys():
							record[key] = new_key_value_dict[key]
					else:
						continue
				doc_data["timestamp"] = time.asctime()
				ujson.dump(doc_data, doc)
				fcntl.flock(doc, fcntl.LOCK_UN)
				doc.close()
		else:
			raise TypeError("Condition data or update data is not a dictionary")
						 

	def search_from_doc(self, doc_name, conditions_dictionary):
		if isinstance(conditions_dictionary, dict):
			doc_path = self.database + "/" + doc_name + ".gik"
			with open(doc_path, 'rb+') as doc:
				fcntl.flock(doc, fcntl.LOCK_EX)
				doc_data = ujson.load(doc)
				results_list = list()
				for record in doc_data["records"]:
					if self.check_for_key_value_pairs_in_dict(conditions_dictionary, record):
						results_list.append(record)
					else:
						continue
				fcntl.flock(doc, fcntl.LOCK_UN)
				doc.close()
				return results_list
		else:
			raise TypeError("Condition data is not a dictionary.")

	def dropdoc(self, doc_name):
		doc_path = self.database + "/" + doc_name + ".gik"
		assert (os.path.exists(doc_path)),"Database not created/opened or specified doc does not exists."
		os.remove(doc_path)

	def closedb(self):
		self.database = ""

	def dropdb(self, database_name):
		assert (os.path.exists(database_name) and len(self.database) < 1),"Database " + database_name + " does not exist or is not closed."
		shutil.rmtree(database_name)

	def get_databases(self):
		databases = os.listdir(".data")
		return databases

	def get_docs(self):
		docs = [doc.replace(".gik", "") for doc in os.listdir(self.database)]
		return docs

	def get_doc_keys(self, doc_name):
		doc_path = self.database + "/" + doc_name + ".gik"
		with open(doc_path, 'rb+') as doc:
			fcntl.flock(doc, fcntl.LOCK_EX)
			doc_data = ujson.load(doc)
			doc_keys = doc_data["keys"]
			fcntl.flock(doc, fcntl.LOCK_UN)
			doc.close()
			return doc_keys