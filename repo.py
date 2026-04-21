from typing import Any, Dict, Iterable, List, Optional, Sequence, Union
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson import ObjectId

"""
MongoDB connector class for basic CRUD operations.

Save as: /c:/Users/jame/OneDrive - Erhvervsakademi København/source/repo/TeamMgmt/repo.py
Dependencies: pymongo (pip install pymongo)
"""



class MongoDBRepo:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def create(self, data: Dict[str, Any]) -> str:
        result = self.collection.insert_one(data)
        print(f"Inserted document with id: {result.inserted_id}")
        return str(result.inserted_id)

    def read(self, item_id: str) -> Optional[Dict[str, Any]]:
        result = self.collection.find_one({"_id": ObjectId(item_id)})
        if result:
            result["_id"] = str(result["_id"])
        return result

    def update(self, item_id: str, data: Dict[str, Any]) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(item_id)}, {"$set": data}
        )
        return result.modified_count > 0

    def delete(self, item_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def list_all(self) -> List[Dict[str, Any]]:
        results = []
        for item in self.collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
        return results
    
    def close(self):
        self.client.close()

# Example usage:
if __name__ == "__main__":
    repo = MongoDBRepo("mongodb://localhost:27017/", "team_mgmt_db", "students")
    new_id = repo.create({"name": "John Doe", "age": 22, "email": "john.doe@example.com"})
    student = repo.read(new_id)
    print(student)
    repo.update(new_id, {"age": 23})
    # repo.delete(new_id)
    repo.close()  
