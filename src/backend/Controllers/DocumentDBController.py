import json
import glob
class DocumentDBController:
    
    def __init__(self):
        pass

    def get_collection_documents(self, collection):
        documents = []
        document_paths = glob.glob(f"src/backend/temp_document_db/{collection}*.json")
        for path in document_paths:
            with open(path, 'r') as json_doc:
                documents.append(json.load(json_doc))
        return documents

    def get_document(self, collection, id):
        with open(f'src/backend/temp_document_db/{collection}_{id}.json', 'r') as json_doc:
            return json.load(json_doc)
    
    def store_document(self, collection, id, document):
        with open(f'src/backend/temp_document_db/{collection}_{id}.json', 'w') as json_doc:
            json.dump(document, json_doc)

if __name__ == '__main__':
    controller = DocumentDBController()
    test = {"hello": True}
    controller.store_document('articles', '5f5e5f3c5e5f5f5f5f5f5f5f', test)
    controller.store_document('articles', '5f5e5f3c5e5f5f5f5fkeilai', test)
    docs = controller.get_collection_documents('articles')
    print(docs)