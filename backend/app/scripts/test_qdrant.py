from services.vector_store import client


def main():

    collections = client.get_collections()

    print("Connected to Qdrant!")

    print(
        "Collections:",
        collections,
    )


if __name__ == "__main__":
    main()