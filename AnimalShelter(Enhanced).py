from pymongo import MongoClient

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31482
        DB = 'AAC'
        COL = 'animals'
        
        try:
            # create the mongoDB connection string using credentials
            self.client = MongoClient(f'mongodb://{username}:{password}@{HOST}:{PORT}/?authSource=admin')
            # trigger and immediate connection test
            self.client.admin.command('ping')
            # connect to the specified database and collection
            self.database = self.client[DB]
            self.collection = self.database[COL]
        except ConnectionFailure as e:
            print("Could not connect to MongoDB:", e)
            raise
        

    # Create method to implement the C in CRUD.
    def create(self, data):
        #Insert a single document into the collection.
        #Returns True if successful, False otherwise.
        
        if not isinstance(data, dict):
            raise TypeError("Insert data must be a dictionary.")
        if not data:
            raise ValueError("Insert data cannot be empty.")

        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            print("Error inserting data:", e)
            return False
            
    # Create method to implement the R in CRUD.
    def read(self, query=None):
    # Read documents from the collection based on a query.
    # Returns a list of matching documents.

    if query is None:
        query = {}

    if not isinstance(query, dict):
        raise TypeError("Query must be a dictionary.")

    try:
        results = list(self.collection.find(query))

        # Return an empty list if no matching records are found.
        if not results:
            return []

        return results

    except Exception as e:
        print("Error reading data:", e)
        return []

    # Count matching records in the collection.
    def count(self, query=None):
        # Returns the number of documents that match a query.

        if query is None:
            query = {}

        if not isinstance(query, dict):
            raise TypeError("Query must be a dictionary.")

        try:
            return self.collection.count_documents(query)

        except Exception as e:
            print("Error counting documents:", e)
            return 0
        
    # Create method to implement the U in CRUD.
    def update(self, query, new_values):
        #Update matching documents with new values.
        #Returns the number of modified documents.
        
        if not isinstance(query, dict) or not isinstance(new_values, dict):
            raise TypeError("Both query and new_values must be dictionaries.")
        if not query or not new_values:
            raise ValueError("Neither query nor new_values can be empty.")
        
        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except Exception as e:
            print("Error updating data:", e)
            return 0
    
    # Create method to implement the D in CRUD.
    def delete(self, query):
        #Delete documents from the collection based on a query.
        #Returns the number of deleted documents.
        
        if not isinstance(query, dict):
            raise TypeError("Query must be a dictionary.")
        if not query:
            raise ValueError("Query cannot be empty.")
        
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print("Error deleting data:", e)
            return 0