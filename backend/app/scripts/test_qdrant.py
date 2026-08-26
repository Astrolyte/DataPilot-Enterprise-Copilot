from services.vector_store import client, create_collections,COLLECTION_NAME


def main():

    collections = client.get_collections()

    print("Connected to Qdrant!")
    print(f"Existing collections {collections}")
    
    create_collections()
    
    collection = client.get_collection(COLLECTION_NAME)
    
    print("\n Collection created successfully")
    
    print("Vector size: ", collection.config.params.vectors.size)
    
    print("Distance:",collection.config.params.vectors.distance)
    
if __name__ == "__main__":
    main()